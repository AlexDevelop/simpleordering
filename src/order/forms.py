from django.forms import ModelForm
from order.models import Order
from suit.widgets import SuitDateWidget, SuitTimeWidget, SuitSplitDateTimeWidget


class OrderChangeForm(ModelForm):
    class Meta:
        model = Order
        widgets = {
            'order_date': SuitSplitDateTimeWidget,
        }
        fields = ('order_date', )
