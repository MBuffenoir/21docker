#!/usr/bin/env python3
# coding: utf-8

import app
# import json
from unittest import TestCase, mock

mock.patch('payment.required', lambda x: x)

# http://stackoverflow.com/questions/7667567/can-i-patch-a-python-decorator-before-it-wraps-a-function

class AppTestCase(TestCase):
    def setUp(self):
        self.app = app.app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    # Flask basics !
    def test_00_redirect_when_trailing_slash_is_missing(self):
        headers = [('Content-Type', 'application/json')]
        rv = self.app.get( '/docker/run')
        self.assertEqual(rv.status_code, 301)

    # Without mocking @payment.required
    def test_01_post_without_payment_should_402(self):
        headers = [('Content-Type', 'application/json')]
        rv = self.app.post( '/docker/run/')
        # print(rv)
        self.assertEqual(rv.status_code, 402)
        self.assertEqual(rv.data, b'Payment Required')
        assert b'Payment Required' in rv.data

    def test_02_post_json_without_image_key_should_422(self):
        headers = [('Content-Type', 'application/json')]
        data = '{"no_image_in_there"}'
        rv = self.app.post( '/docker/run', headers=headers, data=data, follow_redirects=True)
        self.assertEqual(rv.status_code, 422)

    # def test_02_post_image_name_no_tag(self):
    #     headers = [('Content-Type', 'application/json')]
    #     data = '{"image":"nginx"}'
    #     rv = self.app.post( '/docker/run', headers=headers, data=data, follow_redirects=True))
    #     self.assertEqual(rv.status_code, 422)

# post image name ending with colons should fail
# payment not done / done

if __name__ == '__main__':
    unittest.main()

# but I would point you to magicmock https://docs.python.org/3/library/unittest.mock.html in particular the usage `thing.method = MagicMock(return_value=True)`
# So you can, e.g., patch the unit tests that call paid methods with a MagicMock around `is_valid_payment`

