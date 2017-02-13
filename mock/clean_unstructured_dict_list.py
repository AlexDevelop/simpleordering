from pprint import pprint

data_list_2 = ['@alex', 'appel',]
data_dict_3 = {
    '@key_3a': 'value',
}

data_dict = {
    '@key_1a': 'value',
    '@key_1b': {
        '@key_2a': 'value_2',
        '@key_2b': data_list_2,
        '@key_2c': data_dict_3
    }
}
data_list = ['@alex', 'appel',
             data_dict]


def get_type(element):
    return type(element)


def replace_text(element):
    if type(element) == str:
        element = element.replace('@', '')
    return element


def clean_dict_keys(element):
    for key in element.keys():
        original_key = key

        new_key = replace_text(original_key)
        element[new_key] = element[original_key]
        del element[original_key]

        element[new_key] = clean(element[new_key])

    return element


def clean_list_values(element):
    for item in element:
        original_place = element.index(item)
        new_item = replace_text(item)
        element.append(new_item)
        del element[original_place]

    return element


def clean(data):
    type_element = get_type(data)
    if type_element == dict:
        data = clean_dict_keys(data)
    if type_element == list:
        data = clean_list_values(data)

    return data

pprint(clean(data_dict))
pprint(clean(data_list))
