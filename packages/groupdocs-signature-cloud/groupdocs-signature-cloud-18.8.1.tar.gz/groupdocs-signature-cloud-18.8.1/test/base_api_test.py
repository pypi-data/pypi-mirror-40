# coding: utf-8
# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="BaseApiTest.py">
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
import os
import json 
import asposestoragecloud
from groupdocs_signature_cloud.configuration import Configuration
from groupdocs_signature_cloud.apis.signature_api import SignatureApi
from groupdocs_signature_cloud.models.color import Color
from groupdocs_signature_cloud.models.signature_font_data import SignatureFontData
from internal.test_file import TestFile
from internal.test_files import TestFiles

class BaseApiTest():

    def __init__(self, fileStorage):

        self.FileStorage = fileStorage
        self.ConfigPath = os.path.dirname(os.path.abspath(__file__)) +"\\internal\\config.json"
        self.TestDataPath = os.path.dirname(os.path.abspath(__file__)) +"\\internal\\test_data"
        self.TestFiles = TestFiles()

        self.getConfig()
        self.SignatureApi = SignatureApi(configuration=self.Configuration)
        self.SkipFilesUploading = self.Configuration.skip_files_uploading
        self.UploadOnlyMissingFiles = self.Configuration.upload_only_missing_files

        # Storage Api initialization
        storageConfiguration = asposestoragecloud.Configuration()
        storageConfiguration.host = self.Configuration.host
        storageConfiguration.base_url = self.Configuration.base_url
        storageConfiguration.api_key_prefix = "Bearer"
        
        storageApiClient = asposestoragecloud.ApiClient(apiKey=str(self.Configuration.api_key["api_key"]), 
         appSid=str(self.Configuration.api_key["app_sid"]), configuration = storageConfiguration)
        
        self.StorageApi = asposestoragecloud.apis.StorageApi(storageApiClient)

        # Test files uploading
        if not self.SkipFilesUploading:
            self.TestFilesUploaded = True 
            self.uploadTestFiles()

    def getConfig(self):

        fileConfig = open(self.ConfigPath, "r")
        config = json.loads(fileConfig.read())
        fileConfig.close()

        self.Configuration = Configuration()
        self.Configuration.host = config["ApiHost"]
        self.Configuration.base_url = config["ApiBaseUrl"]
        self.Configuration.api_key["api_key"] = config["AppKey"]
        self.Configuration.api_key["app_sid"] = config["AppSID"]
        self.Configuration.skip_files_uploading = config["SkipFilesUploading"]
        self.Configuration.upload_only_missing_files = config["UploadOnlyMissingFiles"]

    def uploadTestFiles(self):
    
        if self.TestFilesUploaded:
            return True

        storageExistsResponse = self.StorageApi.get_is_storage_exist_with_http_info(self.FileStorage, _preload_content=False)
        if self.is_folder_exists(storageExistsResponse) != True:
            return False

        #Storage folder
        for curFile in self.TestFiles.getAllStorageFiles():
            self.upload_file(curFile)
        
        #Images folder
        for curFile in self.TestFiles.getAllImagesFiles():
            self.upload_file(curFile)               

        #Certificates folder
        for curFile in self.TestFiles.getAllCertificatesFiles():
            self.upload_file(curFile)

        #Signed folder
        for curFile in self.TestFiles.getAllSignedFiles():
            self.upload_file(curFile)  

        self.TestFilesUploaded = True                             
        
    def is_folder_exists(self, response):
 
        if response[1] != 200:
            return False
        responseData = json.loads(response[0].data)
        if responseData["isExist"] != True:
            return False
        return True

    def is_file_exists(self, response):
 
        responseData = json.loads(response.data)
        if responseData["code"] == 200 and responseData["fileExist"]["isExist"] == True:
            return True
        return False    

    def upload_file(self, file):

        storagePath = file.getStoragePath()
        # skip existing file uploading
        if self.UploadOnlyMissingFiles:
            fileExistsResponse = self.StorageApi.get_is_exist(storagePath, storage = self.FileStorage, _preload_content=False)
            if self.is_file_exists(fileExistsResponse) == True:
                return False
        # file stream uploading
        filePath = file.getPath(self.TestDataPath)
        filestream = open(file = filePath, mode = "rb")
        self.StorageApi.put_create(path = storagePath, file = filestream, storage = self.FileStorage)      
        filestream.close()    
        print("Uploaded: " + storagePath)     

    def get_color(self, web):

        color = Color(web)
        return color
    
    def get_font(self, name, size, bold, italic, underline):

        font = SignatureFontData(name, size, bold, italic, underline)
        return font


