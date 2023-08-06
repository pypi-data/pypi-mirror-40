# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['UserStateSchemaTestCase::test_create 1'] = {
    'data': {
        'createUserState': {
            'userState': {
                'data': {
                    'userRegions': [
                        {
                            'mapbox': {
                                'viewport': {
                                    'latitude': 50.5915,
                                    'longitude': 2.0165,
                                    'zoom': 7
                                }
                            },
                            'region': {
                            }
                        }
                    ]
                },
                'user': {
                }
            }
        }
    }
}
