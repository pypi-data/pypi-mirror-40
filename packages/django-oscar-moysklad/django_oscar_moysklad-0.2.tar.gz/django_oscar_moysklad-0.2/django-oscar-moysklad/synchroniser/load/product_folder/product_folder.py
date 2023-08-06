import time

from oscar.apps.catalogue.categories import create_from_breadcrumbs
from oscar.apps.catalogue.models import Category

from models import ProductFolderSync
from synchroniser.base import BaseSync
from synchroniser.util.loader import RequestList
from synchroniser.util.optional import Optional
from synchroniser.util.util import get_map_objects_by_id_element_row, \
    parse_date_for_moscow, only_insert_and_return_all


class ProductFolderSyncLoadTask(BaseSync):
    default_url = "https://online.moysklad.ru/api/remap/1.1/entity/productfolder/"
    root_sync_id = "4c158bc1-9b87-11e6-7a69-9711004871ba"

    def execute(self, last_update):
        folders_rows = []
        load_first = RequestList.load_one_row_by_url(ProductFolderSyncLoadTask.default_url
                                                     + ProductFolderSyncLoadTask.root_sync_id)

        path_name = load_first.get('name', None)
        if path_name is None:
            raise Exception("No found basic product folder name")
        params = {"filter": "pathName~=" + path_name}
        if last_update:
            params['updatedFrom'] = last_update.strftime('%Y-%m-%d %H:%M:%S')

        folders_rows.append(load_first)
        folders_rows.extend(RequestList.load_rows_by_url(ProductFolderSyncLoadTask.default_url, params=params))
        self.update_pf(folders_rows)

    def update_pf(self, product_folder_rows):
        product_folders_objs = []

        pf_by_sync_id_dict = get_map_objects_by_id_element_row(
            product_folder_rows,
            lambda sync_ids: ProductFolderSync.objects.get_by_sync_ids(sync_ids))

        for row in product_folder_rows:
            sync_id = row.get('id')
            pf_from_db = pf_by_sync_id_dict.get(sync_id) if pf_by_sync_id_dict.get(sync_id) else ProductFolderSync()

            parent_id = Optional(row.get('productFolder')).map(lambda x: x.get('meta')) \
                .map(lambda x: x.get('href')).if_exists(lambda x: x.replace(ProductFolderSyncLoadTask.default_url, ''))

            updated_date = parse_date_for_moscow(row.get('updated'))

            pf_from_db.sync_id = sync_id
            pf_from_db.parent_sync_id = parent_id
            pf_from_db.name = row.get('name')
            pf_from_db.path_name = row.get('pathName')
            pf_from_db.archived = row.get('archived')
            pf_from_db.updated = updated_date
            pf_from_db.path_name_changed = None

            product_folders_objs.append(pf_from_db)

        # print('sync before save' + str(time.clock()))
        result = only_insert_and_return_all(product_folders_objs, ProductFolderSync.objects)
        # print('sync after save' + str(time.clock()))

        dict_by_id = {result[i].sync_id: result[i] for i in range(0, len(result), )}

        for pf in result:
            parent = dict_by_id.get(pf.parent_sync_id)
            pf.parent_product_folder_sync = parent

        for pf in result:
            pf.path_name_changed = self.change_path(pf)

        ProductFolderSync.objects.bulk_update(result)

        self.update_categories(result)

    def update_categories(self, product_folder_syncs):
        # print('before save' + str(time.clock()))
        for pf_sync in product_folder_syncs:
            category = pf_sync.category if pf_sync.category else create_from_breadcrumbs(pf_sync.path_name_changed,
                                                                                         '${/}')

            # new_category = create_from_breadcrumbs(pf_sync.path_name_changed,
            #                                                                              '${/}');
            # if category.name != new_category.name:
            #     category.name = new_category.name
            #     category.save()

            # добавить archived
            # category.archived = pf_sync.archived
            # category.save()

            pf_sync.category = category
        # print('after save' + str(time.clock()))

        ProductFolderSync.objects.bulk_update(product_folder_syncs)

    def change_path(self, pf: ProductFolderSync):
        if pf.path_name_changed:
            return pf.path_name_changed
        parent_path = Optional(pf.parent_product_folder_sync) \
            .if_exists(lambda x: x.path_name_changed if x.path_name_changed else self.change_path(x))
        return parent_path + "${/}" + pf.name if parent_path else pf.name

# проверить перенос каталога
