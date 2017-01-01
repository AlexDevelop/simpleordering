import re
from collections import OrderedDict
from copy import deepcopy

import requests
import xmltodict
from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
import xml.etree.ElementTree as ET

from dsl.models import DslRequest


class DslOrder(object):
    def __init__(self, event_validation=None, view_state=None):
        self.data_url = 'https://pqcc.soap.dslorder.nl/pqcc/v{}.0/pqcc.aspx'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'pqcc.soap.dslorder.nl',
            'Origin': 'https://pqcc.soap.dslorder.nl',
        }
        self.headers = headers

    def get_dslorder_v7(self, postcode, housenumber, housenumber_add=None):
        headers = self.headers
        headers['postcode'] = postcode
        headers['housenumber'] = housenumber
        headers['housenumber_add'] = housenumber_add

        viewstate_gen = settings.VIEW_STATE_GEN_V7
        event_validation = settings.EVENT_VALIDATION_V7
        view_state = settings.VIEW_STATE_V7

        post_data = '__LASTFOCUS=&__EVENTTARGET=&__EVENTARGUMENT=' \
                    '&__VIEWSTATE={viewstate}' \
                    '&__VIEWSTATEGENERATOR={viewstate_gen}&__EVENTVALIDATION={eventval}' \
                    '&Postcode={postcode}&HouseNumber={housenumber}&Addition={addition}&PhoneNumber=&CheckButton=Check'.format(
            postcode=postcode, housenumber=housenumber, addition=housenumber_add,
            viewstate=view_state, eventval=event_validation, viewstate_gen=viewstate_gen)
        data_url = self.data_url.format(7)

        response_v7 = requests.post(url=data_url, data=post_data, headers=headers, verify=False)
        return response_v7

    def get_dslorder_v8(self, postcode, housenumber, housenumber_add=None):
        viewstate_gen = settings.VIEW_STATE_GEN_V8
        event_validation = settings.EVENT_VALIDATION_V8
        view_state = settings.VIEW_STATE_V8

        data_url = self.data_url.format(8)
        headers = self.headers
        headers['Referer'] = data_url
        headers['Upgrade-Insecure-Requests'] = 1
        headers['postcode'] = postcode
        headers['housenumber'] = housenumber
        headers['housenumber_add'] = housenumber_add

        structure_post_data = '__LASTFOCUS=&__EVENTTARGET=&__EVENTARGUMENT=' \
                              '&__VIEWSTATE={viewstate}' \
                              '&__VIEWSTATEGENERATOR={viewstate_gen}&__EVENTVALIDATION={eventval}' \
                              '&PQCCType=Copper&Postcode={postcode}&HouseNumber={housenumber}&Addition={addition}&PhoneNumber=&CheckButton=Check'
        post_data = structure_post_data.format(
            postcode=postcode, housenumber=housenumber, addition=housenumber_add,
            viewstate=view_state, eventval=event_validation, viewstate_gen=viewstate_gen)

        response_v8 = requests.post(url=data_url, data=post_data, headers=headers, verify=False)
        return response_v8


def clean_params(data_to_clean):
    if not data_to_clean:
        return None
    new_data = type(data_to_clean)()
    for item in data_to_clean:
        if type(item) in (list, OrderedDict):
            #print 'type(item) in (list, OrderedDict)'
            item = clean_params(item)

        try:
            if type(data_to_clean[item]) == OrderedDict:
                #print 'type(data_to_clean[item]) == OrderedDict'
                data_to_clean[item] = clean_params(data_to_clean[item])
        except TypeError:
            pass
        try:
            values = data_to_clean[item]
        except TypeError:
            values = item

        new_item = item
        if type(item) == unicode:
            new_item = item.replace('@', '') if item.startswith('@') else item
            new_item = new_item.replace('-', '_')
            del (data_to_clean[item])

        if type(values) == list:
            values_fix = []
            for item in values:
                values_fix.append(clean_params(item))
            values = values_fix

        if type(data_to_clean) == list:
            new_data.append(values)
        if type(data_to_clean) == OrderedDict:
            new_data[new_item] = values
    return new_data


