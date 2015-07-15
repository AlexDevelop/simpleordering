from django.conf.urls import patterns, include, url
from django.contrib import admin
from main import settings
from order import views as OrderProductViews
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'orders', OrderProductViews.OrderViewSet)
router.register(r'products', OrderProductViews.ProductViewSet)

urlpatterns = patterns('',
    # Examples:
    url(r'^order/?$', 'order.views.adjust_order', name='adjust_order'),
    url(r'^order/(?P<order_id>[0-9]+)/add/(?P<batch_size>[0-9]+)/?$', 'order.views.adjust_order', name='add_order'),
    url(r'^order/(?P<order_id>[0-9]+)/remove/(?P<batch_size>[0-9]+)/?$', 'order.views.adjust_order', name='update_order'),
    url(r'^api/?', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),
    url(r'^admin/?', include(admin.site.urls)),
)

if settings.DEBUG is True:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
