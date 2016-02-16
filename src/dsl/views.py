import requests
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
import xml.etree.ElementTree as ET


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
            
        post_data = '__LASTFOCUS=&__EVENTTARGET=&__EVENTARGUMENT=' \
                    '&__VIEWSTATE=%2FwEPDwULLTExNjY2MDU5OTEPZBYCAgMPZBYCAgEPFgIeCWlubmVyaHRtbAUdVmVyc2lvbiA3LjEsIEZyaSAxNyBKdWwgMTM6NTJkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYCBQlTaG93RGVidWcFGENoZWNrZm9yVXBncmFkZURvd25HcmFkZadrpQNWL5nk7KwOV4zAatCv%2B18n' \
                    '&__VIEWSTATEGENERATOR=D8B62B3A&__EVENTVALIDATION=%2FwEWCAL01dzpAQLU4YLJCwLsu%2BfPCQL2soCpDQKJ%2BpbDCgLo1KSVDwKE%2FfOFAgLO4PZGcfjOTnCgzFi7KmMTv8whoMIaIy4%3D' \
                    '&Postcode={postcode}&HouseNumber={housenumber}&Addition={addition}&PhoneNumber=&ShowDebug=on&CheckButton=Check'.format(
            postcode=postcode, housenumber=housenumber, addition=housenumber_add,
        )
        data_url = 'https://pqcc.soap.dslorder.nl/pqcc/v7.0/pqcc.aspx'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'pqcc.soap.dslorder.nl',
            'Origin': 'https://pqcc.soap.dslorder.nl',
        }
        response = requests.post(url=data_url, data=post_data, headers=headers)

        if response.status_code is 200:
            existing_dsl_service_id, name, length_last_distributor, length_mdf = self.retrieve_parse_xml(response.content)

            data = {
                "existing_dsl_service_id": str(existing_dsl_service_id),
                "name": str(name),
                "length_last_distributor": str(length_last_distributor),
                "length_mdf": str(length_mdf)
            }
            return Response(data=data)

        return Response('Something went wrong')

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

        return existing_dsl_service_id, name, length_last_distributor, length_mdf