def parse_v8(doc):
    response_v8 = dict(
        deliverable_product=list()
    )

    # Search the dict for the dat that we need and transform it if needed
    pqcc_response = doc['PqccResponse']
    errors = clean_params(doc['PqccResponse']['Errors']['Error']) if doc['PqccResponse']['Errors'] else None
    response_v8_data = dict()
    response_v8_data['errors'] = errors
    if not errors:
        pqcc_response_copy = deepcopy(doc['PqccResponse'])
        deliverable_products = pqcc_response['DeliverableProducts']
        address = pqcc_response['Address']

        existing_situation = pqcc_response['ExistingSituation']
        existing_situation_copper = existing_situation[
            'ExistingSituationCopper'] if 'ExistingSituationCopper' in existing_situation else None
        existing_situation_fiber = existing_situation[
            'ExistingSituationFiber'] if 'ExistingSituationFiber' in existing_situation else None
        remarks = existing_situation['Remarks'] if 'Remarks' in existing_situation else None

        # Output to the view that consumes it
        # TODO Make it work for the entire XML, with all the dicts/lists deep inside it
        response_v8['deliverable_product'] = clean_params(
            deliverable_products['DeliverableProduct']) if deliverable_products else None
        response_v8['existing_situation_copper'] = clean_params(existing_situation_copper)
        response_v8['existing_situation_fiber'] = clean_params(existing_situation_fiber)
        response_v8['address'] = clean_params(address)
        if remarks:
            response_v8['remarks'] = clean_params(remarks['Remark'])
        else:
            response_v8['remarks'] = remarks

        copperconnection = response_v8['existing_situation_copper']['coper_connectionpointinfo']['copperconnection']
        if type(copperconnection) == list:
            response_v8['total_aderparen'] = len(copperconnection)
        else:
            response_v8['total_aderparen'] = 1
        response_v8_data = response_v8
        response_v8_data['errors'] = None
    return response_v8_data


def parse_v7(response_v8_data, response_v8, data):
    coper_connectionpointinfo = None
    copperconnection = None
    current_mdf_access_serviceid = None
    if response_v8_data and not response_v8_data['errors']:
        existing_situation_copper = response_v8_data['existing_situation_copper'] if 'existing_situation_copper' in response_v8_data else None
        if existing_situation_copper:
            coper_connectionpointinfo = existing_situation_copper[
                'coper_connectionpointinfo'] if 'coper_connectionpointinfo' in existing_situation_copper else None
        if coper_connectionpointinfo:
            copperconnection = coper_connectionpointinfo[
                'copperconnection'] if 'copperconnection' in coper_connectionpointinfo else None
        if copperconnection:
            current_mdf_access_serviceid = ''
            for item in copperconnection:
                if item == 'current_mdf_access_serviceid':
                    if copperconnection[item]:
                        current_mdf_access_serviceid += copperconnection[item] + ' '
                if type(item) == OrderedDict:
                    if item['current_mdf_access_serviceid']:
                        current_mdf_access_serviceid += item['current_mdf_access_serviceid'] + ' '

        v7_existing_dsl_service_id = data['existing_dsl_service_id'] if 'existing_dsl_service_id' in data else None
        existing_dsl_service_id = v7_existing_dsl_service_id if v7_existing_dsl_service_id else current_mdf_access_serviceid
        if existing_dsl_service_id:
            existing_dsl_service_id = existing_dsl_service_id.strip()

        data = [
            existing_dsl_service_id,
            v7_existing_dsl_service_id,
            current_mdf_access_serviceid,
            coper_connectionpointinfo,
            copperconnection
        ]
        return data


