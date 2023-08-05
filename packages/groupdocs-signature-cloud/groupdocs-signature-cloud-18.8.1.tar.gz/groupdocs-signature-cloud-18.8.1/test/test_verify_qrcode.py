# coding: utf-8
# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="test_verify_qrcode.py">
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
from groupdocs_signature_cloud.models.requests.post_verification_qr_code_request import PostVerificationQrCodeRequest
from groupdocs_signature_cloud.models.requests.post_verification_qr_code_from_url_request import PostVerificationQrCodeFromUrlRequest
from groupdocs_signature_cloud.models.requests.post_verification_collection_request import PostVerificationCollectionRequest
from groupdocs_signature_cloud.models.requests.post_verification_collection_from_url_request import PostVerificationCollectionFromUrlRequest
from groupdocs_signature_cloud.models import *

class TestsVerificationQRCode(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("\nVerification QRCode")
        cls.BaseTest = BaseApiTest(fileStorage="Signature-Dev")
        cls.assertNotEqual(cls, cls.BaseTest.SignatureApi.api_client.configuration.access_token, "")

    def test_verify_post_qr_code_cells_collection(self):

        collection = VerifyOptionsCollectionData()
        options1 = self.get_options_verify_qr_code_cells()
        options2 = self.get_options_verify_qr_code_cells()
        options2.text = "John"
        options2.match_type ="StartsWith"
        collection._items = [options1, options2]

        file = self.BaseTest.TestFiles.getFileSignedCells()

        request = PostVerificationCollectionRequest(file.fileName, collection, file.password, file.folder, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_verification_collection(request)
        self.assert_response(file, response) 
    
    def test_verify_post_qr_code_cells_collection_url(self):

        collection = VerifyOptionsCollectionData()
        options1 = self.get_options_verify_qr_code_cells()
        options2 = self.get_options_verify_qr_code_cells()
        options2.text = "John"
        options2.match_type ="StartsWith"
        collection._items = [options1, options2]

        file = self.BaseTest.TestFiles.getFileSignedCellsUrl()

        request = PostVerificationCollectionFromUrlRequest(file.url, collection, file.password, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_verification_collection_from_url(request)
        self.assert_response(file, response, True)        
    
    def test_verify_post_qr_code_cells(self):
        file = self.BaseTest.TestFiles.getFileSignedCells()
        options = self.get_options_verify_qr_code_cells()
        request = PostVerificationQrCodeRequest(file.fileName, options, file.password, file.folder, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_verification_qr_code(request)
        self.assert_response(file, response) 
        
    def test_verify_post_qr_code_cells_url(self):
        file = self.BaseTest.TestFiles.getFileSignedCellsUrl()
        options = self.get_options_verify_qr_code_cells()
        request = PostVerificationQrCodeFromUrlRequest(file.url, options, file.password, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_verification_qr_code_from_url(request)
        self.assert_response(file, response, True)
        
    def get_options_verify_qr_code_cells(self):
        options = CellsVerifyQRCodeOptionsData()
        self.compose_qr_code_verify_optionsData(options)
        return options
    
    def test_verify_post_qr_code_docimages(self):
        file = self.BaseTest.TestFiles.getFileSignedDocImages()
        options = self.get_options_verify_qr_code_docimages()
        request = PostVerificationQrCodeRequest(file.fileName, options, file.password, file.folder, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_verification_qr_code(request)
        self.assert_response(file, response)

    def test_verify_post_qr_code_docimages_url(self):
        file = self.BaseTest.TestFiles.getFileSignedDocImagesUrl()
        options = self.get_options_verify_qr_code_docimages()
        request = PostVerificationQrCodeFromUrlRequest(file.url, options, file.password, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_verification_qr_code_from_url(request)
        self.assert_response(file, response, True)    

    def get_options_verify_qr_code_docimages(self):
        options = ImagesVerifyQRCodeOptionsData()
        self.compose_qr_code_verify_optionsData(options)
        return options

    def test_verify_post_qr_code_pdf(self):
        file = self.BaseTest.TestFiles.getFileSignedPdf()
        options = self.get_options_verify_qr_code_pdf()
        request = PostVerificationQrCodeRequest(file.fileName, options, file.password, file.folder, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_verification_qr_code(request)
        self.assert_response(file, response)

    def test_verify_post_qr_code_pdf_url(self):
        file = self.BaseTest.TestFiles.getFileSignedPdfUrl()
        options = self.get_options_verify_qr_code_pdf()
        request = PostVerificationQrCodeFromUrlRequest(file.url, options, file.password, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_verification_qr_code_from_url(request)
        self.assert_response(file, response, True)          

    def get_options_verify_qr_code_pdf(self):
        options = PdfVerifyQRCodeOptionsData()
        self.compose_qr_code_verify_optionsData(options)
        return options

    def test_verify_post_qr_code_slides(self):
        file = self.BaseTest.TestFiles.getFileSignedSlides()
        options = self.get_options_verify_qr_code_slides()
        request = PostVerificationQrCodeRequest(file.fileName, options, file.password, file.folder, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_verification_qr_code(request)
        self.assert_response(file, response)

    def test_verify_post_qr_code_slides_url(self):
        file = self.BaseTest.TestFiles.getFileSignedSlidesUrl()
        options = self.get_options_verify_qr_code_slides()
        request = PostVerificationQrCodeFromUrlRequest(file.url, options, file.password, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_verification_qr_code_from_url(request)
        self.assert_response(file, response, True)    

    def get_options_verify_qr_code_slides(self):
        options = SlidesVerifyQRCodeOptionsData()
        self.compose_qr_code_verify_optionsData(options)
        return options

    def test_verify_post_qr_code_words(self):
        file = self.BaseTest.TestFiles.getFileSignedWords()
        options = self.get_options_verify_qr_code_words()
        request = PostVerificationQrCodeRequest(file.fileName, options, file.password, file.folder, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_verification_qr_code(request)
        self.assert_response(file, response)

    def test_verify_post_qr_code_words_url(self):
        file = self.BaseTest.TestFiles.getFileSignedWordsUrl()
        options = self.get_options_verify_qr_code_words()
        request = PostVerificationQrCodeFromUrlRequest(file.url, options, file.password, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_verification_qr_code_from_url(request)
        self.assert_response(file, response, True)  

    def get_options_verify_qr_code_words(self):
        options = WordsVerifyQRCodeOptionsData()
        self.compose_qr_code_verify_optionsData(options)
        return options
    
    def compose_qr_code_verify_optionsData(self, options):
        # set qr_code properties
        options.qr_code_type_name ="Aztec"
        options.text = "John Smith"
        # set match type
        options.match_type ="Contains"
        #set pages for verify
        options.document_page_number = 1

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
