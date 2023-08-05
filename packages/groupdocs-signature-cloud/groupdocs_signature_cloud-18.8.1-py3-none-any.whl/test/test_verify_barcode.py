# coding: utf-8
# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="test_verify_barcode.py">
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
from groupdocs_signature_cloud.models.requests.post_verification_barcode_request import PostVerificationBarcodeRequest
from groupdocs_signature_cloud.models.requests.post_verification_barcode_from_url_request import PostVerificationBarcodeFromUrlRequest
from groupdocs_signature_cloud.models.requests.post_verification_collection_request import PostVerificationCollectionRequest
from groupdocs_signature_cloud.models.requests.post_verification_collection_from_url_request import PostVerificationCollectionFromUrlRequest
from groupdocs_signature_cloud.models import *

class TestsVerificationBarcode(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("\nVerification Barcode")
        cls.BaseTest = BaseApiTest(fileStorage="Signature-Dev")
        cls.assertNotEqual(cls, cls.BaseTest.SignatureApi.api_client.configuration.access_token, "")
        
    def test_verify_post_barcode_cells_collection(self):

        collection = VerifyOptionsCollectionData()
        options1 = self.get_options_verify_barcode_cells()
        options2 = self.get_options_verify_barcode_cells()
        options2.text = "1234"
        options2.match_type ="StartsWith"
        collection._items = [options1, options2]

        file = self.BaseTest.TestFiles.getFileSignedCells()

        request = PostVerificationCollectionRequest(file.fileName, collection, file.password, file.folder, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_verification_collection(request)
        self.assert_response(file, response) 
    
    def test_verify_post_barcode_cells_collection_url(self):

        collection = VerifyOptionsCollectionData()
        options1 = self.get_options_verify_barcode_cells()
        options2 = self.get_options_verify_barcode_cells()
        options2.text = "1234"
        options2.match_type ="StartsWith"
        collection._items = [options1, options2]

        file = self.BaseTest.TestFiles.getFileSignedCellsUrl()

        request = PostVerificationCollectionFromUrlRequest(file.url, collection, file.password, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_verification_collection_from_url(request)
        self.assert_response(file, response, True)         
    
    def test_verify_post_barcode_cells(self):
        file = self.BaseTest.TestFiles.getFileSignedCells()
        options = self.get_options_verify_barcode_cells()
        request = PostVerificationBarcodeRequest(file.fileName, options, file.password, file.folder, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_verification_barcode(request)
        self.assert_response(file, response) 
        
    def test_verify_post_barcode_cells_url(self):
        file = self.BaseTest.TestFiles.getFileSignedCellsUrl()
        options = self.get_options_verify_barcode_cells()
        request = PostVerificationBarcodeFromUrlRequest(file.url, options, file.password, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_verification_barcode_from_url(request)
        self.assert_response(file, response, True)
        
    def get_options_verify_barcode_cells(self):
        options = CellsVerifyBarcodeOptionsData()
        self.compose_barcode_verify_optionsData(options)
        return options
    
    def test_verify_post_barcode_docimages(self):
        file = self.BaseTest.TestFiles.getFileSignedDocImages()
        options = self.get_options_verify_barcode_docimages()
        request = PostVerificationBarcodeRequest(file.fileName, options, file.password, file.folder, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_verification_barcode(request)
        self.assert_response(file, response)

    def test_verify_post_barcode_docimages_url(self):
        file = self.BaseTest.TestFiles.getFileSignedDocImagesUrl()
        options = self.get_options_verify_barcode_docimages()
        request = PostVerificationBarcodeFromUrlRequest(file.url, options, file.password, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_verification_barcode_from_url(request)
        self.assert_response(file, response, True)    

    def get_options_verify_barcode_docimages(self):
        options = ImagesVerifyBarcodeOptionsData()
        self.compose_barcode_verify_optionsData(options)
        return options

    def test_verify_post_barcode_pdf(self):
        file = self.BaseTest.TestFiles.getFileSignedPdf()
        options = self.get_options_verify_barcode_pdf()
        request = PostVerificationBarcodeRequest(file.fileName, options, file.password, file.folder, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_verification_barcode(request)
        self.assert_response(file, response)

    def test_verify_post_barcode_pdf_url(self):
        file = self.BaseTest.TestFiles.getFileSignedPdfUrl()
        options = self.get_options_verify_barcode_pdf()
        request = PostVerificationBarcodeFromUrlRequest(file.url, options, file.password, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_verification_barcode_from_url(request)
        self.assert_response(file, response, True)          

    def get_options_verify_barcode_pdf(self):
        options = PdfVerifyBarcodeOptionsData()
        self.compose_barcode_verify_optionsData(options)
        return options

    def test_verify_post_barcode_slides(self):
        file = self.BaseTest.TestFiles.getFileSignedSlides()
        options = self.get_options_verify_barcode_slides()
        request = PostVerificationBarcodeRequest(file.fileName, options, file.password, file.folder, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_verification_barcode(request)
        self.assert_response(file, response)

    def test_verify_post_barcode_slides_url(self):
        file = self.BaseTest.TestFiles.getFileSignedSlidesUrl()
        options = self.get_options_verify_barcode_slides()
        request = PostVerificationBarcodeFromUrlRequest(file.url, options, file.password, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_verification_barcode_from_url(request)
        self.assert_response(file, response, True)    

    def get_options_verify_barcode_slides(self):
        options = SlidesVerifyBarcodeOptionsData()
        self.compose_barcode_verify_optionsData(options)
        return options

    def test_verify_post_barcode_words(self):
        file = self.BaseTest.TestFiles.getFileSignedWords()
        options = self.get_options_verify_barcode_words()
        request = PostVerificationBarcodeRequest(file.fileName, options, file.password, file.folder, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_verification_barcode(request)
        self.assert_response(file, response)

    def test_verify_post_barcode_words_url(self):
        file = self.BaseTest.TestFiles.getFileSignedWordsUrl()
        options = self.get_options_verify_barcode_words()
        request = PostVerificationBarcodeFromUrlRequest(file.url, options, file.password, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_verification_barcode_from_url(request)
        self.assert_response(file, response, True)  

    def get_options_verify_barcode_words(self):
        options = WordsVerifyBarcodeOptionsData()
        self.compose_barcode_verify_optionsData(options)
        return options
    
    def compose_barcode_verify_optionsData(self, options):
        # set barcode properties
        options.barcode_type_name ="Code39Standard"
        options.text = "12345678"
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
