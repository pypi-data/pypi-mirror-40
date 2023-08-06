from django_bulk_update.helper import bulk_update

from models import StoreSync, StockTypeEnum, StockByStoreSync, ProductSync, VariantSync
from synchroniser.base import BaseSync
from synchroniser.load.product_folder.product_folder import ProductFolderSyncLoadTask
from synchroniser.load.products.product import ProductSyncLoadTask
from synchroniser.static.static_values import StaticSyncValues
from synchroniser.util.loader import RequestList
from synchroniser.load.stock.store import StoreSyncLoadTask
from oscar.apps.partner.models import StockRecord, Partner


class StockSyncLoadTask(BaseSync):
    default_url = "https://online.moysklad.ru/api/remap/1.1/report/stock/bystore/"
    # default_url_start_path = 'https://online.moysklad.ru/api/remap/1.1/entity/'

    # ?productFolder.id=4c158bc1-9b87-11e6-7a69-9711004871ba&stockMode=positiveOnly
    # filter=id!=6c605458-36b9-483a-9ddc-bf4e56522c24;id!=d79a0cf1-9120-11e6-7a69-9711006f784a
    def execute(self):
        params = {'productFolder.id': ProductFolderSyncLoadTask.root_sync_id, 'stockMode': 'positiveOnly'}
        rows = RequestList.load_rows_by_url(StockSyncLoadTask.default_url, params=params)
        self.update_pv(rows)

    def update_pv(self, stock_rows):
        all_stocks = []
        stores_map_by_sync_id = dict((x.sync_id, x) for x in StoreSync.objects.all())

        for row in stock_rows:
            type_enum = None
            sync_id = None
            if row.get('meta') and row.get('meta').get('href'):
                meta_array = row.get('meta').get('href').split("?")[0].split("/")
                sync_id = meta_array[len(meta_array)-1]
                type_enum = StockTypeEnum(meta_array[len(meta_array) - 2])
            if type_enum is None and sync_id is None:
                break

            for stock_by_store in row.get('stockByStore'):
                store_sync_id = ''
                if stock_by_store.get('meta') and stock_by_store.get('meta').get('href'):
                    store_sync_id = stock_by_store.get('meta').get('href').replace(StoreSyncLoadTask.default_url, '')

                store = stores_map_by_sync_id.get(store_sync_id)
                if store:
                    stock_by_store_db = StockByStoreSync()
                    stock_by_store_db.type_enum = type_enum
                    stock_by_store_db.product_or_variant_sync_id = sync_id
                    stock_by_store_db.store = store
                    stock_by_store_db.stock = stock_by_store.get('stock')
                    stock_by_store_db.reserve = stock_by_store.get('reserve')
                    stock_by_store_db.in_transit = stock_by_store.get('inTransit')
                    all_stocks.append(stock_by_store_db)

        StockByStoreSync.objects.all().delete()
        result = StockByStoreSync.objects.bulk_create(all_stocks)
        self.update_stock(result)

    def update_stock(self, stock_by_store):
        product_sync_ids = list(map(lambda x: x.product_or_variant_sync_id,
                                    filter(lambda x: x.type_enum == StockTypeEnum.PRODUCT, stock_by_store)))
        product_syncs = list(ProductSync.objects.filter(sync_id__in=product_sync_ids))
        product_map = {product_sync.sync_id: product_sync.product for product_sync in product_syncs}

        variant_sync_ids = list(map(lambda x: x.product_or_variant_sync_id,
                                    filter(lambda x: x.type_enum == StockTypeEnum.VARIANT, stock_by_store)))
        variant_syncs = list(VariantSync.objects.filter(sync_id__in=variant_sync_ids))
        variant_map = {product_sync.sync_id: product_sync.product for product_sync in variant_syncs}
        product_map.update(variant_map)

        products = product_map.values()
        stock_records = list(StockRecord.objects.select_related('product', 'partner').filter(product__in=products))

        product_stock_map = {(stock_record.product.id, stock_record.partner.id): stock_record
                             for stock_record in stock_records}

        updated_stock_records = []
        added_stock_records = []
        for stock in stock_by_store:
            product = product_map.get(stock.product_or_variant_sync_id)
            partner = stock.store.partner
            if product is not None and partner is not None:
                stock_record = product_stock_map.get((product.id, partner.id))
                if stock_record:
                    stock_record.num_in_stock = stock.stock if stock.stock > 0 else 0
                    updated_stock_records.append(stock_record)
                else:
                    stock_record = StockRecord(product=product, partner=partner)
                    stock_record.partner_sku = ProductSyncLoadTask.partner_sku_func(partner, product)
                    stock_record.num_in_stock = stock.stock if stock.stock > 0 else 0
                    added_stock_records.append(stock_record)

        StockRecord.objects.update(num_in_stock=0)
        update_result = bulk_update(updated_stock_records)
        insert_result = StockRecord.objects.bulk_create(added_stock_records)
