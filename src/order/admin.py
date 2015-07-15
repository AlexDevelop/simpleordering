from django.contrib import admin
from order.models import Order, Product, Customer
from django.core.urlresolvers import reverse
from django.template.loader import get_template
from django.utils.html import format_html


class OrderAdmin(admin.ModelAdmin):
    fields = ('quantity', 'product', 'order_date', 'type', 'customer', )
    list_display = ('id', 'batch_size', 'product', 'order_date', 'created', 'type', 'customer_custom', )

    def batch_size(self, obj):
        return obj.quantity
    batch_size.short_description = 'Batch Size'

    def customer_custom(self, obj):
        if not obj.customer:
            return ''
        url = reverse('admin:order_customer_change', args=(obj.customer.pk,))
        return format_html('<a href={url}>{name}</>'.format(url=url, name=obj.customer))
    customer_custom.allow_tags = True
    customer_custom.short_description = 'Customer'

class OrderInline(admin.TabularInline):
    model = Order
    fields = ('quantity', )
    extra = 0
    ordering = ('-created', )


class ProductAdmin(admin.ModelAdmin):
    inlines = (OrderInline, )
    fields = ('name', 'quantity', 'description', 'code', )
    exclude = ('order', 'update_batch_10', 'update_batch_5', 'update_batch_1', )
    list_display = ('name', 'quantity', 'description_custom', 'code', 'update_batch_10', 'update_batch_5', 'update_batch_1', )

    def description_custom(self, obj):
        if not obj.description:
            return ""

        return obj.description

    description_custom.short_description = 'Description'

    def update_batch_10(self, obj):
        return ProductAdmin.render_batch_helper(obj, 10, 'update')

    update_batch_10.allow_tags = True
    update_batch_10.short_description = ''

    def update_batch_5(self, obj):
        return ProductAdmin.render_batch_helper(obj, 5, 'update')

    update_batch_5.allow_tags = True
    update_batch_5.short_description = ''

    def update_batch_1(self, obj):
        return ProductAdmin.render_batch_helper(obj, 1, 'update')

    update_batch_1.allow_tags = True
    update_batch_1.short_description = ''

    @staticmethod
    def render_batch_helper(obj, batch_size=1, type='add'):
        product_id = obj.pk
        type = type

        route = 'add_order'
        add_route = reverse(route, kwargs={'order_id': product_id,'batch_size': batch_size})

        route = 'update_order'
        update_route = reverse(route, kwargs={'order_id': product_id,
                                                  'batch_size': batch_size})

        template_name = 'order/ajax-buttons-add.html'

        if type == 'update':
            template_name = 'order/ajax-buttons-update.html'

        template = get_template(template_name)
        rendered_html = template.render({'batch_size': batch_size,
                                         'product_id': product_id, 'type': type,
                                         'add_route': add_route, 'update_route': update_route})

        return rendered_html

    class Media:
        js = ('js/admin/add_batch.js', )


class CustomerAdmin(admin.ModelAdmin):
    fields = ('name', 'postalcode', 'housenumber', 'housenumber_addition', )
    list_display = ('name', 'postalcode', 'housenumber', 'housenumber_addition',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Customer, CustomerAdmin)
