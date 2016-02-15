from datetime import datetime

from django.db import models
from django_extensions.db.fields import (ModificationDateTimeField,
                                         CreationDateTimeField)
from django.utils.translation import ugettext_lazy as _
from main.utils import *


class TimeStampedModel(models.Model):
    """ TimeStampedModel
    An abstract base class model that provides self-managed "created" and
    "modified" fields.
    """
    created = CreationDateTimeField(_('created'))
    modified = ModificationDateTimeField(_('modified'))

    class Meta:
        get_latest_by = 'modified'
        ordering = ('-modified', '-created',)
        abstract = True


class Order(TimeStampedModel):
    quantity = models.IntegerField(_('Order Quantity'), default=1)
    product = models.ForeignKey(to='Product', related_name="product")
    customer = models.ForeignKey(to='Customer', related_name="customer",
                                 blank=True, null=True)
    order_date = models.DateTimeField(verbose_name=_('Order / Delivery date'), default=datetime.now, )

    type = models.CharField(max_length=255, choices=TYPE_OF_ORDER_STRING, default=ORDER_INV_TO_CUSTOMER)
    deleted = models.BooleanField(default=False)

    def set_deleted_true(self, using=None):
        self.deleted = True
        self.save()

    class Meta:
        verbose_name = _("Order")

    def __str__(self):
        return "Order: {quantity} - {product}".format(quantity=self.quantity, product=self.product.name)


class Product(TimeStampedModel):
    name = models.CharField(_('name'), max_length=255)
    code = models.CharField(_('code'), max_length=255)
    quantity = models.IntegerField(_('Order Quantity'), default=0)
    description = models.CharField(_('description'), max_length=2048, default=None, null=True)

    class Meta:
        verbose_name = _("Product")

    def __unicode__(self):
        return "Product {name}".format(name=self.name)


class Customer(TimeStampedModel):
    name = models.CharField(_('fullname'), max_length=255)
    postalcode = models.CharField(_('postalcode'), max_length=8)
    housenumber = models.CharField(_('housenumber'), max_length=10)
    housenumber_addition = models.CharField(_('housenumber addition'), max_length=10, null=True,
                                            default=None, blank=True)

    class Meta:
        verbose_name = _("Customer")

    def __unicode__(self):
        return "Customer {name} - {postalcode} {housenumber} {housenumber_addition}".\
            format(
                name=self.name,
                postalcode=self.postalcode,
                housenumber=self.housenumber,
                housenumber_addition=self.housenumber_addition,
            )