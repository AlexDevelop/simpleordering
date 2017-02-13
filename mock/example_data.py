from pprint import pprint

import types

example_data = {
    "@Whatever": "data1",
    "@Whateverr": "data2",
    "@Adress": [
        {}, {},
        {
            "@Street": 'Transistorstraat 55a',
            "@House-number": 50
        }
    ],
    "@Product-Tv": {
        "@Name": "xs4all",
        "@Channels": [
            {
                "@metadata": 1111
            },
            "npo_1", "npo_2"
        ]
    },
    "list_item": [{'value': 1}],
    "dict_item": {'value': 1}
}
unwanted_characters = {
    '@': '',
    '-': '_',
    '.': '_',
}


def clean_unwanted_parameters(data):
    item = data
    for key, replacement in unwanted_characters.iteritems():
        if key in data:
            item = data.replace(key, replacement)
    return item


def clean_dict(data):
    for item in data:
        raw_item = item

        # Try and set the raw values
        if type(item) == list:
            index_of_data = data.index(item)
            raw_values = data[index_of_data]
        elif type(item) == dict and item in data:
            if type(data) == list:
                index_of_data = data.index(item)
            else:
                index_of_data = item
            data[index_of_data] = clean_dict(item)
            raw_values = data[index_of_data]
        elif type(item) == str:
            if type(data) in (list, ):
                index_of_data = data.index(item)
                raw_values = data[index_of_data]
            else:
                raw_values = data[item]
            # clean keys (@ and replace unwanted points or dashes)
            item = clean_unwanted_parameters(item)

        # Replacement
        if '@' in raw_item or '-' in raw_item or '.' in raw_item:
            del(data[raw_item])
            data[item] = raw_values

        # Try and set the values
        if type(item) == list:
            index_of_data = data.index(item)
            values = data[index_of_data]
        elif type(item) == dict and item in data:
            if type(data) == list:
                index_of_data = data.index(item)
            else:
                index_of_data = item
            values = data[index_of_data]
        elif type(data) == list and type(item) in (str, int):
            values = item
        else:
            values = data[item]

        if type(values) in (list, ):
            data[item] = clean_dict(data[item])
        if type(values) in (dict, ):
            if type(data) == list:
                index_of_data = data.index(item)
            else:
                index_of_data = item
            data[index_of_data] = clean_dict(values)

    return data

data = clean_dict(example_data)
print
pprint(data, ) # width=300)