class SingleDsl(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    #authentication_classes = (authentication.,)
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        try:
            housenumber = request.QUERY_PARAMS['housenumber']
            postcode = request.QUERY_PARAMS['postcode']
        except MultiValueDictKeyError:
            return Response('Missing housenumber and/or postcode')

        try:
            housenumber_add = request.QUERY_PARAMS['housenumber_add']
        except MultiValueDictKeyError:
            housenumber_add = ''

        dsl_object = DslRequest(postcode=postcode, housenumber=housenumber, housenumber_add=housenumber_add)
        dsl_object.save()
        response_v7 = DslOrder().get_dslorder_v7(postcode, housenumber, housenumber_add)
        response_v8 = DslOrder().get_dslorder_v8(postcode, housenumber, housenumber_add)

        response_v8_data = None
        pqcc_response_copy = None
        if response_v8.status_code is 200:
            doc = xmltodict.parse(response_v8.content)
            response_v8_data = parse_v8(doc)

        if response_v7.status_code is 200:
            data = self.retrieve_parse_xml(response_v7.content)  # xmltodict.parse(response_v7.content)
            data_v7 = parse_v7(response_v8_data, response_v8, data)
            if data_v7:
                existing_dsl_service_id, v7_existing_dsl_service_id, current_mdf_access_serviceid, coper_connectionpointinfo, copperconnection = data_v7
            else:
                existing_dsl_service_id, v7_existing_dsl_service_id, current_mdf_access_serviceid, coper_connectionpointinfo, copperconnection = None, None, None, None, None
            try:
                data = {
                    "existing_dsl_service_id": existing_dsl_service_id if existing_dsl_service_id else '',
                    "name": str(data['name']),
                    "length_last_distributor": str(data['length_last_distributor']),
                    "length_mdf": str(data['length_mdf']),
                    "PostalCode": str(data['postal_code']),
                    "City": str(data['city']),
                    "Street": str(data['street']),
                    "HouseNumber": str(data['house_number']),
                    "HouseNumber_add": str(housenumber_add),
                    "products": data['products'],
                    "remarks": data['remarks'],
                    "v8": response_v8_data,
                    "v8_debug": pqcc_response_copy,
                }
            except Exception as e:
                print(e)
                return Response(e)
            return Response(data=data)

        return Response('Something went wrong - V7: {} - V8: {}'.format(response_v7.status_code, response_v8.status_code))

    def retrieve_parse_xml(self, content):

        tree = ET.fromstring(content)
        try:
            existing_dsl_service_id = tree.findall('ExistingSituation')[0].attrib['ExistingDslServiceId']
        except (KeyError, IndexError):
            existing_dsl_service_id = None

        try:
            name = tree.findall('Cgb')[0].attrib['Name']
        except (KeyError, IndexError):
            name = None

        try:
            length_last_distributor = tree.findall('Cgb')[0].attrib['LengthLastDistributor']
        except (KeyError, IndexError):
            length_last_distributor = None

        try:
            length_mdf = tree.findall('Cgb')[0].attrib['LengthMdf']
        except (KeyError, IndexError):
            length_mdf = None

        products = []
        # Deliverable Products
        for product in tree.findall('DeliverableProducts')[0]:
            network = product.attrib['Network']
            technology = product.attrib['Technology']
            expected_down = product.attrib['ExpectedDownKbps'] if 'ExpectedDownKbps' in product.attrib else '-'
            orderable_down = product.attrib['OrderableDownKbps']
            expected_up = product.attrib['ExpectedUpKbps'] if 'ExpectedUpKbps' in product.attrib else '-'
            orderable_up = product.attrib['OrderableUpKbps']
            products.append(
                {
                    'network': network,
                    'technology': technology,
                    'expected_down': expected_down,
                    'orderable_down': orderable_down,
                    'expected_up': expected_up,
                    'orderable_up': orderable_up
                }
            )

        remarks = []
        try:
            for remark in tree.findall('ExistingSituation')[0].findall('Remarks')[0]:
                remarks.append(remark.attrib['RemarkTextNed'])
        except IndexError as e:
            pass

        try:
            PostalCode = tree.findall('Address')[0].attrib['PostalCode']
            City = tree.findall('Address')[0].attrib['City']
            Street = tree.findall('Address')[0].attrib['Street']
            HouseNumber = tree.findall('Address')[0].attrib['HouseNumber']
        except KeyError:
            PostalCode = None
            City = None
            Street = None
            HouseNumber = None

        data = dict(
            existing_dsl_service_id=existing_dsl_service_id,
            name=name,
            length_last_distributor=length_last_distributor,
            length_mdf=length_mdf,
            postal_code=PostalCode,
            city=City,
            street=Street,
            house_number=HouseNumber,
            products=products,
            remarks=remarks
        )
        return data
