from django_bulk_update.helper import bulk_update
from oscar.apps.catalogue.models import Product, ProductClass, ProductAttribute, ProductAttributeValue, ProductCategory
from oscar.apps.partner.models import StockRecord, Partner

from helpers import product_title_parser
from models import ProductFolderSync, ProductSync
from synchroniser.base import BaseSync
from synchroniser.load.product_folder.product_folder import ProductFolderSyncLoadTask
from synchroniser.util.loader import RequestList
from synchroniser.util.optional import Optional
from synchroniser.util.util import get_map_objects_by_id_element_row, parse_date_for_moscow, update_or_insert


class ProductSyncLoadTask(BaseSync):
    default_url = "https://online.moysklad.ru/api/remap/1.1/entity/product/"

    attr_type_enum = {
        'customentity':
            (lambda attr: Optional(attr).map(lambda x: x.get('value')).if_exists(lambda x: x.get('name'))),
        'long':
            (lambda attr: Optional(attr).if_exists(lambda x: x.get('value')))
    }

    partner_sku_func = lambda partner, product: 'par=' + str(partner.id) + '_prod=' + str(product.id)

    def execute(self, last_update):
        root_product_folder_sync_obj = ProductFolderSync.objects.get_by_sync_id(ProductFolderSyncLoadTask.root_sync_id)
        path_name = root_product_folder_sync_obj.name
        if path_name is None:
            raise Exception("No found basic product folder name")

        params = {"filter": "pathName~=" + path_name}
        if last_update:
            params['updatedFrom'] = last_update.strftime('%Y-%m-%d %H:%M:%S')

        products_rows = RequestList.load_rows_by_url(ProductSyncLoadTask.default_url, params=params)
        self.update_p(products_rows)

    def update_p(self, product_rows):
        product_objs = []

        p_by_sync_id_dict = get_map_objects_by_id_element_row(
            product_rows,
            lambda sync_ids: ProductSync.objects.get_by_sync_ids(sync_ids))

        for row in product_rows:
            sync_id = row.get('id')
            p_from_db = p_by_sync_id_dict.get(sync_id) if p_by_sync_id_dict.get(sync_id) else ProductSync()

            product_folder_id = Optional(row.get('productFolder')).map(lambda x: x.get('meta')) \
                .map(lambda x: x.get('href')).if_exists(lambda x: x.replace(ProductFolderSyncLoadTask.default_url, ''))
            price = Optional(row.get('salePrices')).map(lambda x: x[0]).map(lambda x: x.get('value')) \
                .if_exists(lambda x: x / 100)
            updated_date = parse_date_for_moscow(row.get('updated'))

            p_from_db.sync_id = sync_id
            p_from_db.folder_sync_id = product_folder_id
            p_from_db.path_name = row.get('pathName')
            p_from_db.archived = row.get('archived')
            p_from_db.updated = updated_date
            p_from_db.name = product_title_parser(row.get('name'))
            p_from_db.article = row.get('article')
            p_from_db.volume = row.get('volume')
            p_from_db.weight = row.get('weight')
            p_from_db.price = price

            p_from_db.set_attributes(({attr.get('name'): self.attr_type_enum.get(attr.get('type'))(attr)
                                       for attr in row.get('attributes')}) if row.get('attributes') else None)

            product_objs.append(p_from_db)

        l = 0
        result = update_or_insert(product_objs, ProductSync.objects)
        self.update_product(result)
        k = 0

    def update_product(self, product_syncs):
        product_class = ProductClass.objects.get_or_create(name='moy_sklad')[0]
        sync_ids = list(map(lambda x: x.folder_sync_id, product_syncs))
        pf_syncs = list(ProductFolderSync.objects.filter(sync_id__in=sync_ids))
        pf_sync_map_by_sync = {pf_sync.sync_id: pf_sync for pf_sync in pf_syncs}

        for product_sync in product_syncs:
            pf_sync = pf_sync_map_by_sync.get(product_sync.folder_sync_id)

            product = product_sync.product if product_sync.product else Product()
            product.is_discountable = True
            product.product_class = product_class
            product.title = product_title_parser(product_sync.name)
            # product.categories = [pf_sync.category]
            product.save()

            for category in list(product.categories.all()):
                if category != pf_sync.category:
                    ProductCategory.objects.filter(category=category, product=product).delete()
            ProductCategory.objects.get_or_create(category=pf_sync.category, product=product)

            product_sync.product = product

        ProductSync.objects.bulk_update(product_syncs)

        update_product_attr_from_sync_obj(product_syncs, lambda x: x.get_attributes(), product_class)
        update_price_product_from_sync_obj(product_syncs)
        k = 0


