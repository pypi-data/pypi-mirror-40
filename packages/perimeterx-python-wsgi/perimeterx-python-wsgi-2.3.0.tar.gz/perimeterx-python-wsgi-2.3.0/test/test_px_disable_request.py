from perimeterx import px_activities_client
from perimeterx.middleware import PerimeterX
from perimeterx.px_config import PxConfig
from werkzeug.test import EnvironBuilder

import unittest


class TestPxActivitiesClient(unittest.TestCase):

    def test_send_to_perimeterx(self):
        from django.core.wsgi import get_wsgi_application
        application = get_wsgi_application()
        config = PxConfig({'app_id': 'fake_app_id'})

        builder = EnvironBuilder(headers={}, path='/fake_app_id/init.js')

        environ = builder.get_environ()
        environ['px_disable_request'] = True
        px = PerimeterX(application, config)
        var = px.__call__(environ, lambda x: x)
        print 'bla'