from django.conf.urls import patterns, include, url
from django.contrib import admin
from frontend.views import DefaultFormsetView, DefaultFormView, DefaultFormByFieldView, \
    FormHorizontalView, FormInlineView, FormWithFilesView, PaginationView, MiscView, HomePageView, \
    loginview
from main import settings
from order import views as OrderProductViews
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'orders', OrderProductViews.OrderViewSet)
router.register(r'products', OrderProductViews.ProductViewSet)

urlpatterns = patterns('',
    # Order
    url(r'^order/?$', 'order.views.adjust_order', name='adjust_order'),
    url(r'^order/(?P<order_id>[0-9]+)/add/(?P<batch_size>[0-9]+)/?$', 'order.views.adjust_order', name='add_order'),
    url(r'^order/(?P<order_id>[0-9]+)/remove/(?P<batch_size>[0-9]+)/?$', 'order.views.adjust_order', name='update_order'),

   url(r'^login/?', loginview),

    # Frontend
    # url(r'^home/?$', 'frontend.views.home', name='home'),

    # Bootstrap demo
    url(r'^home/?$', HomePageView.as_view(), name='home'),
    url(r'^formset/?$', DefaultFormsetView.as_view(), name='formset_default'),
    url(r'^formset/(?P<success>[0,1,2]+)/?$', DefaultFormsetView.as_view(), name='formset_default_success'),
    url(r'^form/?$', DefaultFormView.as_view(), name='form_default'),
    url(r'^form_by_field/?$', DefaultFormByFieldView.as_view(), name='form_by_field'),
    url(r'^form_horizontal/?$', FormHorizontalView.as_view(), name='form_horizontal'),
    url(r'^form_inline/?$', FormInlineView.as_view(), name='form_inline'),
    url(r'^form_with_files/?$', FormWithFilesView.as_view(), name='form_with_files'),
    url(r'^pagination/?$', PaginationView.as_view(), name='pagination'),
    url(r'^misc/?$', MiscView.as_view(), name='misc'),

    # API Related
    url(r'^api/?', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),
    url(r'^admin/?', include(admin.site.urls)),
)

if settings.DEBUG is True:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
