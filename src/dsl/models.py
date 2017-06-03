from django.db import models
from order.models import TimeStampedModel


class DslRequest(TimeStampedModel):
    postcode = models.CharField(max_length=6, blank=False, null=False)
    housenumber = models.CharField(max_length=6, blank=False, null=False)
    housenumber_add = models.CharField(max_length=6, blank=True, null=True, default=None)

    def __str__(self):
        return "{} {}{}".format(self.postcode, self.housenumber, self.housenumber_add)