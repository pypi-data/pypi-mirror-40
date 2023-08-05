# coding: utf-8
# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="test_search_qr_code.py">
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
from groupdocs_signature_cloud.models.requests.post_search_qr_code_request import PostSearchQrCodeRequest
from groupdocs_signature_cloud.models.requests.post_search_qr_code_from_url_request import PostSearchQrCodeFromUrlRequest
from groupdocs_signature_cloud.models.requests.post_search_collection_request import PostSearchCollectionRequest
from groupdocs_signature_cloud.models.requests.post_search_collection_from_url_request import PostSearchCollectionFromUrlRequest
from groupdocs_signature_cloud.models import *

class TestsSearchQRCode(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("\nSearch QRCode")
        cls.BaseTest = BaseApiTest(fileStorage="Signature-Dev")
        cls.assertNotEqual(cls, cls.BaseTest.SignatureApi.api_client.configuration.access_token, "")
            
    def test_search_post_qr_code_cells_collection(self):

        collection = SearchOptionsCollectionData()
        options1 = self.get_options_search_qr_code_cells()
        options2 = self.get_options_search_qr_code_cells()
        options2.text = "John"
        options2.match_type ="StartsWith"
        collection._items = [options1, options2]

        file = self.BaseTest.TestFiles.getFileSignedCells()

        request = PostSearchCollectionRequest(file.fileName, collection, file.password, file.folder, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_search_collection(request)
        self.assert_response(file, response) 
    
    def test_search_post_qr_code_cells_collection_url(self):

        collection = SearchOptionsCollectionData()
        options1 = self.get_options_search_qr_code_cells()
        options2 = self.get_options_search_qr_code_cells()
        options2.text = "John"
        options2.match_type ="StartsWith"
        collection._items = [options1, options2]

        file = self.BaseTest.TestFiles.getFileSignedCellsUrl()

        request = PostSearchCollectionFromUrlRequest(file.url, collection, file.password, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_search_collection_from_url(request)
        self.assert_response(file, response, True)         

    def test_search_post_qr_code_cells(self):
        file = self.BaseTest.TestFiles.getFileSignedCells()
        options = self.get_options_search_qr_code_cells()
        request = PostSearchQrCodeRequest(file.fileName, options, file.password, file.folder, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_search_qr_code(request)
        self.assert_response(file, response) 
       
    def test_search_post_qr_code_cells_url(self):
        file = self.BaseTest.TestFiles.getFileSignedCellsUrl()
        options = self.get_options_search_qr_code_cells()
        request = PostSearchQrCodeFromUrlRequest(file.url, options, file.password, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_search_qr_code_from_url(request)
        self.assert_response(file, response, True)
            
    def get_options_search_qr_code_cells(self):
        options = CellsSearchQRCodeOptionsData()
        self.compose_qr_code_search_optionsData(options)
        return options
    
    def test_search_post_qr_code_docimages(self):
        file = self.BaseTest.TestFiles.getFileSignedDocImages()
        options = self.get_options_search_qr_code_docimages()
        request = PostSearchQrCodeRequest(file.fileName, options, file.password, file.folder, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_search_qr_code(request)
        self.assert_response(file, response)

    def test_search_post_qr_code_docimages_url(self):
        file = self.BaseTest.TestFiles.getFileSignedDocImagesUrl()
        options = self.get_options_search_qr_code_docimages()
        request = PostSearchQrCodeFromUrlRequest(file.url, options, file.password, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_search_qr_code_from_url(request)
        self.assert_response(file, response, True)    

    def get_options_search_qr_code_docimages(self):
        options = ImagesSearchQRCodeOptionsData()
        self.compose_qr_code_search_optionsData(options)
        return options

    def test_search_post_qr_code_pdf(self):
        file = self.BaseTest.TestFiles.getFileSignedPdf()
        options = self.get_options_search_qr_code_pdf()
        request = PostSearchQrCodeRequest(file.fileName, options, file.password, file.folder, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_search_qr_code(request)
        self.assert_response(file, response)

    def test_search_post_qr_code_pdf_url(self):
        file = self.BaseTest.TestFiles.getFileSignedPdfUrl()
        options = self.get_options_search_qr_code_pdf()
        request = PostSearchQrCodeFromUrlRequest(file.url, options, file.password, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_search_qr_code_from_url(request)
        self.assert_response(file, response, True)          

    def get_options_search_qr_code_pdf(self):
        options = PdfSearchQRCodeOptionsData()
        self.compose_qr_code_search_optionsData(options)
        return options

    def test_search_post_qr_code_slides(self):
        file = self.BaseTest.TestFiles.getFileSignedSlides()
        options = self.get_options_search_qr_code_slides()
        request = PostSearchQrCodeRequest(file.fileName, options, file.password, file.folder, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_search_qr_code(request)
        self.assert_response(file, response)

    def test_search_post_qr_code_slides_url(self):
        file = self.BaseTest.TestFiles.getFileSignedSlidesUrl()
        options = self.get_options_search_qr_code_slides()
        request = PostSearchQrCodeFromUrlRequest(file.url, options, file.password, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_search_qr_code_from_url(request)
        self.assert_response(file, response, True)    

    def get_options_search_qr_code_slides(self):
        options = SlidesSearchQRCodeOptionsData()
        self.compose_qr_code_search_optionsData(options)
        return options

    def test_search_post_qr_code_words(self):
        file = self.BaseTest.TestFiles.getFileSignedWords()
        options = self.get_options_search_qr_code_words()
        request = PostSearchQrCodeRequest(file.fileName, options, file.password, file.folder, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_search_qr_code(request)
        self.assert_response(file, response)

    def test_search_post_qr_code_words_url(self):
        file = self.BaseTest.TestFiles.getFileSignedWordsUrl()
        options = self.get_options_search_qr_code_words()
        request = PostSearchQrCodeFromUrlRequest(file.url, options, file.password, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_search_qr_code_from_url(request)
        self.assert_response(file, response, True)  

    def get_options_search_qr_code_words(self):
        options = WordsSearchQRCodeOptionsData()
        self.compose_qr_code_search_optionsData(options)
        return options
    
    def compose_qr_code_search_optionsData(self, options):
        # set qr_code properties
        options.qr_code_type_name ="Aztec"
        options.text = "John Smith"
        # set match type
        options.match_type ="Contains"
        #set pages for search
        options.document_page_number = 1

    def assert_response(self, file, response, url = False):
    
        self.assertNotEqual(response, False)
        self.assertEqual(response.code, "200")
        self.assertEqual(response.status, "OK")
        self.assertIn(file.fileName, response.file_name)
        if not url:
            self.assertEqual(response.folder, "signed")
        self.assertNotEqual(response.signatures, False)
        self.assertGreater(len(response.signatures), 0)
        signature = response.signatures[0]
        self.assertEqual(signature.text, "John Smith")
        self.assertEqual(signature.qr_code_type_name, "Aztec")
        self.assertIn("QRCodeSignatureData", signature.signature_type)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
