from django.forms import widgets
from rest_framework import serializers
from models import Order, Product
from django.utils.timesince import timesince


class TimeStampedSerializer(serializers.Serializer):
    created = serializers.SerializerMethodField()
    modified = serializers.SerializerMethodField()

    def get_created(self, obj):
        time_pretty = timesince(obj.created)
        return time_pretty + " ago"

    def get_modified(self, obj):
        time_pretty = timesince(obj.modified)
        return time_pretty + " ago"


class OrderSerializer(TimeStampedSerializer):
    order_date = serializers.DateField(read_only=True)
    product = serializers.CharField(read_only=True)
    quantity = serializers.IntegerField(read_only=True)
    type = serializers.ChoiceField(Order.TYPE_OF_ORDER)

    class Meta:
        model = Order
        fields = ('id', 'order', 'quantity', 'type',)


class ProductSerializer(TimeStampedSerializer):
    name = serializers.CharField(read_only=True)
    quantity = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = ('name', 'quantity', 'code', 'description')