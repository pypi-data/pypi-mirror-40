# coding: utf-8
# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="test_verify_digital.py">
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

import sys

import os
import unittest

import groupdocs_signature_cloud
from base_api_test import BaseApiTest
from groupdocs_signature_cloud.apis.signature_api import SignatureApi
from internal.test_files import TestFiles
from groupdocs_signature_cloud.models.requests.post_verification_digital_request import PostVerificationDigitalRequest
from groupdocs_signature_cloud.models.requests.post_verification_digital_from_url_request import PostVerificationDigitalFromUrlRequest
from groupdocs_signature_cloud.models.requests.post_verification_collection_request import PostVerificationCollectionRequest
from groupdocs_signature_cloud.models.requests.post_verification_collection_from_url_request import PostVerificationCollectionFromUrlRequest
from groupdocs_signature_cloud.models import *

class TestsVerificationDigital(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("\nVerification Digital")
        cls.BaseTest = BaseApiTest(fileStorage="Signature-Dev")
        cls.assertNotEqual(cls, cls.BaseTest.SignatureApi.api_client.configuration.access_token, "")

    def test_verify_post_digital_cells_collection(self):

        collection = VerifyOptionsCollectionData()
        options1 = self.get_options_verify_digital_cells()
        options2 = self.get_options_verify_digital_cells()
        collection._items = [options1, options2]

        file = self.BaseTest.TestFiles.getFileSignedCells()

        request = PostVerificationCollectionRequest(file.fileName, collection, file.password, file.folder, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_verification_collection(request)
        self.assert_response(file, response) 
    
    def test_verify_post_digital_cells_collection_url(self):

        collection = VerifyOptionsCollectionData()
        options1 = self.get_options_verify_digital_cells()
        options2 = self.get_options_verify_digital_cells()
        collection._items = [options1, options2]

        file = self.BaseTest.TestFiles.getFileSignedCellsUrl()

        request = PostVerificationCollectionFromUrlRequest(file.url, collection, file.password, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_verification_collection_from_url(request)
        self.assert_response(file, response, True)         
    
    def test_verify_post_digital_cells(self):
        file = self.BaseTest.TestFiles.getFileSignedCells()
        options = self.get_options_verify_digital_cells()
        request = PostVerificationDigitalRequest(file.fileName, options, file.password, file.folder, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_verification_digital(request)
        self.assert_response(file, response) 
        
    def test_verify_post_digital_cells_url(self):
        file = self.BaseTest.TestFiles.getFileSignedCellsUrl()
        options = self.get_options_verify_digital_cells()
        request = PostVerificationDigitalFromUrlRequest(file.url, options, file.password, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_verification_digital_from_url(request)
        self.assert_response(file, response, True)
        
    def get_options_verify_digital_cells(self):
        options = CellsVerifyDigitalOptionsData()
        self.compose_digital_verify_optionsData(options)
        return options
    
    def test_verify_post_digital_pdf(self):
        file = self.BaseTest.TestFiles.getFileSignedPdf()
        options = self.get_options_verify_digital_pdf()
        request = PostVerificationDigitalRequest(file.fileName, options, file.password, file.folder, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_verification_digital(request)
        self.assert_response(file, response)

    def test_verify_post_digital_pdf_url(self):
        file = self.BaseTest.TestFiles.getFileSignedPdfUrl()
        options = self.get_options_verify_digital_pdf()
        request = PostVerificationDigitalFromUrlRequest(file.url, options, file.password, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_verification_digital_from_url(request)
        self.assert_response(file, response, True)          

    def get_options_verify_digital_pdf(self):
        options = PdfVerifyDigitalOptionsData()
        self.compose_digital_verify_optionsData(options)
        return options

    def test_verify_post_digital_words(self):
        file = self.BaseTest.TestFiles.getFileSignedWords()
        options = self.get_options_verify_digital_words()
        request = PostVerificationDigitalRequest(file.fileName, options, file.password, file.folder, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_verification_digital(request)
        self.assert_response(file, response)

    def test_verify_post_digital_words_url(self):
        file = self.BaseTest.TestFiles.getFileSignedWordsUrl()
        options = self.get_options_verify_digital_words()
        request = PostVerificationDigitalFromUrlRequest(file.url, options, file.password, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_verification_digital_from_url(request)
        self.assert_response(file, response, True)  

    def get_options_verify_digital_words(self):
        options = WordsVerifyDigitalOptionsData()
        self.compose_digital_verify_optionsData(options)
        return options
    
    def compose_digital_verify_optionsData(self, options):
        # set digital properties
        options.certificate_guid = "certificates\\SherlockHolmes.pfx"
        options.password = "1234567890"

    def assert_response(self, file, response, url = False):
    
        self.assertNotEqual(response, False)
        self.assertEqual(response.code, "200")
        self.assertEqual(response.status, "OK")
        self.assertIn(file.fileName, response.file_name)
        if not url:
            self.assertEqual(response.folder, "signed")
        self.assertEqual(response.result, True)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
