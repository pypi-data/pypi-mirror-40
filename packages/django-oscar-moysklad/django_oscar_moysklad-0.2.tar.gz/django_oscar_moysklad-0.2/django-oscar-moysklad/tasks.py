
from django.utils.timezone import now

from .models import SyncTaskObject
from .synchroniser.load.counter_party.counter_party import CounterPartyLoadTask
from .synchroniser.load.discount.accumulation_discount import AccumulationDiscountSyncTask
from .synchroniser.load.product_folder.product_folder import ProductFolderSyncLoadTask
from .synchroniser.load.products.product import ProductSyncLoadTask
from .synchroniser.load.stock.stock import StockSyncLoadTask
from .synchroniser.load.stock.store import StoreSyncLoadTask
from .synchroniser.load.variant.variant import VariantSyncLoadTask


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     print('-----dawdjwadiawjdoiawjjwaoi---')
#     # Calls test('hello') every 10 seconds.
#
#     sender.add_periodic_task(60*5, product_update_task.s(), name='add every 10')
#     sender.add_periodic_task(60*5, discount_update_task.s(), name='add every 10')
#
# #

# Tasks

# @app.task(name="initial_task")
def initial_task():
    print('-----PRODUCT UPDATE--------')
    product_updatе()
    print('-----DISCOUNT SYNC--------')
    discount_update()
    print('-----PRODUCT STOCK--------')
    product_sync_stock()


# @app.task(name="product_update_task")
def product_update_task():
    product_updatе()


# @app.task(name="product_sync_stock_task")
def product_sync_stock_task():
    product_sync_stock()


# @app.task(name="discount_update_task")
def discount_update_task(self):
    discount_update()


# Functions

def product_sync_stock():
    StockSyncLoadTask().execute()


def product_updatе():
    print('-Start product update task-')
    task, created = SyncTaskObject.objects.get_or_create(name='product_update_task')
    last_date = task.last_run_date

    ProductFolderSyncLoadTask().execute(last_date)
    StoreSyncLoadTask().execute(last_date)
    ProductSyncLoadTask().execute(last_date)
    VariantSyncLoadTask().execute(last_date)

    task.last_run_date = now()
    task.save()


def discount_update():
    print('-Start discount_update_task-')
    task, created = SyncTaskObject.objects.get_or_create(name='discount_update_task')
    last_date = task.last_run_date

    CounterPartyLoadTask().execute(last_date)
    AccumulationDiscountSyncTask().execute(last_date)

    task.last_run_date = now()
    task.save()

