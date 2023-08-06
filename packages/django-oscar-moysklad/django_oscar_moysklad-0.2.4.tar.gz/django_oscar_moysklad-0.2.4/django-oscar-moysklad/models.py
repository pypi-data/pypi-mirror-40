import json
from enum import Enum

from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models
from oscar.apps.catalogue.models import Product, Category
from django_bulk_update.manager import BulkUpdateManager

from oscar.apps.partner.models import Partner, StockRecord
from oscar.core.compat import get_user_model

User = get_user_model()

class SyncBulkUpdateManager:
    def get_by_sync_ids(self, ids):
        return list(self.get_queryset().filter(sync_id__in=ids).all())

    def get_by_sync_id(self, id):
        return self.get_queryset().filter(sync_id=id).first()


class ProductSyncManager(BulkUpdateManager, SyncBulkUpdateManager):

    def get_queryset(self):
        return super(ProductSyncManager, self).get_queryset()


class ProductSync(models.Model):
    sync_id = models.CharField(max_length=100, unique=True)
    folder_sync_id = models.CharField(max_length=100, null=False)

    article = models.CharField(max_length=200, null=True)
    weight = models.IntegerField
    volume = models.IntegerField
    price = models.IntegerField

    path_name = models.CharField(max_length=200, null=True)
    archived = models.BooleanField()
    updated = models.DateTimeField()
    name = models.CharField(max_length=100, null=True)
    attributes = models.CharField(max_length=1000, default='{}')

    product = models.ForeignKey(Product, blank=True, null=True)

    objects = ProductSyncManager()
    product_sync = models.Manager()

    def set_attributes(self, x):
        self.attributes = json.dumps(x) if x else '{}'

    def get_attributes(self):
        return json.loads(self.attributes)


class ProductFolderSyncUpdateManager(BulkUpdateManager, SyncBulkUpdateManager):

    def get_queryset(self):
        return super(ProductFolderSyncUpdateManager, self).get_queryset()


class ProductFolderSync(models.Model):
    sync_id = models.CharField(max_length=100, unique=True)
    parent_sync_id = models.CharField(max_length=100, null=True)
    path_name = models.CharField(max_length=200)
    archived = models.BooleanField()
    updated = models.DateTimeField()
    name = models.CharField(max_length=100)
    parent_product_folder_sync = models.ForeignKey('ProductFolderSync', blank=True, null=True)
    path_name_changed = models.CharField(max_length=200, null=True)

    category = models.ForeignKey(Category, blank=True, null=True)

    objects = ProductFolderSyncUpdateManager()


class VariantSyncUpdateManager(BulkUpdateManager, SyncBulkUpdateManager):

    def get_queryset(self):
        return super(VariantSyncUpdateManager, self).get_queryset()


class VariantSync(models.Model):
    sync_id = models.CharField(max_length=100, unique=True)
    updated = models.DateTimeField()
    name = models.CharField(max_length=100)
    archived = models.BooleanField()
    price = models.IntegerField
    product_sync_id = models.CharField(max_length=100, null=True)
    characteristics = models.CharField(max_length=1000, default='{}')

    product = models.ForeignKey(Product, blank=True, null=True)

    def set_characteristics(self, x):
        self.characteristics = json.dumps(x) if x else '{}'

    def get_characteristics(self):
        return json.loads(self.characteristics)

    objects = VariantSyncUpdateManager()


class VariantCharacteristicsUpdateManager(BulkUpdateManager):

    def get_queryset(self):
        return super(VariantCharacteristicsUpdateManager, self).get_queryset()


class VariantCharacteristics(models.Model):
    sync_id = models.CharField(max_length=100, null=True)

    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    variant_sync_id = models.CharField(max_length=100, null=True)
    variant_sync_obj = models.ForeignKey('VariantSync', blank=True, null=True)

    objects = VariantCharacteristicsUpdateManager()


class StoreSyncUpdateManager(BulkUpdateManager, SyncBulkUpdateManager):

    def get_queryset(self):
        return super(StoreSyncUpdateManager, self).get_queryset()


class StoreSync(models.Model):
    sync_id = models.CharField(max_length=100, null=True)
    updated = models.DateTimeField()
    name = models.CharField(max_length=100, null=True)
    archived = models.BooleanField()
    path_name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=150, null=True)
    description = models.CharField(max_length=100, null=True)

    partner = models.ForeignKey(Partner, blank=True, null=True)
    objects = StoreSyncUpdateManager()


class StockByStoreSyncUpdateManager(BulkUpdateManager):

    def get_queryset(self):
        return super(StockByStoreSyncUpdateManager, self).get_queryset()


class StockTypeEnum(Enum):
    PRODUCT = 'product'
    VARIANT = 'variant'


class StockByStoreSync(models.Model):
    product_or_variant_sync_id = models.CharField(max_length=100, null=True)
    type_enum = models.CharField(max_length=50, choices=[(tag, tag.value) for tag in StockTypeEnum])
    store = models.ForeignKey('StoreSync', blank=True, null=True)
    stock = models.IntegerField
    in_transit = models.IntegerField
    reserve = models.IntegerField
    quantity = models.IntegerField

    objects = StoreSyncUpdateManager()


class UserSyncUpdateManager(BulkUpdateManager, SyncBulkUpdateManager):

    def get_queryset(self):
        return super(UserSyncUpdateManager, self).get_queryset()


class UserSync(models.Model):
    sync_id = models.CharField(max_length=100, unique=True)
    archived = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now_add=True,)
    email = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(User, blank=True, null=True)
    personal_discount = models.IntegerField(default=0)
    demand_sum_correction = models.IntegerField(default=0)

    objects = UserSyncUpdateManager()


class AccumulationDiscountSyncUpdateManager(BulkUpdateManager, SyncBulkUpdateManager):

    def get_queryset(self):
        return super(AccumulationDiscountSyncUpdateManager, self).get_queryset()


class AccumulationDiscountSync(models.Model):
    sync_id = models.CharField(max_length=100, unique=True)
    active = models.BooleanField()
    name = models.CharField(max_length=100, null=True)
    levels = models.CharField(max_length=1000)

    objects = AccumulationDiscountSyncUpdateManager()

    def set_levels(self, x):
        self.levels = json.dumps(x)

    def get_levels(self):
        return json.loads(self.levels)


class SyncTaskObject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    last_run_date = models.DateTimeField(null=True)
