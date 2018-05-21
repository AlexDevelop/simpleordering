from django import template
from django.template.defaultfilters import stringfilter
import json

register = template.Library()

@register.filter
def get_data(data, keys):
    keys_splitup = keys.split('.')
    if 'debug' in data:
        a = search_items(data['debug'], keys_splitup)
        return a  
    return 'Missing Data'


@register.filter
def get_and_join_data(data, keys):
    prepend = False
    if '__' in keys:
        keys,  prepend = keys.split('__')
    keys, search_key = keys.split(',')
    keys_splitup = keys.split('.')
    values_search_key = []
    if 'debug' in data:
        list_with_dicts = search_items(data['debug'], keys_splitup)
        if 'Key cannot be found' in list_with_dicts:
            return '' # list_with_dicts
        for counter, item in enumerate(list_with_dicts):
            a = type(item)
            if type(item) == unicode or type(item) == dict:
                continue
            if search_key not in item or not item[search_key]:
                continue
            if prepend:
                values_search_key.append('[{}] {}'.format(counter, item[search_key]))
            else:
                values_search_key.append('{}'.format(item[search_key]))
        return ' '.join(values_search_key)
    return 'Missing Data'


def search_items(data, keys):
    if keys[0] in data:
        return search_item(data[keys[0]], keys, 1)
    else:
        return '' #'Key cannot be found: {}'.format(keys[0])


def search_item(data, keys, counter):
    if not data:
        return 'Missing Data'

    if counter == len(keys):
        return data

    if keys[counter] in data:
        return search_item(data[keys[counter]], keys, counter + 1)
    else:
        return '' # 'Key cannot be found: {}'.format(keys[counter])