def update_product_attr_from_sync_obj(product_syncs, get_attributes_func, product_class):
    attr_keys = set().union(*map(lambda x: list(get_attributes_func(x).keys()), product_syncs))
    attr_map = {}

    for attr_key in attr_keys:
        attr = \
            ProductAttribute.objects.get_or_create(product_class=product_class,
                                                   name=attr_key, code=attr_key, type='text')[0]
        attr_map[attr.code] = attr

    attrs = attr_map.values()
    products = list(map(lambda x: x.product, product_syncs))
    attr_values = list(ProductAttributeValue.objects.filter(attribute__in=attrs, product__in=products))
    attr_values_map = {(attr.product.id, attr.attribute.id): attr for attr in attr_values}

    added_attr_values = []
    updated_attr_values = []
    deleted_attr_value_ids = []
    for product_sync in product_syncs:
        product = product_sync.product

        product_attr_values = []
        for key, value in get_attributes_func(product_sync).items():
            attr = attr_map.get(key)

            attr_value = attr_values_map.get((product.id, attr.id))
            attr_value = attr_value if attr_value else ProductAttributeValue(product=product, attribute=attr)
            attr_value.value_text = value
            # attr_value.save()
            if attr_value.id is None:
                added_attr_values.append(attr_value)
            else:
                updated_attr_values.append(attr_value)
            product_attr_values.append(attr_value)

        # проверить потом
        for deleted_attr in \
                list(product.attribute_values.exclude(id__in=list(map(lambda x: x.id, product_attr_values)))):
            deleted_attr_value_ids.append(deleted_attr.id)
            # deleted_attr.delete()
    update_result = bulk_update(updated_attr_values)
    insert_result = ProductAttributeValue.objects.bulk_create(added_attr_values)
    delete_result = ProductAttributeValue.objects.filter(id__in=deleted_attr_value_ids).delete()
    k = 0


def update_price_product_from_sync_obj(product_syncs):
    products = list(map(lambda x: x.product, product_syncs))
    partners = list(Partner.objects.all())
    stock_records = list(StockRecord.objects.filter(product__in=products, partner__in=partners))
    # хуевая операция, долгая?
    product_stock_map = {str(stock_record.product.id) + '_' + str(stock_record.partner.id): stock_record
                         for stock_record in stock_records}
    updated_stock_records = []
    added_stock_records = []
    for product_sync in product_syncs:
        for partner in partners:
            product = product_sync.product
            stock_record = product_stock_map.get(str(product.id) + '_' + str(partner.id))
            if stock_record:
                stock_record.price_excl_tax = product_sync.price
                stock_record.price_retail = product_sync.price
                # реализовать сохранение всех, иначе пиздец полный для большого количества
                # stock_record.save()
                updated_stock_records.append(stock_record)
            else:
                stock_record = StockRecord(product=product, partner=partner)
                stock_record.partner_sku = ProductSyncLoadTask.partner_sku_func(partner, product)
                stock_record.price_excl_tax = product_sync.price
                stock_record.price_retail = product_sync.price
                stock_record.num_in_stock = 0
                added_stock_records.append(stock_record)
    update_result = bulk_update(updated_stock_records)
    insert_result = StockRecord.objects.bulk_create(added_stock_records)
    c = 0


def delete_price(product_syncs):
    products = list(map(lambda x: x.product, product_syncs))
    StockRecord.objects.filter(product__in=products).delete()


# moy_sklad_product_class = ProductClass.objects.get_or_create(name='moy_sklad')[0]
