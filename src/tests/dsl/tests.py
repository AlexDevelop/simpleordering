from django.test import TestCase

from django.conf import settings

from dsl.views import DslOrder
from utils.general import Ddict
import vcr
import os


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
            )
        ]

        self.items = items

    def test_valid_dslorder_v7(self):
        with vcr.use_cassette(os.path.join(settings.REPOSITORY_ROOT, 'fixtures/dsl/test_valid_dslorder_v7.yaml'),
                              record_mode='new_episodes'):
            for item in self.items:
                response = DslOrder().get_dslorder_v7(item.postcode, item.housenumber, item.housenumber_add)
                assert response.status_code is 200

    def test_valid_dslorder_v8(self):
        with vcr.use_cassette(os.path.join(settings.REPOSITORY_ROOT, 'fixtures/dsl/test_valid_dslorder_v8.yaml'),
                              record_mode='new_episodes'):
            for item in self.items:
                response = DslOrder().get_dslorder_v8(item.postcode, item.housenumber, item.housenumber_add)
                assert response.status_code is 200
