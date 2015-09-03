from django.utils.translation import ugettext_lazy as _

ORDER_INV_TO_CUSTOMER = _('Inventory naar Klant')
ORDER_CUSTOMER_TO_INV = _('Klant naar Inventory')
ORDER_GUIDION_TO_INV = _('Guidion naar Inventory')
ORDER_INV_TO_GUIDOON = _('Inventory naar Guidion naar Klant')
TYPE_OF_ORDER = (
    (0, ORDER_INV_TO_CUSTOMER),
    (1, ORDER_CUSTOMER_TO_INV),
    (2, ORDER_GUIDION_TO_INV),
    (3, ORDER_INV_TO_GUIDOON),
)
TYPE_OF_ORDER_DICT = {
    '0': ORDER_INV_TO_CUSTOMER,
    '1': ORDER_CUSTOMER_TO_INV,
    '2': ORDER_GUIDION_TO_INV,
    '3': ORDER_INV_TO_GUIDOON,
}