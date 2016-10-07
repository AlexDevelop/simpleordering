import requests
from django.test import TestCase

from django.conf import settings

from dsl.views import DslOrder
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
                housenumber_add='',
            ),
            Ddict(
                postcode='1321HS',
                housenumber='44',
                housenumber_add='',
            ),
            Ddict(
                postcode='3603AZ',
                housenumber='14',
                housenumber_add='',
            ),
            Ddict(
                postcode='1967DC',
                housenumber='2260',
                housenumber_add='',
            ),
            Ddict(
                postcode='3438LE',
                housenumber='136',
                housenumber_add='',
            ),
            Ddict(
                postcode='1716KE',
                housenumber='38',
                housenumber_add='',
            ),
            Ddict(
                postcode='1043EJ',
                housenumber='121',
                housenumber_add='',
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
                              record_mode='all'):
            for item in self.items:
                response = DslOrder(event_validation=self.event_validation_v7, view_state=self.view_state_v7).get_dslorder_v7(item.postcode, item.housenumber, item.housenumber_add)
                assert response.status_code is 200

    def test_valid_dslorder_v8(self):
        with vcr.use_cassette(os.path.join(settings.REPOSITORY_ROOT, 'fixtures/dsl/test_valid_dslorder_v8.yaml'),
                              record_mode='all'):
            for item in self.items:
                response = DslOrder(event_validation=self.event_validation_v8, view_state=self.view_state_v8).get_dslorder_v8(item.postcode, item.housenumber, item.housenumber_add)
                assert response.status_code is 200
