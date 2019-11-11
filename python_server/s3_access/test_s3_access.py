import unittest

from s3_access import *

class TestS3AccessMethods(unittest.TestCase):

    def test_download_file_from_S3(self):
        self.assertTrue(download_file_from_S3('smartmeetingsbelieving', 'gordonBurger.txt', 'ts65ue95bv6vi70y3gnogbmcs6mz'))
        self.assertFalse(download_file_from_S3('moon2LOLE', 'kidsface.jpg', 'yikes'))

    def test_upload_file_to_S3(self):
        #self.assertTrue(upload_file_to_S3('smartmeetingsbelieving', '__init__.py'))
        self.assertFalse(upload_file_to_S3('moon2LOLE', 'kidsface.jpg'))

if __name__ == '__main__':
    unittest.main()
