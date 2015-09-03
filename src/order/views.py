import datetime, json
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from order.models import Order, Product

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from serializers import OrderSerializer, ProductSerializer


@csrf_exempt
def adjust_order(request, **kwargs):
    now = datetime.datetime.now()
    html = "test - {now}".format(now=now)
    retour_defect = False
    type = 'Regular'
    order_id = kwargs.get('order_id', None)
    batch_size = kwargs.get('batch_size', None)
    if batch_size:
        batch_size = int(batch_size)

    if order_id is None or batch_size is None:
        body = json.loads(request.body)
        if 'order_id' in body:
            order_id = body['order_id']
        if 'batch_size' in body:
            batch_size = body['batch_size']
        if 'type' in body:
            type = body['type']
        if 'date' in body:
            date = body['date']

    if order_id is None or batch_size is None:
        return HttpResponseBadRequest('Bad Request')

    try:
        batch_size = int(batch_size)
    except:
        return HttpResponseBadRequest('Bad Request')

    update_or_add = None
    if request.resolver_match.view_name == 'add_order':
        update_or_add = 'add'

    if request.resolver_match.view_name == 'adjust_order':
        update_or_add = 'add'

    if request.resolver_match.view_name == 'update_order':
        update_or_add = 'remove'

    if retour_defect == True:
        update_or_add = 'remove'

    # Updating quantity of product
    try:
        product = Product.objects.get(pk=order_id)

        order = Order(product=product)
        order.quantity = batch_size
        order.type = type
        order.order_date = date
        order.save()

        if update_or_add == 'add':
            product.quantity += order.quantity
        if update_or_add == 'remove':
            product.quantity -= order.quantity
        product.save()

    except Product.DoesNotExist:
        return HttpResponseNotFound('Product Not Found')

    # html = html + ' - Q: {quantity} - Name: {name} - Product Q: {product_quantity}'.format(
    #     quantity=order.quantity,
    #     name=order.product.name,
    #     product_quantity=product.quantity
    # )

    html = order.pk

    return HttpResponse(html)


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows orders to be viewed or edited.
    """
    queryset = Order.objects.all().order_by('-modified')
    serializer_class = OrderSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    queryset = Product.objects.all().order_by('name')
    serializer_class = ProductSerializer
