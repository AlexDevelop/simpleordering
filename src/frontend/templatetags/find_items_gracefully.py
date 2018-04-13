from django import template
from django.template.defaultfilters import stringfilter
import json

register = template.Library()

@register.filter
def get_data(data, keys):
    keys_splitup = keys.split('.')
    a = search_items(data['debug'], keys_splitup)
    return a


def search_items(data, keys):
    if keys[0] in data:
        return search_item(data[keys[0]], keys, 1)
    else:
        return 'Key cannot be found: {}'.format(keys[0])


def search_item(data, keys, counter):
    if counter == len(keys):
        return data

    if keys[counter] in data:
        return search_item(data[keys[counter]], keys, counter + 1)
    else:
        return 'Key cannot be found: {}'.format(keys[counter])