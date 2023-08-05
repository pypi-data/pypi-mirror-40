# coding: utf-8
# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="test_sign_stamp.py">
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
from groupdocs_signature_cloud.models.requests.post_stamp_request import PostStampRequest
from groupdocs_signature_cloud.models.requests.post_stamp_from_url_request import PostStampFromUrlRequest
from groupdocs_signature_cloud.models.requests.post_collection_request import PostCollectionRequest
from groupdocs_signature_cloud.models.requests.post_collection_from_url_request import PostCollectionFromUrlRequest
from groupdocs_signature_cloud.models import *

class TestsSignStamp(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("\nSign Stamp")
        cls.BaseTest = BaseApiTest(fileStorage="Signature-Dev")
        cls.assertNotEqual(cls, cls.BaseTest.SignatureApi.api_client.configuration.access_token, "")
            
    def test_signature_post_stamp_cells_collection(self):

        collection = SignOptionsCollectionData()
        options1 = self.get_options_sign_stamp_cells()
        options2 = self.get_options_sign_stamp_cells()
        options2.inner_lines[0].text = "Smith John"
        options2.top = 10
        collection._items = [options1, options2]

        file = self.BaseTest.TestFiles.getFileSignedCells()

        request = PostCollectionRequest(file.fileName, collection, file.password, file.folder, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_collection(request)
        self.assert_response(file, response) 
    
    def test_signature_post_stamp_cells_collection_url(self):

        collection = SignOptionsCollectionData()
        options1 = self.get_options_sign_stamp_cells()
        options2 = self.get_options_sign_stamp_cells()
        options2.inner_lines[0].text  = "Smith John"
        options2.top = 10
        collection._items = [options1, options2]

        file = self.BaseTest.TestFiles.getFileSignedCellsUrl()

        request = PostCollectionFromUrlRequest(file.url, collection, file.password, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_collection_from_url(request)
        self.assert_response(file, response)           

    def test_signature_post_stamp_cells(self):
        file = self.BaseTest.TestFiles.getFile01PagesCells()
        options = self.get_options_sign_stamp_cells()
        request = PostStampRequest(file.fileName, options, file.password, file.folder, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_stamp(request)
        self.assert_response(file, response) 

    def test_signature_post_stamp_cells_url(self):
        file = self.BaseTest.TestFiles.getFile01PagesCellsUrl()
        options = self.get_options_sign_stamp_cells()
        request = PostStampFromUrlRequest(file.url, options, file.password, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_stamp_from_url(request)
        self.assert_response(file, response)
    
    def get_options_sign_stamp_cells(self):
        options = CellsSignStampOptionsData(1, 1, 1)
        self.compose_stamp_sign_optionsData(options)
        options.top = 5 
        options.left = 5 
        return options

    def test_signature_post_stamp_docimages(self):
        file = self.BaseTest.TestFiles.getFile01PagesDocImages()
        options = self.get_options_sign_stamp_docimages()
        request = PostStampRequest(file.fileName, options, file.password, file.folder, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_stamp(request)
        self.assert_response(file, response)

    def test_signature_post_stamp_docimages_url(self):
        file = self.BaseTest.TestFiles.getFile01PagesDocImagesUrl()
        options = self.get_options_sign_stamp_docimages()
        request = PostStampFromUrlRequest(file.url, options, file.password, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_stamp_from_url(request)
        self.assert_response(file, response)    

    def get_options_sign_stamp_docimages(self):
        options = ImagesSignStampOptionsData()
        self.compose_stamp_sign_optionsData(options)
        return options

    def test_signature_post_stamp_pdf(self):
        file = self.BaseTest.TestFiles.getFile01PagesPdf()
        options = self.get_options_sign_stamp_pdf()
        request = PostStampRequest(file.fileName, options, file.password, file.folder, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_stamp(request)
        self.assert_response(file, response)

    def test_signature_post_stamp_pdf_url(self):
        file = self.BaseTest.TestFiles.getFile01PagesPdfUrl()
        options = self.get_options_sign_stamp_pdf()
        request = PostStampFromUrlRequest(file.url, options, file.password, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_stamp_from_url(request)
        self.assert_response(file, response)          

    def get_options_sign_stamp_pdf(self):
        options = PdfSignStampOptionsData()
        self.compose_stamp_sign_optionsData(options)
        return options

    def test_signature_post_stamp_slides(self):
        file = self.BaseTest.TestFiles.getFile01PagesSlides()
        options = self.get_options_sign_stamp_slides()
        request = PostStampRequest(file.fileName, options, file.password, file.folder, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_stamp(request)
        self.assert_response(file, response)

    def test_signature_post_stamp_slides_url(self):
        file = self.BaseTest.TestFiles.getFile01PageSlidesUrl()
        options = self.get_options_sign_stamp_slides()
        request = PostStampFromUrlRequest(file.url, options, file.password, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_stamp_from_url(request)
        self.assert_response(file, response)    

    def get_options_sign_stamp_slides(self):
        options = SlidesSignStampOptionsData()
        self.compose_stamp_sign_optionsData(options)
        return options

    def test_signature_post_stamp_words(self):
        file = self.BaseTest.TestFiles.getFile01PagesWords()
        options = self.get_options_sign_stamp_words()
        request = PostStampRequest(file.fileName, options, file.password, file.folder, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_stamp(request)
        self.assert_response(file, response)

    def test_signature_post_stamp_words_url(self):
        file = self.BaseTest.TestFiles.getFile01PagesWordsUrl()
        options = self.get_options_sign_stamp_words()
        request = PostStampFromUrlRequest(file.url, options, file.password, self.BaseTest.FileStorage)
        response = self.BaseTest.SignatureApi.post_stamp_from_url(request)
        self.assert_response(file, response)  

    def get_options_sign_stamp_words(self):
        options = WordsSignStampOptionsData()
        self.compose_stamp_sign_optionsData(options)
        return options

    def compose_stamp_sign_optionsData(self, options):

        # get colors
        clrGold = self.BaseTest.get_color("#FFD700")
        clrBlueViolet = self.BaseTest.get_color("#8A2BE2")
        clrCornflowerBlue = self.BaseTest.get_color("#6495ED")
        clrDarkOrange = self.BaseTest.get_color("#FF8C00")
        clrOliveDrab = self.BaseTest.get_color("#6B8E23")
        clrGhostWhite = self.BaseTest.get_color("#F8F8FF")

        # outer line
        outerLine = StampLineData()
        outerLine.text = "John Smith"
        outerLine.font = self.BaseTest.get_font("Arial", 12, True, False, False)
        outerLine.text_bottom_intent = 5
        outerLine.text_color = clrGold
        outerLine.text_repeat_type = "FullTextRepeat"
        outerLine.background_color = clrBlueViolet
        outerLine.height = 20
        outerLineInnerBorder = BorderLineData(color = clrDarkOrange, style = "LongDash", transparency = 0.5, weight = 1.2)
        outerLine.inner_border = outerLineInnerBorder
        outerLineOuterBorder = BorderLineData(color = clrDarkOrange, style = "LongDashDot", transparency = 0.7, weight = 1.4)
        outerLine.outer_border = outerLineOuterBorder
        outerLine.visible = True        

        options.outer_lines = [outerLine]

        # inner line
        innerLine = StampLineData()
        innerLine.text = "John Smith"
        innerLine.font = self.BaseTest.get_font("Times New Roman", 20, True, True, True)
        innerLine.text_bottom_intent = 3
        innerLine.text_color = clrGold
        innerLine.text_repeat_type = "None"
        innerLine.background_color = clrCornflowerBlue
        innerLine.height = 30
        innerLineInnerBorder = BorderLineData(color = clrOliveDrab, style = "LongDash", transparency = 0.5, weight = 1.2)
        innerLine.inner_border = innerLineInnerBorder
        innerLineOuterBorder = BorderLineData(color = clrGhostWhite, style = "Dot", transparency = 0.4, weight = 1.4)
        innerLine.outer_border = innerLineOuterBorder
        innerLine.visible = True     
        
        options.inner_lines = [innerLine]

        options.image_guid = "images\\JohnSmithSign.png"
        # set position on page
        options.width = 300
        options.height = 200
        options.location_measure_type = "Pixels"
        options.size_measure_type = "Pixels"
        options.stretch = "None"
        options.rotation_angle = 0
        options.horizontal_alignment = "Left"
        options.vertical_alignment = "Top"
        # set margin
        margin = PaddingData(all = 100)        
        options.margin = margin
        options.margin_measure_type = "Pixels"
        # set background 
        options.background_color = clrCornflowerBlue
        options.background_color_crop_type = "InnerArea"
        options.background_image_crop_type = "MiddleArea"        
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
