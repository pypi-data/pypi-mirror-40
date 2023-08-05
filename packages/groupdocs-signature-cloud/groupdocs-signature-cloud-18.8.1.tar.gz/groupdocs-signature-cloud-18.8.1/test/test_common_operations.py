# coding: utf-8
# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="test_common_operations.py">
#   Copyright (c) 2018 Aspose Pty Ltd
# </copyright>
# <summary>
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
# </summary>
# -----------------------------------------------------------------------------------

import sys

import os
import unittest

import groupdocs_signature_cloud
from groupdocs_signature_cloud.apis.signature_api import SignatureApi
from groupdocs_signature_cloud.models.requests.get_barcodes_request import GetBarcodesRequest
from groupdocs_signature_cloud.models.requests.get_qr_codes_request import GetQrCodesRequest
from groupdocs_signature_cloud.models.requests.get_document_info_request import GetDocumentInfoRequest
from groupdocs_signature_cloud.models.requests.get_document_info_from_url_request import GetDocumentInfoFromUrlRequest
from groupdocs_signature_cloud.models.requests.get_supported_formats_request import GetSupportedFormatsRequest

from groupdocs_signature_cloud.rest import ApiException
from base_api_test import BaseApiTest

from internal.test_files import TestFiles

class TestsCommonOperations(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("\nCommon operations")
        cls.BaseTest = BaseApiTest(fileStorage="Signature-Dev")
        cls.assertNotEqual(cls, cls.BaseTest.SignatureApi.api_client.configuration.access_token, "")

    def test_get_supported_file_formats(self):
        request = GetSupportedFormatsRequest()
        response = self.BaseTest.SignatureApi.get_supported_formats(request)

        self.assertNotEqual(response, False)
        self.assertGreater(len(response.formats), 0)
        for curItem in response.formats: 
            self.assertNotEqual(curItem.extension, False)
            self.assertNotEqual(curItem.file_format, False)

    def test_get_supported_barcodes(self):
        request = GetBarcodesRequest()
        response = self.BaseTest.SignatureApi.get_barcodes(request)

        self.assertNotEqual(response, False)
        self.assertGreater(len(response.barcode_types), 0)
        for curItem in response.barcode_types: 
            self.assertNotEqual(curItem.name, False)

    def test_get_supported_qrcodes(self):
        request = GetQrCodesRequest()
        response = self.BaseTest.SignatureApi.get_qr_codes(request)

        self.assertNotEqual(response, False)
        self.assertGreater(len(response.qr_code_types), 0)
        for curItem in response.qr_code_types: 
            self.assertNotEqual(curItem.name, False)            

    def test_get_document_info(self):

        file = self.BaseTest.TestFiles.getFile02PagesPdf()
        
        request = GetDocumentInfoRequest(file.fileName, file.password, file.folder, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.get_document_info(request)

        self.assert_document_info_response(file, response, "Pdf")

    def test_get_document_info_from_url(self):

        file = self.BaseTest.TestFiles.getFile01PagesWordsUrl()
        
        request = GetDocumentInfoFromUrlRequest(file.url, file.password, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.get_document_info_from_url(request)

        self.assert_document_info_response(file, response, "Docx")

    def tearDown(self):
        pass

    def assert_document_info_response(self, file, response, fileFormat):
    
        self.assertNotEqual(response, False)
        self.assertEquals(file.fileName, response.name)
        self.assertEquals(file.folder,   response.folder)
        filename, file_extension = os.path.splitext(response.name)
        self.assertEquals(file_extension, "."+response.extension)

if __name__ == '__main__':
    unittest.main()
