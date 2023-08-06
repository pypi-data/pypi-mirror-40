# coding: utf-8
import unittest
from flask import Flask
from flask_qiniustoraging import Qiniu, prefix
from io import BytesIO


CONFIG = {
    'QINIU_ACCESS_KEY': 'Your access key',
    'QINIU_SECRET_KEY': 'Your secret key',
    'QINIU_BUCKET_NAME': 'Your bucket name',
    'QINIU_BUCKET_DOMAIN': 'Your bucket domain'
}


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.config.update(CONFIG)
        app.testing = True
        self.context = app.test_request_context()
        self.context.push()
        self.qiniu = Qiniu(app)

    def tearDown(self):
        self.context.pop()


class UploadTestCase(BaseTestCase):
    def test_upload_file(self):
        filename = 'text/test.txt'
        file_path = 'test.txt'
        ret, _ = self.qiniu.upload_file(filename, file_path)
        self.assertIsInstance(ret, dict)
        self.assertEqual(ret['key'], filename)

    def test_upload_data(self):
        filename = 'text/test_bytes.txt'
        out = BytesIO()
        out.write(b'test bytes')
        out.seek(0)
        ret, _ = self.qiniu.upload_data(filename, out.read())
        self.assertIsInstance(ret, dict)
        self.assertEqual(ret['key'], filename)

    def test_fetch_url(self):
        filename = 'image/test.jpg'
        url = 'https://picsum.photos/200'
        ret, _ = self.qiniu.fetch_url(filename, url)
        self.assertIsInstance(ret, dict)
        self.assertEqual(ret['key'], filename)

    def test_with_prefix(self):
        prefix_str = 'prefix/'
        with prefix(prefix_str):
            filename = 'text/test.txt'
            file_path = 'test.txt'
            ret, _ = self.qiniu.upload_file(filename, file_path)
            self.assertIsInstance(ret, dict)
            self.assertEqual(ret['key'], prefix_str + filename)


class ModifyTestCase(BaseTestCase):
    def test_rename(self):
        filename = 'text/test_bytes.txt'
        filename_to = 'text/test_byte.txt'
        ret, _ = self.qiniu.rename_file(filename, filename_to)
        self.assertFalse(ret)


class DeleteTestCase(BaseTestCase):
    def test_delete(self):
        files = [
            'text/test.txt',
            'text/test_byte.txt',
            'image/test.jpg',
            'prefix/text/test.txt'
        ]
        for file in files:
            ret, _ = self.qiniu.delete_file(file)
            self.assertFalse(ret)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(UploadTestCase))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(ModifyTestCase))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(DeleteTestCase))

    runner = unittest.TextTestRunner()
    runner.run(suite)
