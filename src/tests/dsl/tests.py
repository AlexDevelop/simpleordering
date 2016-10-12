import requests
import xmltodict
from django.test import TestCase

from django.conf import settings

from dsl.views import DslOrder, SingleDsl, clean_params
from utils.general import Ddict
import vcr
import os
import re
import urllib


class DslTest(TestCase):
    def setUp(self):
        items = [
            Ddict(
                postcode='1319CS',
                housenumber='105',
                housenumber_add=None,
            ),
            Ddict(
                postcode='1321HS',
                housenumber='44',
                housenumber_add=None,
            ),
            Ddict(
                postcode='3603AZ',
                housenumber='14',
                housenumber_add=None,
            ),
            Ddict(
                postcode='1967DC',
                housenumber='2260',
                housenumber_add=None,
            ),
            Ddict(
                postcode='3438LE',
                housenumber='136',
                housenumber_add=None,
            ),
            Ddict(
                postcode='1716KE',
                housenumber='38',
                housenumber_add=None,
            ),
            Ddict(
                postcode='1043EJ',
                housenumber='121',
                housenumber_add=None,
            ),
            Ddict(
                postcode='1311XB',
                housenumber='6',
                housenumber_add=None,
            )
        ]

        self.items = items

        response_v7 = requests.get('https://pqcc.soap.dslorder.nl/pqcc/v7.0/pqcc.aspx')
        self.event_validation_v7 = urllib.quote(re.findall('__EVENTVALIDATION.*?value=\"(.*?)\"', response_v7.content)[0], safe='')
        self.view_state_v7 = urllib.quote(re.findall('__VIEWSTATE\".*?value=\"(.*?)\"', response_v7.content)[0], safe='')

        response_v8 = requests.get('https://pqcc.soap.dslorder.nl/pqcc/v8.0/pqcc.aspx')
        self.event_validation_v8 = urllib.quote(re.findall('__EVENTVALIDATION.*?value=\"(.*?)\"', response_v8.content)[0], safe='')
        self.view_state_v8 = urllib.quote(re.findall('__VIEWSTATE\".*?value=\"(.*?)\"', response_v8.content)[0], safe='')

    def test_valid_dslorder_v7(self):
        with vcr.use_cassette(os.path.join(settings.REPOSITORY_ROOT, 'fixtures/dsl/test_valid_dslorder_v7.yaml'),
                              record_mode='new_episodes'):
            for item in self.items:
                response = DslOrder(event_validation=self.event_validation_v7, view_state=self.view_state_v7).get_dslorder_v7(item.postcode, item.housenumber, item.housenumber_add)
                data = xmltodict.parse(response.content)
                data_cleaned = clean_params(data)
                assert response.status_code is 200
                assert data_cleaned['PqccResponse']['Errors'] is None
                assert data_cleaned['PqccResponse']['Address']['PostalCode'] == item.postcode
                assert data_cleaned['PqccResponse']['Address']['HouseNumber'] == item.housenumber
                assert 'PossibleHouseNumberAdditions' in data_cleaned['PqccResponse']['Address']

    def test_valid_dslorder_v8(self):
        with vcr.use_cassette(os.path.join(settings.REPOSITORY_ROOT, 'fixtures/dsl/test_valid_dslorder_v8.yaml'),
                              record_mode='new_episodes'):
            for item in self.items:
                response = DslOrder(event_validation=self.event_validation_v8, view_state=self.view_state_v8).get_dslorder_v8(item.postcode, item.housenumber, item.housenumber_add)
                data = xmltodict.parse(response.content)
                data_cleaned = clean_params(data)
                assert response.status_code is 200
                assert data_cleaned['PqccResponse']['Errors'] is None
                assert data_cleaned['PqccResponse']['Address']['PostalCode'] == item.postcode
                assert data_cleaned['PqccResponse']['Address']['HouseNumber'] == item.housenumber
                assert 'PossibleHouseNumberAdditions' in data_cleaned['PqccResponse']['Address']

                housenumber_add = item.housenumber_add if item.housenumber_add else ''
                parameters = {'postcode': item.postcode, 'housenumber': item.housenumber, 'housenumber_add': housenumber_add}
                p = urllib.urlencode(parameters)
                response = requests.get('http://0.0.0.0:5555/dsl-info?{}'.format(p)).json()

                assert response['PostalCode'] == item.postcode
                assert response['HouseNumber'] == item.housenumber
                assert response['v8'] != None
