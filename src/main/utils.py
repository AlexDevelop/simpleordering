from django.utils.translation import ugettext_lazy as _

ORDER_INV_TO_CUSTOMER = _('Inventory naar Klant')
ORDER_CUSTOMER_TO_INV = _('Klant naar Inventory')
ORDER_GUIDION_TO_INV = _('Guidion naar Inventory')
ORDER_INV_TO_GUIDION = _('Inventory naar Guidion')
TYPE_OF_ORDER = (
    (0, ORDER_INV_TO_CUSTOMER),
    (1, ORDER_CUSTOMER_TO_INV),
    (2, ORDER_GUIDION_TO_INV),
    (3, ORDER_INV_TO_GUIDION),
)
TYPE_OF_ORDER_STRING = (
    ('0', ORDER_INV_TO_CUSTOMER),
    ('1', ORDER_CUSTOMER_TO_INV),
    ('2', ORDER_GUIDION_TO_INV),
    ('3', ORDER_INV_TO_GUIDION),
)
TYPE_OF_ORDER_DICT = {
    '0': ORDER_INV_TO_CUSTOMER,
    '1': ORDER_CUSTOMER_TO_INV,
    '2': ORDER_GUIDION_TO_INV,
    '3': ORDER_INV_TO_GUIDION,
}