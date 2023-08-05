# coding: utf-8
# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="test_sign_barcode.py">
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
from groupdocs_signature_cloud.models.requests.post_barcode_request import PostBarcodeRequest
from groupdocs_signature_cloud.models.requests.post_barcode_from_url_request import PostBarcodeFromUrlRequest
from groupdocs_signature_cloud.models.requests.post_collection_request import PostCollectionRequest
from groupdocs_signature_cloud.models.requests.post_collection_from_url_request import PostCollectionFromUrlRequest
from groupdocs_signature_cloud.models import *

class TestsSignBarcode(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\nSign Barcode")
        cls.BaseTest = BaseApiTest(fileStorage="Signature-Dev")
        cls.assertNotEqual(cls, cls.BaseTest.SignatureApi.api_client.configuration.access_token, "")

    def test_signature_post_barcode_cells_collection(self):

        collection = SignOptionsCollectionData()
        options1 = self.get_options_sign_barcode_cells()
        options2 = self.get_options_sign_barcode_cells()
        options2.text = "87654321"
        options2.top = 10
        collection._items = [options1, options2]

        file = self.BaseTest.TestFiles.getFileSignedCells()

        request = PostCollectionRequest(file.fileName, collection, file.password, file.folder, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_collection(request)
        self.assert_response(file, response) 
    
    def test_signature_post_barcode_cells_collection_url(self):

        collection = SignOptionsCollectionData()
        options1 = self.get_options_sign_barcode_cells()
        options2 = self.get_options_sign_barcode_cells()
        options2.text = "87654321"
        options2.top = 10
        collection._items = [options1, options2]

        file = self.BaseTest.TestFiles.getFileSignedCellsUrl()

        request = PostCollectionFromUrlRequest(file.url, collection, file.password, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_collection_from_url(request)
        self.assert_response(file, response)              

    def test_signature_post_barcode_cells(self):
        file = self.BaseTest.TestFiles.getFile01PagesCells()
        options = self.get_options_sign_barcode_cells()
        request = PostBarcodeRequest(file.fileName, options, file.password, file.folder, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_barcode(request)
        self.assert_response(file, response) 
    
    def test_signature_post_barcode_cells_url(self):
        file = self.BaseTest.TestFiles.getFile01PagesCellsUrl()
        options = self.get_options_sign_barcode_cells()
        request = PostBarcodeFromUrlRequest(file.url, options, file.password, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_barcode_from_url(request)
        self.assert_response(file, response)
    
    def get_options_sign_barcode_cells(self):
        options = CellsSignBarcodeOptionsData(1, 1, 1)
        self.compose_barcode_sign_optionsData(options)
        options.top = 5 
        options.left = 5           
        return options
    
    def test_signature_post_barcode_docimages(self):
        file = self.BaseTest.TestFiles.getFile01PagesDocImages()
        options = self.get_options_sign_barcode_docimages()
        request = PostBarcodeRequest(file.fileName, options, file.password, file.folder, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_barcode(request)
        self.assert_response(file, response)

    def test_signature_post_barcode_docimages_url(self):
        file = self.BaseTest.TestFiles.getFile01PagesDocImagesUrl()
        options = self.get_options_sign_barcode_docimages()
        request = PostBarcodeFromUrlRequest(file.url, options, file.password, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_barcode_from_url(request)
        self.assert_response(file, response)    

    def get_options_sign_barcode_docimages(self):
        options = ImagesSignBarcodeOptionsData()
        self.compose_barcode_sign_optionsData(options)
        return options

    def test_signature_post_barcode_pdf(self):
        file = self.BaseTest.TestFiles.getFile01PagesPdf()
        options = self.get_options_sign_barcode_pdf()
        request = PostBarcodeRequest(file.fileName, options, file.password, file.folder, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_barcode(request)
        self.assert_response(file, response)

    def test_signature_post_barcode_pdf_url(self):
        file = self.BaseTest.TestFiles.getFile01PagesPdfUrl()
        options = self.get_options_sign_barcode_pdf()
        request = PostBarcodeFromUrlRequest(file.url, options, file.password, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_barcode_from_url(request)
        self.assert_response(file, response)          

    def get_options_sign_barcode_pdf(self):
        options = PdfSignBarcodeOptionsData()
        self.compose_barcode_sign_optionsData(options)
        return options

    def test_signature_post_barcode_slides(self):
        file = self.BaseTest.TestFiles.getFile01PagesSlides()
        options = self.get_options_sign_barcode_slides()
        request = PostBarcodeRequest(file.fileName, options, file.password, file.folder, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_barcode(request)
        self.assert_response(file, response)

    def test_signature_post_barcode_slides_url(self):
        file = self.BaseTest.TestFiles.getFile01PageSlidesUrl()
        options = self.get_options_sign_barcode_slides()
        request = PostBarcodeFromUrlRequest(file.url, options, file.password, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_barcode_from_url(request)
        self.assert_response(file, response)    

    def get_options_sign_barcode_slides(self):
        options = SlidesSignBarcodeOptionsData()
        self.compose_barcode_sign_optionsData(options)
        return options

    def test_signature_post_barcode_words(self):
        file = self.BaseTest.TestFiles.getFile01PagesWords()
        options = self.get_options_sign_barcode_words()
        request = PostBarcodeRequest(file.fileName, options, file.password, file.folder, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_barcode(request)
        self.assert_response(file, response)

    def test_signature_post_barcode_words_url(self):
        file = self.BaseTest.TestFiles.getFile01PagesWordsUrl()
        options = self.get_options_sign_barcode_words()
        request = PostBarcodeFromUrlRequest(file.url, options, file.password, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_barcode_from_url(request)
        self.assert_response(file, response)  

    def get_options_sign_barcode_words(self):
        options = WordsSignBarcodeOptionsData()
        self.compose_barcode_sign_optionsData(options)
        return options
    
    def compose_barcode_sign_optionsData(self, options):
        # set barcode properties
        options.barcode_type_name ="Code128"
        options.text = "12345678"
        # set position on page
        options.left = 100
        options.top = 100
        options.width = 300
        options.height = 100
        options.location_measure_type = "Pixels"
        options.size_measure_type = "Pixels"
        options.stretch = "None"
        options.rotation_angle = 45
        options.horizontal_alignment = "None"
        options.vertical_alignment = "None"
        # set margin
        margin = PaddingData(all = 100)        
        options.margin = margin
        options.margin_measure_type = "Pixels"
        #set border    
        options.border_dash_style = "DashLongDashDot"
        options.border_weight = 1
        options.opacity = 1
        options.border_visiblity = True
        # set colors
        clrFore = self.BaseTest.get_color("#ff0000")
        options.fore_color = clrFore
        clrBoard = self.BaseTest.get_color("#121212")
        options.border_color = clrBoard
        clrBack = self.BaseTest.get_color("#ffaaaa")
        options.background_color = clrBack
        #set pages for signing
        options.sign_all_pages = False
        options.document_page_number = 1
        pagesSetup = PagesSetupData(True, False, False, False)        
        options.pages_setup = pagesSetup         

    def assert_response(self, file, response):
    
        self.assertNotEqual(response, False)
        self.assertEqual(response.code, "200")
        self.assertEqual(response.status, "OK")
        self.assertEqual(file.fileName, file.fileName)
        self.assertEqual(response.folder, "Output")

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
