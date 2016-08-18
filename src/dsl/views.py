import re
from collections import OrderedDict
from copy import deepcopy
from urllib import urlencode, quote

import requests
import xmltodict
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
import xml.etree.ElementTree as ET
from django.utils.html import escape


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

        event_validation = '%2FwEWCAL01dzpAQLU4YLJCwLsu%2BfPCQL2soCpDQKJ%2BpbDCgLo1KSVDwKE%2FfOFAgLO4PZGcfjOTnCgzFi7KmMTv8whoMIaIy4%3D'
        viewstate = '%2FwEPDwULLTExNjY2MDU5OTEPZBYCAgMPZBYCAgEPFgIeCWlubmVyaHRtbAUdVmVyc2lvbiA3LjEsIEZyaSAxNyBKdWwgMTM6NTJkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYCBQlTaG93RGVidWcFGENoZWNrZm9yVXBncmFkZURvd25HcmFkZadrpQNWL5nk7KwOV4zAatCv%2B18n'
        viewstate_gen = 'D8B62B3A'
        post_data = '__LASTFOCUS=&__EVENTTARGET=&__EVENTARGUMENT=' \
                    '&__VIEWSTATE=%2FwEPDwULLTExNjY2MDU5OTEPZBYCAgMPZBYCAgEPFgIeCWlubmVyaHRtbAUdVmVyc2lvbiA3LjEsIEZyaSAxNyBKdWwgMTM6NTJkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYCBQlTaG93RGVidWcFGENoZWNrZm9yVXBncmFkZURvd25HcmFkZadrpQNWL5nk7KwOV4zAatCv%2B18n' \
                    '&__VIEWSTATEGENERATOR=D8B62B3A&__EVENTVALIDATION=%2FwEWCAL01dzpAQLU4YLJCwLsu%2BfPCQL2soCpDQKJ%2BpbDCgLo1KSVDwKE%2FfOFAgLO4PZGcfjOTnCgzFi7KmMTv8whoMIaIy4%3D' \
                    '&Postcode={postcode}&HouseNumber={housenumber}&Addition={addition}&PhoneNumber=&ShowDebug=on&CheckButton=Check'.format(
            postcode=postcode, housenumber=housenumber, addition=housenumber_add,
            viewstate=viewstate,
            eventval=event_validation, viewstate_gen=viewstate_gen)
        data_url = 'https://pqcc.soap.dslorder.nl/pqcc/v7.0/pqcc.aspx'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'pqcc.soap.dslorder.nl',
            'Origin': 'https://pqcc.soap.dslorder.nl',
        }
        response_v7 = requests.post(url=data_url, data=post_data, headers=headers, verify=False)

        headers['Referer'] = 'https://pqcc.soap.dslorder.nl/pqcc/v8.0/pqcc.aspx'
        headers['Upgrade-Insecure-Requests'] = 1
        event_validation = '%2FwEWCwK8oYf6AwLU4YLJCwLsu%2BfPCQL2soCpDQKJ%2BpbDCgKlwLy3CQLo1KSVDwL285TWCwK5wL7SBgKVpJXOBgLO4PZGVMavHAbsm%2FDWmFiBFFIA00XUNpA%3D'
        viewstate = '%2FwEPDwUKMTY5MDMxMTI0OA9kFgICAw9kFgYCAQ8WAh4JaW5uZXJodG1sBR1WZXJzaW9uIDguMCwgVHVlIDI5IE1hciAxNjoxOWQCIw8QDxYCHgdDaGVja2VkaGRkZGQCJQ8QDxYCHwFnZGRkZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WBgUJU2hvd0RlYnVnBQ1Db3ZlcmFnZUNoZWNrBQ1Db3ZlcmFnZUNoZWNrBQZDb3BwZXIFBUZpYmVyBQVGaWJlct4vSGejrc7z2KI5mRWzo%2F2rokl%2B'
        viewstate_gen = 'B1924A1F'
        structure_post_data = '__LASTFOCUS=&__EVENTTARGET=&__EVENTARGUMENT=' \
                              '&__VIEWSTATE={viewstate}' \
                              '&__VIEWSTATEGENERATOR={viewstate_gen}&__EVENTVALIDATION={eventval}' \
                              '&PQCCType=Copper&Postcode={postcode}&HouseNumber={housenumber}&Addition={addition}&PhoneNumber=&CheckButton=Check'
        post_data = structure_post_data.format(
            postcode=postcode, housenumber=housenumber, addition=housenumber_add,
            viewstate=viewstate,
            eventval=event_validation, viewstate_gen=viewstate_gen)
        data_url = 'https://pqcc.soap.dslorder.nl/pqcc/v8.0/pqcc.aspx'
        response_v8 = requests.post(url=data_url, data=post_data, headers=headers, verify=False)

        response_v8_data = None
        if response_v8.status_code is 200:
            doc = xmltodict.parse(response_v8.content)

            response_v8 = dict(
                deliverable_product=list()
            )

            # Search the dict for the dat that we need and transform it if needed
            pqcc_response = doc['PqccResponse']
            pqcc_response_copy = deepcopy(doc['PqccResponse'])
            deliverable_products = pqcc_response['DeliverableProducts']
            address = pqcc_response['Address']
            deliverable_product = deliverable_products['DeliverableProduct']

            existing_situation = pqcc_response['ExistingSituation']
            existing_situation_copper = existing_situation['ExistingSituationCopper']
            existing_situation_fiber = existing_situation['ExistingSituationFiber']
            remarks = existing_situation['Remarks']

            # Output to the view that consumes it
            # TODO Make it work for the entire XML, with all the dicts/lists deep inside it
            response_v8['deliverable_product'] = SingleDsl.clean_params(deliverable_products['DeliverableProduct'])
            response_v8['existing_situation_copper'] = SingleDsl.clean_params(existing_situation_copper)
            response_v8['existing_situation_fiber'] = SingleDsl.clean_params(existing_situation_fiber)
            response_v8['address'] = SingleDsl.clean_params(address)
            if remarks:
                response_v8['remarks'] = SingleDsl.clean_params(remarks['Remark'])
            else:
                response_v8['remarks'] = remarks

            response_v8_data = response_v8

        if response_v7.status_code is 200:
            data = self.retrieve_parse_xml(response_v7.content)

            coper_connectionpointinfo = None
            copperconnection = None
            current_mdf_access_serviceid = None
            existing_situation_copper = response_v8['existing_situation_copper']
            if existing_situation_copper:
                coper_connectionpointinfo = existing_situation_copper['coper_connectionpointinfo'] if 'coper_connectionpointinfo' in existing_situation_copper else None
            if coper_connectionpointinfo:
                copperconnection = coper_connectionpointinfo['copperconnection'] if 'copperconnection' in coper_connectionpointinfo else None
            if copperconnection:
                current_mdf_access_serviceid = ''
                for item in copperconnection:
                    if item == 'current_mdf_access_serviceid':
                        current_mdf_access_serviceid += copperconnection[item] + ' '
                    if type(item) == OrderedDict:
                        current_mdf_access_serviceid += item['current_mdf_access_serviceid'] + ' '

            v7_existing_dsl_service_id = data['existing_dsl_service_id']
            existing_dsl_service_id = v7_existing_dsl_service_id if v7_existing_dsl_service_id else current_mdf_access_serviceid
            if existing_dsl_service_id:
                existing_dsl_service_id = existing_dsl_service_id.strip()

            data = {
                "existing_dsl_service_id": existing_dsl_service_id,
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
            return Response(data=data)

        return Response('Something went wrong')

    @staticmethod
    def clean_params(data_to_clean):
        new_data = type(data_to_clean)()
        for item in data_to_clean:
            if type(item) in (list, OrderedDict):
                print 'type(item) in (list, OrderedDict)'
                item = SingleDsl.clean_params(item)

            try:
                if type(data_to_clean[item]) == OrderedDict:
                    print 'type(data_to_clean[item]) == OrderedDict'
                    data_to_clean[item] = SingleDsl.clean_params(data_to_clean[item])
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
                    values_fix.append(SingleDsl.clean_params(item))
                values = values_fix

            if type(data_to_clean) == list:
                new_data.append(values)
            if type(data_to_clean) == OrderedDict:
                new_data[new_item] = values
        return new_data

    def retrieve_parse_xml(self, content):

        tree = ET.fromstring(content)
        #tree = ET.parse('1354EJ49.xml')
        try:
            existing_dsl_service_id = tree.findall('Response')[0].findall('ExistingSituation')[0].attrib['ExistingDslServiceId']
        except KeyError:
            existing_dsl_service_id = None

        try:
            name = tree.findall('Response')[0].findall('Cgb')[0].attrib['Name']
        except KeyError:
            name = None

        try:
            length_last_distributor = tree.findall('Response')[0].findall('Cgb')[0].attrib['LengthLastDistributor']
        except KeyError:
            length_last_distributor = None

        try:
            length_mdf = tree.findall('Response')[0].findall('Cgb')[0].attrib['LengthMdf']
        except KeyError:
            length_mdf = None

        products = []
        # Deliverable Products
        for product in tree.findall('Response')[0].findall('DeliverableProducts')[0]:
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
        for remark in tree.findall('Response')[0].findall('ExistingSituation')[0].findall('Remarks')[0]:
            remarks.append(remark.attrib['RemarkTextNed'])

        try:
            PostalCode = tree.findall('Response')[0].findall('Address')[0].attrib['PostalCode']
            City = tree.findall('Response')[0].findall('Address')[0].attrib['City']
            Street = tree.findall('Response')[0].findall('Address')[0].attrib['Street']
            HouseNumber = tree.findall('Response')[0].findall('Address')[0].attrib['HouseNumber']
        except KeyError:
            PostalCode = None
            City = None
            Street = None
            HouseNumber = None


        #<Address PostalCode="1354JE" City="ALMERE" HouseNumber="49" Street="Schoolwerf">
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
