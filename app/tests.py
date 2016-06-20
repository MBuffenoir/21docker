import app
import unittest
import json

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()

    #not needed now
    #def tearDown(self):

    def test_01_post_wrong_data(self):
        headers = [('Content-Type', 'application/json')]
        data ="{'wrong'}"
        headers.append( ('Content-Length', len(data)) )
        rv = self.app.post( '/docker/run', headers=headers, data=data)
        self.assertEqual(rv.status_code, 422)

    def test_02_post_image_name_no_tag(self):
        headers = [('Content-Type', 'application/json')]
        data = '{"image":"nginx"}'
        rv = self.app.post( '/sensor', headers=headers, data=data)
        self.assertEqual(rv.status_code, 422)

if __name__ == '__main__':
    unittest.main()

# but I would point you to magicmock https://docs.python.org/3/library/unittest.mock.html in particular the usage `thing.method = MagicMock(return_value=True)`
# So you can, e.g., patch the unit tests that call paid methods with a MagicMock around `is_valid_payment`

