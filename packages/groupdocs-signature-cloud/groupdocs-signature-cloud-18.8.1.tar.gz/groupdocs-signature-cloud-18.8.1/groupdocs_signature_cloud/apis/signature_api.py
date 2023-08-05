# coding: utf-8

# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="SignatureApi.py">
#   Copyright (c) 2018 2003-2018 Aspose Pty Ltd
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


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six
from groupdocs_signature_cloud.rest import ApiException
from groupdocs_signature_cloud.api_client import ApiClient


class SignatureApi(object):
    """
    GroupDocs Signature for Cloud API

    :param api_client: an api client to perfom http requests
    """
    def __init__(self, api_client=None, configuration=None):
	
        if api_client is None:
            api_client = ApiClient(configuration)
        self.api_client = api_client
		
        self.__request_token()

    def get_barcodes(self, request, **kwargs):  # noqa: E501
        """Retrieves list of supported Barcode type names.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :return: BarcodeCollection
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.get_barcodes_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.get_barcodes_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.__refresh_token()
                raise ApiException('Access token has expired. Token has been refreshed, please run request again.')
        
    def get_barcodes_with_http_info(self, request, **kwargs):  # noqa: E501
        """Retrieves list of supported Barcode type names.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param GetBarcodesRequest request object with parameters
        :return: BarcodeCollection
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_barcodes" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}
        path = '/signature/barcodes'
        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth']  # noqa: E501

        return self.api_client.call_api(
            path, 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='BarcodeCollection',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_document_info(self, request, **kwargs):  # noqa: E501
        """Retrieves document information.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param str file_name: The file name. (required)
        :param str password: The document password.
        :param str folder: The folder name.
        :param str storage: The file storage which have to be used.
        :return: DocumentInfo
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.get_document_info_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.get_document_info_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.__refresh_token()
                raise ApiException('Access token has expired. Token has been refreshed, please run request again.')
        
    def get_document_info_with_http_info(self, request, **kwargs):  # noqa: E501
        """Retrieves document information.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param GetDocumentInfoRequest request object with parameters
        :return: DocumentInfo
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_document_info" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'file_name' is set
        if request.file_name is None:
            raise ValueError("Missing the required parameter `file_name` when calling `get_document_info`")  # noqa: E501

        collection_formats = {}
        path = '/signature/{fileName}/document/info'
        path_params = {}
        if request.file_name is not None:
            path_params[self.__downcase_first_letter('FileName')] = request.file_name  # noqa: E501

        query_params = []
        if self.__downcase_first_letter('Password') in path:
            path = path.replace('{' + self.__downcase_first_letter('Password' + '}'), request.password if request.password is not None else '')
        else:
            if request.password is not None:
                query_params.append((self.__downcase_first_letter('Password'), request.password))  # noqa: E501
        if self.__downcase_first_letter('Folder') in path:
            path = path.replace('{' + self.__downcase_first_letter('Folder' + '}'), request.folder if request.folder is not None else '')
        else:
            if request.folder is not None:
                query_params.append((self.__downcase_first_letter('Folder'), request.folder))  # noqa: E501
        if self.__downcase_first_letter('Storage') in path:
            path = path.replace('{' + self.__downcase_first_letter('Storage' + '}'), request.storage if request.storage is not None else '')
        else:
            if request.storage is not None:
                query_params.append((self.__downcase_first_letter('Storage'), request.storage))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth']  # noqa: E501

        return self.api_client.call_api(
            path, 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='DocumentInfo',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_document_info_from_url(self, request, **kwargs):  # noqa: E501
        """Retrieves document information for document at provided URL. Retrieves file from specified URL and tries to detect file type when fileName parameter is not specified. Saves retrieved file in storage. Use fileName and folder parameters to specify desired file name and folder to save file. When file with specified name already exists in storage new unique file name will be used for file.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param str url: The URL to retrieve document. (required)
        :param str password: The document password.
        :param str storage: The file storage which have to be used.
        :return: DocumentInfo
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.get_document_info_from_url_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.get_document_info_from_url_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.__refresh_token()
                raise ApiException('Access token has expired. Token has been refreshed, please run request again.')
        
    def get_document_info_from_url_with_http_info(self, request, **kwargs):  # noqa: E501
        """Retrieves document information for document at provided URL. Retrieves file from specified URL and tries to detect file type when fileName parameter is not specified. Saves retrieved file in storage. Use fileName and folder parameters to specify desired file name and folder to save file. When file with specified name already exists in storage new unique file name will be used for file.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param GetDocumentInfoFromUrlRequest request object with parameters
        :return: DocumentInfo
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_document_info_from_url" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'url' is set
        if request.url is None:
            raise ValueError("Missing the required parameter `url` when calling `get_document_info_from_url`")  # noqa: E501

        collection_formats = {}
        path = '/signature/document/info'
        path_params = {}

        query_params = []
        if self.__downcase_first_letter('Url') in path:
            path = path.replace('{' + self.__downcase_first_letter('Url' + '}'), request.url if request.url is not None else '')
        else:
            if request.url is not None:
                query_params.append((self.__downcase_first_letter('Url'), request.url))  # noqa: E501
        if self.__downcase_first_letter('Password') in path:
            path = path.replace('{' + self.__downcase_first_letter('Password' + '}'), request.password if request.password is not None else '')
        else:
            if request.password is not None:
                query_params.append((self.__downcase_first_letter('Password'), request.password))  # noqa: E501
        if self.__downcase_first_letter('Storage') in path:
            path = path.replace('{' + self.__downcase_first_letter('Storage' + '}'), request.storage if request.storage is not None else '')
        else:
            if request.storage is not None:
                query_params.append((self.__downcase_first_letter('Storage'), request.storage))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth']  # noqa: E501

        return self.api_client.call_api(
            path, 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='DocumentInfo',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_qr_codes(self, request, **kwargs):  # noqa: E501
        """Retrieves list of supported QR-Code type names.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :return: QRCodeCollection
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.get_qr_codes_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.get_qr_codes_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.__refresh_token()
                raise ApiException('Access token has expired. Token has been refreshed, please run request again.')
        
    def get_qr_codes_with_http_info(self, request, **kwargs):  # noqa: E501
        """Retrieves list of supported QR-Code type names.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param GetQrCodesRequest request object with parameters
        :return: QRCodeCollection
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_qr_codes" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}
        path = '/signature/qrcodes'
        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth']  # noqa: E501

        return self.api_client.call_api(
            path, 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='QRCodeCollection',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_supported_formats(self, request, **kwargs):  # noqa: E501
        """Lists supported file formats.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :return: FormatCollection
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.get_supported_formats_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.get_supported_formats_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.__refresh_token()
                raise ApiException('Access token has expired. Token has been refreshed, please run request again.')
        
    def get_supported_formats_with_http_info(self, request, **kwargs):  # noqa: E501
        """Lists supported file formats.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param GetSupportedFormatsRequest request object with parameters
        :return: FormatCollection
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_supported_formats" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}
        path = '/signature/formats'
        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth']  # noqa: E501

        return self.api_client.call_api(
            path, 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='FormatCollection',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_barcode(self, request, **kwargs):  # noqa: E501
        """Insert Barcode Signature into the Document  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param str name: The Document name. (required)
        :param SignOptionsData sign_options_data: Barcode Signature Options for corresponding Document Type
        :param str password: Document password if required.
        :param str folder: The folder name.
        :param str storage: The file storage which have to be used.
        :return: SignatureDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.post_barcode_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.post_barcode_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.__refresh_token()
                raise ApiException('Access token has expired. Token has been refreshed, please run request again.')
        
    def post_barcode_with_http_info(self, request, **kwargs):  # noqa: E501
        """Insert Barcode Signature into the Document  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param PostBarcodeRequest request object with parameters
        :return: SignatureDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_barcode" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if request.name is None:
            raise ValueError("Missing the required parameter `name` when calling `post_barcode`")  # noqa: E501

        collection_formats = {}
        path = '/signature/{name}/barcode'
        path_params = {}
        if request.name is not None:
            path_params[self.__downcase_first_letter('Name')] = request.name  # noqa: E501

        query_params = []
        if self.__downcase_first_letter('Password') in path:
            path = path.replace('{' + self.__downcase_first_letter('Password' + '}'), request.password if request.password is not None else '')
        else:
            if request.password is not None:
                query_params.append((self.__downcase_first_letter('Password'), request.password))  # noqa: E501
        if self.__downcase_first_letter('Folder') in path:
            path = path.replace('{' + self.__downcase_first_letter('Folder' + '}'), request.folder if request.folder is not None else '')
        else:
            if request.folder is not None:
                query_params.append((self.__downcase_first_letter('Folder'), request.folder))  # noqa: E501
        if self.__downcase_first_letter('Storage') in path:
            path = path.replace('{' + self.__downcase_first_letter('Storage' + '}'), request.storage if request.storage is not None else '')
        else:
            if request.storage is not None:
                query_params.append((self.__downcase_first_letter('Storage'), request.storage))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        if request.sign_options_data is not None:
            body_params = request.sign_options_data
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth']  # noqa: E501

        return self.api_client.call_api(
            path, 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SignatureDocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_barcode_from_url(self, request, **kwargs):  # noqa: E501
        """Insert Barcode Signature into the Document provided by URL  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param str url: The URL to retrieve document. (required)
        :param SignOptionsData sign_options_data: Barcode Signature Options for corresponding Document Type
        :param str password: Document password if required.
        :param str storage: The file storage which have to be used.
        :return: SignatureDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.post_barcode_from_url_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.post_barcode_from_url_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.__refresh_token()
                raise ApiException('Access token has expired. Token has been refreshed, please run request again.')
        
    def post_barcode_from_url_with_http_info(self, request, **kwargs):  # noqa: E501
        """Insert Barcode Signature into the Document provided by URL  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param PostBarcodeFromUrlRequest request object with parameters
        :return: SignatureDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_barcode_from_url" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'url' is set
        if request.url is None:
            raise ValueError("Missing the required parameter `url` when calling `post_barcode_from_url`")  # noqa: E501

        collection_formats = {}
        path = '/signature/barcode'
        path_params = {}

        query_params = []
        if self.__downcase_first_letter('Url') in path:
            path = path.replace('{' + self.__downcase_first_letter('Url' + '}'), request.url if request.url is not None else '')
        else:
            if request.url is not None:
                query_params.append((self.__downcase_first_letter('Url'), request.url))  # noqa: E501
        if self.__downcase_first_letter('Password') in path:
            path = path.replace('{' + self.__downcase_first_letter('Password' + '}'), request.password if request.password is not None else '')
        else:
            if request.password is not None:
                query_params.append((self.__downcase_first_letter('Password'), request.password))  # noqa: E501
        if self.__downcase_first_letter('Storage') in path:
            path = path.replace('{' + self.__downcase_first_letter('Storage' + '}'), request.storage if request.storage is not None else '')
        else:
            if request.storage is not None:
                query_params.append((self.__downcase_first_letter('Storage'), request.storage))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        if request.sign_options_data is not None:
            body_params = request.sign_options_data
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth']  # noqa: E501

        return self.api_client.call_api(
            path, 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SignatureDocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_collection(self, request, **kwargs):  # noqa: E501
        """Insert Signature into the Document  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param str name: The Document name. (required)
        :param SignOptionsCollectionData sign_options_collection_data: Signature Options Collection for corresponding Document Type
        :param str password: Document password if required.
        :param str folder: The folder name.
        :param str storage: The file storage which have to be used.
        :return: SignatureDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.post_collection_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.post_collection_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.__refresh_token()
                raise ApiException('Access token has expired. Token has been refreshed, please run request again.')
        
    def post_collection_with_http_info(self, request, **kwargs):  # noqa: E501
        """Insert Signature into the Document  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param PostCollectionRequest request object with parameters
        :return: SignatureDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_collection" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if request.name is None:
            raise ValueError("Missing the required parameter `name` when calling `post_collection`")  # noqa: E501

        collection_formats = {}
        path = '/signature/{name}/collection'
        path_params = {}
        if request.name is not None:
            path_params[self.__downcase_first_letter('Name')] = request.name  # noqa: E501

        query_params = []
        if self.__downcase_first_letter('Password') in path:
            path = path.replace('{' + self.__downcase_first_letter('Password' + '}'), request.password if request.password is not None else '')
        else:
            if request.password is not None:
                query_params.append((self.__downcase_first_letter('Password'), request.password))  # noqa: E501
        if self.__downcase_first_letter('Folder') in path:
            path = path.replace('{' + self.__downcase_first_letter('Folder' + '}'), request.folder if request.folder is not None else '')
        else:
            if request.folder is not None:
                query_params.append((self.__downcase_first_letter('Folder'), request.folder))  # noqa: E501
        if self.__downcase_first_letter('Storage') in path:
            path = path.replace('{' + self.__downcase_first_letter('Storage' + '}'), request.storage if request.storage is not None else '')
        else:
            if request.storage is not None:
                query_params.append((self.__downcase_first_letter('Storage'), request.storage))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        if request.sign_options_collection_data is not None:
            body_params = request.sign_options_collection_data
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth']  # noqa: E501

        return self.api_client.call_api(
            path, 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SignatureDocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_collection_from_url(self, request, **kwargs):  # noqa: E501
        """Insert Stamp Signature into the Document provided by URL  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param str url: The URL to retrieve document. (required)
        :param SignOptionsCollectionData sign_options_collection_data: Signature Options Collection for corresponding Document Type
        :param str password: Document password if required.
        :param str storage: The file storage which have to be used.
        :return: SignatureDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.post_collection_from_url_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.post_collection_from_url_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.__refresh_token()
                raise ApiException('Access token has expired. Token has been refreshed, please run request again.')
        
    def post_collection_from_url_with_http_info(self, request, **kwargs):  # noqa: E501
        """Insert Stamp Signature into the Document provided by URL  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param PostCollectionFromUrlRequest request object with parameters
        :return: SignatureDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_collection_from_url" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'url' is set
        if request.url is None:
            raise ValueError("Missing the required parameter `url` when calling `post_collection_from_url`")  # noqa: E501

        collection_formats = {}
        path = '/signature/collection'
        path_params = {}

        query_params = []
        if self.__downcase_first_letter('Url') in path:
            path = path.replace('{' + self.__downcase_first_letter('Url' + '}'), request.url if request.url is not None else '')
        else:
            if request.url is not None:
                query_params.append((self.__downcase_first_letter('Url'), request.url))  # noqa: E501
        if self.__downcase_first_letter('Password') in path:
            path = path.replace('{' + self.__downcase_first_letter('Password' + '}'), request.password if request.password is not None else '')
        else:
            if request.password is not None:
                query_params.append((self.__downcase_first_letter('Password'), request.password))  # noqa: E501
        if self.__downcase_first_letter('Storage') in path:
            path = path.replace('{' + self.__downcase_first_letter('Storage' + '}'), request.storage if request.storage is not None else '')
        else:
            if request.storage is not None:
                query_params.append((self.__downcase_first_letter('Storage'), request.storage))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        if request.sign_options_collection_data is not None:
            body_params = request.sign_options_collection_data
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth']  # noqa: E501

        return self.api_client.call_api(
            path, 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SignatureDocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_digital(self, request, **kwargs):  # noqa: E501
        """Insert Digital Signature into the Document  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param str name: The document name (required)
        :param SignOptionsData sign_options_data: Digital Signature Options for corresponding Document Type
        :param str password: Document password if required.
        :param str folder: The folder name
        :param str certificate_file: Digital certificate file name.
        :param str image_file: Image file.
        :param str storage: The file storage which have to be used.
        :return: SignatureDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.post_digital_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.post_digital_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.__refresh_token()
                raise ApiException('Access token has expired. Token has been refreshed, please run request again.')
        
    def post_digital_with_http_info(self, request, **kwargs):  # noqa: E501
        """Insert Digital Signature into the Document  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param PostDigitalRequest request object with parameters
        :return: SignatureDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_digital" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if request.name is None:
            raise ValueError("Missing the required parameter `name` when calling `post_digital`")  # noqa: E501

        collection_formats = {}
        path = '/signature/{name}/digital'
        path_params = {}
        if request.name is not None:
            path_params[self.__downcase_first_letter('Name')] = request.name  # noqa: E501

        query_params = []
        if self.__downcase_first_letter('Password') in path:
            path = path.replace('{' + self.__downcase_first_letter('Password' + '}'), request.password if request.password is not None else '')
        else:
            if request.password is not None:
                query_params.append((self.__downcase_first_letter('Password'), request.password))  # noqa: E501
        if self.__downcase_first_letter('Folder') in path:
            path = path.replace('{' + self.__downcase_first_letter('Folder' + '}'), request.folder if request.folder is not None else '')
        else:
            if request.folder is not None:
                query_params.append((self.__downcase_first_letter('Folder'), request.folder))  # noqa: E501
        if self.__downcase_first_letter('CertificateFile') in path:
            path = path.replace('{' + self.__downcase_first_letter('CertificateFile' + '}'), request.certificate_file if request.certificate_file is not None else '')
        else:
            if request.certificate_file is not None:
                query_params.append((self.__downcase_first_letter('CertificateFile'), request.certificate_file))  # noqa: E501
        if self.__downcase_first_letter('ImageFile') in path:
            path = path.replace('{' + self.__downcase_first_letter('ImageFile' + '}'), request.image_file if request.image_file is not None else '')
        else:
            if request.image_file is not None:
                query_params.append((self.__downcase_first_letter('ImageFile'), request.image_file))  # noqa: E501
        if self.__downcase_first_letter('Storage') in path:
            path = path.replace('{' + self.__downcase_first_letter('Storage' + '}'), request.storage if request.storage is not None else '')
        else:
            if request.storage is not None:
                query_params.append((self.__downcase_first_letter('Storage'), request.storage))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        if request.sign_options_data is not None:
            body_params = request.sign_options_data
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth']  # noqa: E501

        return self.api_client.call_api(
            path, 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SignatureDocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_digital_from_url(self, request, **kwargs):  # noqa: E501
        """Insert Digital Signature into the Document  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param str url: The URL to retrieve document. (required)
        :param SignOptionsData sign_options_data: Digital Signature Options for corresponding Document Type
        :param str password: Document password if required.
        :param str certificate_file: Digital certificate file name.
        :param str image_file: Image file.
        :param str storage: The file storage which have to be used.
        :return: SignatureDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.post_digital_from_url_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.post_digital_from_url_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.__refresh_token()
                raise ApiException('Access token has expired. Token has been refreshed, please run request again.')
        
    def post_digital_from_url_with_http_info(self, request, **kwargs):  # noqa: E501
        """Insert Digital Signature into the Document  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param PostDigitalFromUrlRequest request object with parameters
        :return: SignatureDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_digital_from_url" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'url' is set
        if request.url is None:
            raise ValueError("Missing the required parameter `url` when calling `post_digital_from_url`")  # noqa: E501

        collection_formats = {}
        path = '/signature/digital'
        path_params = {}

        query_params = []
        if self.__downcase_first_letter('Url') in path:
            path = path.replace('{' + self.__downcase_first_letter('Url' + '}'), request.url if request.url is not None else '')
        else:
            if request.url is not None:
                query_params.append((self.__downcase_first_letter('Url'), request.url))  # noqa: E501
        if self.__downcase_first_letter('Password') in path:
            path = path.replace('{' + self.__downcase_first_letter('Password' + '}'), request.password if request.password is not None else '')
        else:
            if request.password is not None:
                query_params.append((self.__downcase_first_letter('Password'), request.password))  # noqa: E501
        if self.__downcase_first_letter('CertificateFile') in path:
            path = path.replace('{' + self.__downcase_first_letter('CertificateFile' + '}'), request.certificate_file if request.certificate_file is not None else '')
        else:
            if request.certificate_file is not None:
                query_params.append((self.__downcase_first_letter('CertificateFile'), request.certificate_file))  # noqa: E501
        if self.__downcase_first_letter('ImageFile') in path:
            path = path.replace('{' + self.__downcase_first_letter('ImageFile' + '}'), request.image_file if request.image_file is not None else '')
        else:
            if request.image_file is not None:
                query_params.append((self.__downcase_first_letter('ImageFile'), request.image_file))  # noqa: E501
        if self.__downcase_first_letter('Storage') in path:
            path = path.replace('{' + self.__downcase_first_letter('Storage' + '}'), request.storage if request.storage is not None else '')
        else:
            if request.storage is not None:
                query_params.append((self.__downcase_first_letter('Storage'), request.storage))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        if request.sign_options_data is not None:
            body_params = request.sign_options_data
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth']  # noqa: E501

        return self.api_client.call_api(
            path, 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SignatureDocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_image(self, request, **kwargs):  # noqa: E501
        """Insert Image Signature into the Document  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param str name: The document name (required)
        :param SignOptionsData sign_options_data: Image Signature Options for corresponding Document Type
        :param str password: Document password if required.
        :param str folder: The folder name
        :param str image: The Image name
        :param str storage: The file storage which have to be used.
        :return: SignatureDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.post_image_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.post_image_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.__refresh_token()
                raise ApiException('Access token has expired. Token has been refreshed, please run request again.')
        
    def post_image_with_http_info(self, request, **kwargs):  # noqa: E501
        """Insert Image Signature into the Document  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param PostImageRequest request object with parameters
        :return: SignatureDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_image" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if request.name is None:
            raise ValueError("Missing the required parameter `name` when calling `post_image`")  # noqa: E501

        collection_formats = {}
        path = '/signature/{name}/image'
        path_params = {}
        if request.name is not None:
            path_params[self.__downcase_first_letter('Name')] = request.name  # noqa: E501

        query_params = []
        if self.__downcase_first_letter('Password') in path:
            path = path.replace('{' + self.__downcase_first_letter('Password' + '}'), request.password if request.password is not None else '')
        else:
            if request.password is not None:
                query_params.append((self.__downcase_first_letter('Password'), request.password))  # noqa: E501
        if self.__downcase_first_letter('Folder') in path:
            path = path.replace('{' + self.__downcase_first_letter('Folder' + '}'), request.folder if request.folder is not None else '')
        else:
            if request.folder is not None:
                query_params.append((self.__downcase_first_letter('Folder'), request.folder))  # noqa: E501
        if self.__downcase_first_letter('Image') in path:
            path = path.replace('{' + self.__downcase_first_letter('Image' + '}'), request.image if request.image is not None else '')
        else:
            if request.image is not None:
                query_params.append((self.__downcase_first_letter('Image'), request.image))  # noqa: E501
        if self.__downcase_first_letter('Storage') in path:
            path = path.replace('{' + self.__downcase_first_letter('Storage' + '}'), request.storage if request.storage is not None else '')
        else:
            if request.storage is not None:
                query_params.append((self.__downcase_first_letter('Storage'), request.storage))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        if request.sign_options_data is not None:
            body_params = request.sign_options_data
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth']  # noqa: E501

        return self.api_client.call_api(
            path, 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SignatureDocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_image_from_url(self, request, **kwargs):  # noqa: E501
        """Insert Image Signature into the Document provided by URL  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param str url: The URL to retrieve document. (required)
        :param SignOptionsData sign_options_data: Image Signature Options for corresponding Document Type
        :param str password: Document password if required.
        :param str image: The Image name
        :param str storage: The file storage which have to be used.
        :return: SignatureDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.post_image_from_url_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.post_image_from_url_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.__refresh_token()
                raise ApiException('Access token has expired. Token has been refreshed, please run request again.')
        
    def post_image_from_url_with_http_info(self, request, **kwargs):  # noqa: E501
        """Insert Image Signature into the Document provided by URL  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param PostImageFromUrlRequest request object with parameters
        :return: SignatureDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_image_from_url" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'url' is set
        if request.url is None:
            raise ValueError("Missing the required parameter `url` when calling `post_image_from_url`")  # noqa: E501

        collection_formats = {}
        path = '/signature/image'
        path_params = {}

        query_params = []
        if self.__downcase_first_letter('Url') in path:
            path = path.replace('{' + self.__downcase_first_letter('Url' + '}'), request.url if request.url is not None else '')
        else:
            if request.url is not None:
                query_params.append((self.__downcase_first_letter('Url'), request.url))  # noqa: E501
        if self.__downcase_first_letter('Password') in path:
            path = path.replace('{' + self.__downcase_first_letter('Password' + '}'), request.password if request.password is not None else '')
        else:
            if request.password is not None:
                query_params.append((self.__downcase_first_letter('Password'), request.password))  # noqa: E501
        if self.__downcase_first_letter('Image') in path:
            path = path.replace('{' + self.__downcase_first_letter('Image' + '}'), request.image if request.image is not None else '')
        else:
            if request.image is not None:
                query_params.append((self.__downcase_first_letter('Image'), request.image))  # noqa: E501
        if self.__downcase_first_letter('Storage') in path:
            path = path.replace('{' + self.__downcase_first_letter('Storage' + '}'), request.storage if request.storage is not None else '')
        else:
            if request.storage is not None:
                query_params.append((self.__downcase_first_letter('Storage'), request.storage))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        if request.sign_options_data is not None:
            body_params = request.sign_options_data
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth']  # noqa: E501

        return self.api_client.call_api(
            path, 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SignatureDocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_qr_code(self, request, **kwargs):  # noqa: E501
        """Insert QRCode Signature into the Document  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param str name: The Document name. (required)
        :param SignOptionsData sign_options_data: QR-Code Signature Options for corresponding Document Type
        :param str password: Document password if required.
        :param str folder: The folder name.
        :param str storage: The file storage which have to be used.
        :return: SignatureDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.post_qr_code_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.post_qr_code_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.__refresh_token()
                raise ApiException('Access token has expired. Token has been refreshed, please run request again.')
        
    def post_qr_code_with_http_info(self, request, **kwargs):  # noqa: E501
        """Insert QRCode Signature into the Document  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param PostQrCodeRequest request object with parameters
        :return: SignatureDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_qr_code" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if request.name is None:
            raise ValueError("Missing the required parameter `name` when calling `post_qr_code`")  # noqa: E501

        collection_formats = {}
        path = '/signature/{name}/qrcode'
        path_params = {}
        if request.name is not None:
            path_params[self.__downcase_first_letter('Name')] = request.name  # noqa: E501

        query_params = []
        if self.__downcase_first_letter('Password') in path:
            path = path.replace('{' + self.__downcase_first_letter('Password' + '}'), request.password if request.password is not None else '')
        else:
            if request.password is not None:
                query_params.append((self.__downcase_first_letter('Password'), request.password))  # noqa: E501
        if self.__downcase_first_letter('Folder') in path:
            path = path.replace('{' + self.__downcase_first_letter('Folder' + '}'), request.folder if request.folder is not None else '')
        else:
            if request.folder is not None:
                query_params.append((self.__downcase_first_letter('Folder'), request.folder))  # noqa: E501
        if self.__downcase_first_letter('Storage') in path:
            path = path.replace('{' + self.__downcase_first_letter('Storage' + '}'), request.storage if request.storage is not None else '')
        else:
            if request.storage is not None:
                query_params.append((self.__downcase_first_letter('Storage'), request.storage))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        if request.sign_options_data is not None:
            body_params = request.sign_options_data
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth']  # noqa: E501

        return self.api_client.call_api(
            path, 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SignatureDocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_qr_code_from_url(self, request, **kwargs):  # noqa: E501
        """Insert QRCode Signature into the Document provided by URL  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param str url: The URL to retrieve document. (required)
        :param SignOptionsData sign_options_data: QR-Code Signature Options for corresponding Document Type
        :param str password: Document password if required.
        :param str storage: The file storage which have to be used.
        :return: SignatureDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.post_qr_code_from_url_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.post_qr_code_from_url_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.__refresh_token()
                raise ApiException('Access token has expired. Token has been refreshed, please run request again.')
        
    def post_qr_code_from_url_with_http_info(self, request, **kwargs):  # noqa: E501
        """Insert QRCode Signature into the Document provided by URL  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param PostQrCodeFromUrlRequest request object with parameters
        :return: SignatureDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_qr_code_from_url" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'url' is set
        if request.url is None:
            raise ValueError("Missing the required parameter `url` when calling `post_qr_code_from_url`")  # noqa: E501

        collection_formats = {}
        path = '/signature/qrcode'
        path_params = {}

        query_params = []
        if self.__downcase_first_letter('Url') in path:
            path = path.replace('{' + self.__downcase_first_letter('Url' + '}'), request.url if request.url is not None else '')
        else:
            if request.url is not None:
                query_params.append((self.__downcase_first_letter('Url'), request.url))  # noqa: E501
        if self.__downcase_first_letter('Password') in path:
            path = path.replace('{' + self.__downcase_first_letter('Password' + '}'), request.password if request.password is not None else '')
        else:
            if request.password is not None:
                query_params.append((self.__downcase_first_letter('Password'), request.password))  # noqa: E501
        if self.__downcase_first_letter('Storage') in path:
            path = path.replace('{' + self.__downcase_first_letter('Storage' + '}'), request.storage if request.storage is not None else '')
        else:
            if request.storage is not None:
                query_params.append((self.__downcase_first_letter('Storage'), request.storage))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        if request.sign_options_data is not None:
            body_params = request.sign_options_data
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth']  # noqa: E501

        return self.api_client.call_api(
            path, 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SignatureDocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_search_barcode(self, request, **kwargs):  # noqa: E501
        """Search the Document with Barcode Signatures  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param str name: The document name. (required)
        :param SearchOptionsData search_options_data: Search Options
        :param str password: Document password if required.
        :param str folder: The folder name.
        :param str storage: The file storage which have to be used.
        :return: SearchDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.post_search_barcode_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.post_search_barcode_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.__refresh_token()
                raise ApiException('Access token has expired. Token has been refreshed, please run request again.')
        
    def post_search_barcode_with_http_info(self, request, **kwargs):  # noqa: E501
        """Search the Document with Barcode Signatures  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param PostSearchBarcodeRequest request object with parameters
        :return: SearchDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_search_barcode" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if request.name is None:
            raise ValueError("Missing the required parameter `name` when calling `post_search_barcode`")  # noqa: E501

        collection_formats = {}
        path = '/signature/{name}/barcode/search'
        path_params = {}
        if request.name is not None:
            path_params[self.__downcase_first_letter('Name')] = request.name  # noqa: E501

        query_params = []
        if self.__downcase_first_letter('Password') in path:
            path = path.replace('{' + self.__downcase_first_letter('Password' + '}'), request.password if request.password is not None else '')
        else:
            if request.password is not None:
                query_params.append((self.__downcase_first_letter('Password'), request.password))  # noqa: E501
        if self.__downcase_first_letter('Folder') in path:
            path = path.replace('{' + self.__downcase_first_letter('Folder' + '}'), request.folder if request.folder is not None else '')
        else:
            if request.folder is not None:
                query_params.append((self.__downcase_first_letter('Folder'), request.folder))  # noqa: E501
        if self.__downcase_first_letter('Storage') in path:
            path = path.replace('{' + self.__downcase_first_letter('Storage' + '}'), request.storage if request.storage is not None else '')
        else:
            if request.storage is not None:
                query_params.append((self.__downcase_first_letter('Storage'), request.storage))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        if request.search_options_data is not None:
            body_params = request.search_options_data
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth']  # noqa: E501

        return self.api_client.call_api(
            path, 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SearchDocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_search_barcode_from_url(self, request, **kwargs):  # noqa: E501
        """Search the url based Document with Barcode Signatures  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param str url: The URL of document. (required)
        :param SearchOptionsData search_options_data: Search Options
        :param str password: Document password if required.
        :param str storage: The file storage which have to be used.
        :return: SearchDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.post_search_barcode_from_url_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.post_search_barcode_from_url_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.__refresh_token()
                raise ApiException('Access token has expired. Token has been refreshed, please run request again.')
        
    def post_search_barcode_from_url_with_http_info(self, request, **kwargs):  # noqa: E501
        """Search the url based Document with Barcode Signatures  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param PostSearchBarcodeFromUrlRequest request object with parameters
        :return: SearchDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_search_barcode_from_url" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'url' is set
        if request.url is None:
            raise ValueError("Missing the required parameter `url` when calling `post_search_barcode_from_url`")  # noqa: E501

        collection_formats = {}
        path = '/signature/barcode/search'
        path_params = {}

        query_params = []
        if self.__downcase_first_letter('Url') in path:
            path = path.replace('{' + self.__downcase_first_letter('Url' + '}'), request.url if request.url is not None else '')
        else:
            if request.url is not None:
                query_params.append((self.__downcase_first_letter('Url'), request.url))  # noqa: E501
        if self.__downcase_first_letter('Password') in path:
            path = path.replace('{' + self.__downcase_first_letter('Password' + '}'), request.password if request.password is not None else '')
        else:
            if request.password is not None:
                query_params.append((self.__downcase_first_letter('Password'), request.password))  # noqa: E501
        if self.__downcase_first_letter('Storage') in path:
            path = path.replace('{' + self.__downcase_first_letter('Storage' + '}'), request.storage if request.storage is not None else '')
        else:
            if request.storage is not None:
                query_params.append((self.__downcase_first_letter('Storage'), request.storage))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        if request.search_options_data is not None:
            body_params = request.search_options_data
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth']  # noqa: E501

        return self.api_client.call_api(
            path, 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SearchDocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_search_collection(self, request, **kwargs):  # noqa: E501
        """Search the Document.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param str name: The Document name. (required)
        :param SearchOptionsCollectionData search_options_collection_data: Search Options Collection for corresponding Document Type.
        :param str password: Document password if required.
        :param str folder: The folder name.
        :param str storage: The file storage which have to be used.
        :return: SearchDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.post_search_collection_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.post_search_collection_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.__refresh_token()
                raise ApiException('Access token has expired. Token has been refreshed, please run request again.')
        
    def post_search_collection_with_http_info(self, request, **kwargs):  # noqa: E501
        """Search the Document.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param PostSearchCollectionRequest request object with parameters
        :return: SearchDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_search_collection" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if request.name is None:
            raise ValueError("Missing the required parameter `name` when calling `post_search_collection`")  # noqa: E501

        collection_formats = {}
        path = '/signature/{name}/collection/search'
        path_params = {}
        if request.name is not None:
            path_params[self.__downcase_first_letter('Name')] = request.name  # noqa: E501

        query_params = []
        if self.__downcase_first_letter('Password') in path:
            path = path.replace('{' + self.__downcase_first_letter('Password' + '}'), request.password if request.password is not None else '')
        else:
            if request.password is not None:
                query_params.append((self.__downcase_first_letter('Password'), request.password))  # noqa: E501
        if self.__downcase_first_letter('Folder') in path:
            path = path.replace('{' + self.__downcase_first_letter('Folder' + '}'), request.folder if request.folder is not None else '')
        else:
            if request.folder is not None:
                query_params.append((self.__downcase_first_letter('Folder'), request.folder))  # noqa: E501
        if self.__downcase_first_letter('Storage') in path:
            path = path.replace('{' + self.__downcase_first_letter('Storage' + '}'), request.storage if request.storage is not None else '')
        else:
            if request.storage is not None:
                query_params.append((self.__downcase_first_letter('Storage'), request.storage))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        if request.search_options_collection_data is not None:
            body_params = request.search_options_collection_data
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth']  # noqa: E501

        return self.api_client.call_api(
            path, 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SearchDocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_search_collection_from_url(self, request, **kwargs):  # noqa: E501
        """Search the Document provided by URL.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param str url: The URL to retrieve document. (required)
        :param SearchOptionsCollectionData search_options_collection_data: Search Options Collection for corresponding Document Type.
        :param str password: Document password if required.
        :param str storage: The file storage which have to be used.
        :return: SearchDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.post_search_collection_from_url_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.post_search_collection_from_url_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.__refresh_token()
                raise ApiException('Access token has expired. Token has been refreshed, please run request again.')
        
    def post_search_collection_from_url_with_http_info(self, request, **kwargs):  # noqa: E501
        """Search the Document provided by URL.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param PostSearchCollectionFromUrlRequest request object with parameters
        :return: SearchDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_search_collection_from_url" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'url' is set
        if request.url is None:
            raise ValueError("Missing the required parameter `url` when calling `post_search_collection_from_url`")  # noqa: E501

        collection_formats = {}
        path = '/signature/collection/search'
        path_params = {}

        query_params = []
        if self.__downcase_first_letter('Url') in path:
            path = path.replace('{' + self.__downcase_first_letter('Url' + '}'), request.url if request.url is not None else '')
        else:
            if request.url is not None:
                query_params.append((self.__downcase_first_letter('Url'), request.url))  # noqa: E501
        if self.__downcase_first_letter('Password') in path:
            path = path.replace('{' + self.__downcase_first_letter('Password' + '}'), request.password if request.password is not None else '')
        else:
            if request.password is not None:
                query_params.append((self.__downcase_first_letter('Password'), request.password))  # noqa: E501
        if self.__downcase_first_letter('Storage') in path:
            path = path.replace('{' + self.__downcase_first_letter('Storage' + '}'), request.storage if request.storage is not None else '')
        else:
            if request.storage is not None:
                query_params.append((self.__downcase_first_letter('Storage'), request.storage))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        if request.search_options_collection_data is not None:
            body_params = request.search_options_collection_data
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth']  # noqa: E501

        return self.api_client.call_api(
            path, 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SearchDocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_search_digital(self, request, **kwargs):  # noqa: E501
        """Search the Document with Digital Signatures  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param str name: The document name. (required)
        :param SearchOptionsData search_options_data: Search Options
        :param str password: Document password if required.
        :param str folder: The folder name.
        :param str storage: The file storage which have to be used.
        :return: SearchDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.post_search_digital_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.post_search_digital_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.__refresh_token()
                raise ApiException('Access token has expired. Token has been refreshed, please run request again.')
        
    def post_search_digital_with_http_info(self, request, **kwargs):  # noqa: E501
        """Search the Document with Digital Signatures  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param PostSearchDigitalRequest request object with parameters
        :return: SearchDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_search_digital" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if request.name is None:
            raise ValueError("Missing the required parameter `name` when calling `post_search_digital`")  # noqa: E501

        collection_formats = {}
        path = '/signature/{name}/digital/search'
        path_params = {}
        if request.name is not None:
            path_params[self.__downcase_first_letter('Name')] = request.name  # noqa: E501

        query_params = []
        if self.__downcase_first_letter('Password') in path:
            path = path.replace('{' + self.__downcase_first_letter('Password' + '}'), request.password if request.password is not None else '')
        else:
            if request.password is not None:
                query_params.append((self.__downcase_first_letter('Password'), request.password))  # noqa: E501
        if self.__downcase_first_letter('Folder') in path:
            path = path.replace('{' + self.__downcase_first_letter('Folder' + '}'), request.folder if request.folder is not None else '')
        else:
            if request.folder is not None:
                query_params.append((self.__downcase_first_letter('Folder'), request.folder))  # noqa: E501
        if self.__downcase_first_letter('Storage') in path:
            path = path.replace('{' + self.__downcase_first_letter('Storage' + '}'), request.storage if request.storage is not None else '')
        else:
            if request.storage is not None:
                query_params.append((self.__downcase_first_letter('Storage'), request.storage))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        if request.search_options_data is not None:
            body_params = request.search_options_data
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth']  # noqa: E501

        return self.api_client.call_api(
            path, 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SearchDocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_search_digital_from_url(self, request, **kwargs):  # noqa: E501
        """Search the Document from url with Digital Signatures  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param str url: The url of document. (required)
        :param SearchOptionsData search_options_data: Search Options
        :param str password: Document password if required.
        :param str storage: The file storage which have to be used.
        :return: SearchDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.post_search_digital_from_url_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.post_search_digital_from_url_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.__refresh_token()
                raise ApiException('Access token has expired. Token has been refreshed, please run request again.')
        
    def post_search_digital_from_url_with_http_info(self, request, **kwargs):  # noqa: E501
        """Search the Document from url with Digital Signatures  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param PostSearchDigitalFromUrlRequest request object with parameters
        :return: SearchDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_search_digital_from_url" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'url' is set
        if request.url is None:
            raise ValueError("Missing the required parameter `url` when calling `post_search_digital_from_url`")  # noqa: E501

        collection_formats = {}
        path = '/signature/digital/search'
        path_params = {}

        query_params = []
        if self.__downcase_first_letter('Url') in path:
            path = path.replace('{' + self.__downcase_first_letter('Url' + '}'), request.url if request.url is not None else '')
        else:
            if request.url is not None:
                query_params.append((self.__downcase_first_letter('Url'), request.url))  # noqa: E501
        if self.__downcase_first_letter('Password') in path:
            path = path.replace('{' + self.__downcase_first_letter('Password' + '}'), request.password if request.password is not None else '')
        else:
            if request.password is not None:
                query_params.append((self.__downcase_first_letter('Password'), request.password))  # noqa: E501
        if self.__downcase_first_letter('Storage') in path:
            path = path.replace('{' + self.__downcase_first_letter('Storage' + '}'), request.storage if request.storage is not None else '')
        else:
            if request.storage is not None:
                query_params.append((self.__downcase_first_letter('Storage'), request.storage))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        if request.search_options_data is not None:
            body_params = request.search_options_data
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth']  # noqa: E501

        return self.api_client.call_api(
            path, 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SearchDocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_search_qr_code(self, request, **kwargs):  # noqa: E501
        """Search the Document with QRCode Signatures  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param str name: The document name. (required)
        :param SearchOptionsData search_options_data: Search Options
        :param str password: Document password if required.
        :param str folder: The folder name.
        :param str storage: The file storage which have to be used.
        :return: SearchDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.post_search_qr_code_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.post_search_qr_code_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.__refresh_token()
                raise ApiException('Access token has expired. Token has been refreshed, please run request again.')
        
    def post_search_qr_code_with_http_info(self, request, **kwargs):  # noqa: E501
        """Search the Document with QRCode Signatures  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param PostSearchQrCodeRequest request object with parameters
        :return: SearchDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_search_qr_code" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if request.name is None:
            raise ValueError("Missing the required parameter `name` when calling `post_search_qr_code`")  # noqa: E501

        collection_formats = {}
        path = '/signature/{name}/qrcode/search'
        path_params = {}
        if request.name is not None:
            path_params[self.__downcase_first_letter('Name')] = request.name  # noqa: E501

        query_params = []
        if self.__downcase_first_letter('Password') in path:
            path = path.replace('{' + self.__downcase_first_letter('Password' + '}'), request.password if request.password is not None else '')
        else:
            if request.password is not None:
                query_params.append((self.__downcase_first_letter('Password'), request.password))  # noqa: E501
        if self.__downcase_first_letter('Folder') in path:
            path = path.replace('{' + self.__downcase_first_letter('Folder' + '}'), request.folder if request.folder is not None else '')
        else:
            if request.folder is not None:
                query_params.append((self.__downcase_first_letter('Folder'), request.folder))  # noqa: E501
        if self.__downcase_first_letter('Storage') in path:
            path = path.replace('{' + self.__downcase_first_letter('Storage' + '}'), request.storage if request.storage is not None else '')
        else:
            if request.storage is not None:
                query_params.append((self.__downcase_first_letter('Storage'), request.storage))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        if request.search_options_data is not None:
            body_params = request.search_options_data
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth']  # noqa: E501

        return self.api_client.call_api(
            path, 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SearchDocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_search_qr_code_from_url(self, request, **kwargs):  # noqa: E501
        """Search the url based Document with QRCode Signatures  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param str url: The url of document. (required)
        :param SearchOptionsData search_options_data: Search Options
        :param str password: Document password if required.
        :param str storage: The file storage which have to be used.
        :return: SearchDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.post_search_qr_code_from_url_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.post_search_qr_code_from_url_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.__refresh_token()
                raise ApiException('Access token has expired. Token has been refreshed, please run request again.')
        
    def post_search_qr_code_from_url_with_http_info(self, request, **kwargs):  # noqa: E501
        """Search the url based Document with QRCode Signatures  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param PostSearchQrCodeFromUrlRequest request object with parameters
        :return: SearchDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_search_qr_code_from_url" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'url' is set
        if request.url is None:
            raise ValueError("Missing the required parameter `url` when calling `post_search_qr_code_from_url`")  # noqa: E501

        collection_formats = {}
        path = '/signature/qrcode/search'
        path_params = {}

        query_params = []
        if self.__downcase_first_letter('Url') in path:
            path = path.replace('{' + self.__downcase_first_letter('Url' + '}'), request.url if request.url is not None else '')
        else:
            if request.url is not None:
                query_params.append((self.__downcase_first_letter('Url'), request.url))  # noqa: E501
        if self.__downcase_first_letter('Password') in path:
            path = path.replace('{' + self.__downcase_first_letter('Password' + '}'), request.password if request.password is not None else '')
        else:
            if request.password is not None:
                query_params.append((self.__downcase_first_letter('Password'), request.password))  # noqa: E501
        if self.__downcase_first_letter('Storage') in path:
            path = path.replace('{' + self.__downcase_first_letter('Storage' + '}'), request.storage if request.storage is not None else '')
        else:
            if request.storage is not None:
                query_params.append((self.__downcase_first_letter('Storage'), request.storage))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        if request.search_options_data is not None:
            body_params = request.search_options_data
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth']  # noqa: E501

        return self.api_client.call_api(
            path, 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SearchDocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_stamp(self, request, **kwargs):  # noqa: E501
        """Insert Stamp Signature into the Document  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param str name: The Document name. (required)
        :param SignOptionsData sign_options_data: Stamp Signature Options for corresponding Document Type
        :param str password: Document password if required.
        :param str folder: The folder name.
        :param str storage: The file storage which have to be used.
        :return: SignatureDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.post_stamp_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.post_stamp_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.__refresh_token()
                raise ApiException('Access token has expired. Token has been refreshed, please run request again.')
        
    def post_stamp_with_http_info(self, request, **kwargs):  # noqa: E501
        """Insert Stamp Signature into the Document  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param PostStampRequest request object with parameters
        :return: SignatureDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_stamp" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if request.name is None:
            raise ValueError("Missing the required parameter `name` when calling `post_stamp`")  # noqa: E501

        collection_formats = {}
        path = '/signature/{name}/stamp'
        path_params = {}
        if request.name is not None:
            path_params[self.__downcase_first_letter('Name')] = request.name  # noqa: E501

        query_params = []
        if self.__downcase_first_letter('Password') in path:
            path = path.replace('{' + self.__downcase_first_letter('Password' + '}'), request.password if request.password is not None else '')
        else:
            if request.password is not None:
                query_params.append((self.__downcase_first_letter('Password'), request.password))  # noqa: E501
        if self.__downcase_first_letter('Folder') in path:
            path = path.replace('{' + self.__downcase_first_letter('Folder' + '}'), request.folder if request.folder is not None else '')
        else:
            if request.folder is not None:
                query_params.append((self.__downcase_first_letter('Folder'), request.folder))  # noqa: E501
        if self.__downcase_first_letter('Storage') in path:
            path = path.replace('{' + self.__downcase_first_letter('Storage' + '}'), request.storage if request.storage is not None else '')
        else:
            if request.storage is not None:
                query_params.append((self.__downcase_first_letter('Storage'), request.storage))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        if request.sign_options_data is not None:
            body_params = request.sign_options_data
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth']  # noqa: E501

        return self.api_client.call_api(
            path, 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SignatureDocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_stamp_from_url(self, request, **kwargs):  # noqa: E501
        """Insert Stamp Signature into the Document provided by URL  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param str url: The URL to retrieve document. (required)
        :param SignOptionsData sign_options_data: Stamp Signature Options for corresponding Document Type
        :param str password: Document password if required.
        :param str storage: The file storage which have to be used.
        :return: SignatureDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.post_stamp_from_url_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.post_stamp_from_url_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.__refresh_token()
                raise ApiException('Access token has expired. Token has been refreshed, please run request again.')
        
    def post_stamp_from_url_with_http_info(self, request, **kwargs):  # noqa: E501
        """Insert Stamp Signature into the Document provided by URL  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param PostStampFromUrlRequest request object with parameters
        :return: SignatureDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_stamp_from_url" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'url' is set
        if request.url is None:
            raise ValueError("Missing the required parameter `url` when calling `post_stamp_from_url`")  # noqa: E501

        collection_formats = {}
        path = '/signature/stamp'
        path_params = {}

        query_params = []
        if self.__downcase_first_letter('Url') in path:
            path = path.replace('{' + self.__downcase_first_letter('Url' + '}'), request.url if request.url is not None else '')
        else:
            if request.url is not None:
                query_params.append((self.__downcase_first_letter('Url'), request.url))  # noqa: E501
        if self.__downcase_first_letter('Password') in path:
            path = path.replace('{' + self.__downcase_first_letter('Password' + '}'), request.password if request.password is not None else '')
        else:
            if request.password is not None:
                query_params.append((self.__downcase_first_letter('Password'), request.password))  # noqa: E501
        if self.__downcase_first_letter('Storage') in path:
            path = path.replace('{' + self.__downcase_first_letter('Storage' + '}'), request.storage if request.storage is not None else '')
        else:
            if request.storage is not None:
                query_params.append((self.__downcase_first_letter('Storage'), request.storage))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        if request.sign_options_data is not None:
            body_params = request.sign_options_data
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth']  # noqa: E501

        return self.api_client.call_api(
            path, 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SignatureDocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_text(self, request, **kwargs):  # noqa: E501
        """Insert Text Signature into the Document  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param str name: The Document name. (required)
        :param SignOptionsData sign_options_data: Text Signature Options for corresponding Document Type
        :param str password: Document password if required.
        :param str folder: The folder name.
        :param str storage: The file storage which have to be used.
        :return: SignatureDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.post_text_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.post_text_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.__refresh_token()
                raise ApiException('Access token has expired. Token has been refreshed, please run request again.')
        
    def post_text_with_http_info(self, request, **kwargs):  # noqa: E501
        """Insert Text Signature into the Document  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param PostTextRequest request object with parameters
        :return: SignatureDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_text" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if request.name is None:
            raise ValueError("Missing the required parameter `name` when calling `post_text`")  # noqa: E501

        collection_formats = {}
        path = '/signature/{name}/text'
        path_params = {}
        if request.name is not None:
            path_params[self.__downcase_first_letter('Name')] = request.name  # noqa: E501

        query_params = []
        if self.__downcase_first_letter('Password') in path:
            path = path.replace('{' + self.__downcase_first_letter('Password' + '}'), request.password if request.password is not None else '')
        else:
            if request.password is not None:
                query_params.append((self.__downcase_first_letter('Password'), request.password))  # noqa: E501
        if self.__downcase_first_letter('Folder') in path:
            path = path.replace('{' + self.__downcase_first_letter('Folder' + '}'), request.folder if request.folder is not None else '')
        else:
            if request.folder is not None:
                query_params.append((self.__downcase_first_letter('Folder'), request.folder))  # noqa: E501
        if self.__downcase_first_letter('Storage') in path:
            path = path.replace('{' + self.__downcase_first_letter('Storage' + '}'), request.storage if request.storage is not None else '')
        else:
            if request.storage is not None:
                query_params.append((self.__downcase_first_letter('Storage'), request.storage))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        if request.sign_options_data is not None:
            body_params = request.sign_options_data
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth']  # noqa: E501

        return self.api_client.call_api(
            path, 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SignatureDocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_text_from_url(self, request, **kwargs):  # noqa: E501
        """Insert Text Signature into the Document  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param str url: The URL to retrieve document. (required)
        :param SignOptionsData sign_options_data: Text Signature Options for corresponding Document Type
        :param str password: Document password if required.
        :param str storage: The file storage which have to be used.
        :return: SignatureDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.post_text_from_url_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.post_text_from_url_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.__refresh_token()
                raise ApiException('Access token has expired. Token has been refreshed, please run request again.')
        
    def post_text_from_url_with_http_info(self, request, **kwargs):  # noqa: E501
        """Insert Text Signature into the Document  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param PostTextFromUrlRequest request object with parameters
        :return: SignatureDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_text_from_url" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'url' is set
        if request.url is None:
            raise ValueError("Missing the required parameter `url` when calling `post_text_from_url`")  # noqa: E501

        collection_formats = {}
        path = '/signature/text'
        path_params = {}

        query_params = []
        if self.__downcase_first_letter('Url') in path:
            path = path.replace('{' + self.__downcase_first_letter('Url' + '}'), request.url if request.url is not None else '')
        else:
            if request.url is not None:
                query_params.append((self.__downcase_first_letter('Url'), request.url))  # noqa: E501
        if self.__downcase_first_letter('Password') in path:
            path = path.replace('{' + self.__downcase_first_letter('Password' + '}'), request.password if request.password is not None else '')
        else:
            if request.password is not None:
                query_params.append((self.__downcase_first_letter('Password'), request.password))  # noqa: E501
        if self.__downcase_first_letter('Storage') in path:
            path = path.replace('{' + self.__downcase_first_letter('Storage' + '}'), request.storage if request.storage is not None else '')
        else:
            if request.storage is not None:
                query_params.append((self.__downcase_first_letter('Storage'), request.storage))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        if request.sign_options_data is not None:
            body_params = request.sign_options_data
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth']  # noqa: E501

        return self.api_client.call_api(
            path, 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SignatureDocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_verification_barcode(self, request, **kwargs):  # noqa: E501
        """Verify the Document with Barcode Signatures  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param str name: The document name. (required)
        :param VerifyOptionsData verify_options_data: Verification Options
        :param str password: Document password if required.
        :param str folder: The folder name.
        :param str storage: The file storage which have to be used.
        :return: VerifiedDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.post_verification_barcode_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.post_verification_barcode_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.__refresh_token()
                raise ApiException('Access token has expired. Token has been refreshed, please run request again.')
        
    def post_verification_barcode_with_http_info(self, request, **kwargs):  # noqa: E501
        """Verify the Document with Barcode Signatures  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param PostVerificationBarcodeRequest request object with parameters
        :return: VerifiedDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_verification_barcode" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if request.name is None:
            raise ValueError("Missing the required parameter `name` when calling `post_verification_barcode`")  # noqa: E501

        collection_formats = {}
        path = '/signature/{name}/barcode/verification'
        path_params = {}
        if request.name is not None:
            path_params[self.__downcase_first_letter('Name')] = request.name  # noqa: E501

        query_params = []
        if self.__downcase_first_letter('Password') in path:
            path = path.replace('{' + self.__downcase_first_letter('Password' + '}'), request.password if request.password is not None else '')
        else:
            if request.password is not None:
                query_params.append((self.__downcase_first_letter('Password'), request.password))  # noqa: E501
        if self.__downcase_first_letter('Folder') in path:
            path = path.replace('{' + self.__downcase_first_letter('Folder' + '}'), request.folder if request.folder is not None else '')
        else:
            if request.folder is not None:
                query_params.append((self.__downcase_first_letter('Folder'), request.folder))  # noqa: E501
        if self.__downcase_first_letter('Storage') in path:
            path = path.replace('{' + self.__downcase_first_letter('Storage' + '}'), request.storage if request.storage is not None else '')
        else:
            if request.storage is not None:
                query_params.append((self.__downcase_first_letter('Storage'), request.storage))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        if request.verify_options_data is not None:
            body_params = request.verify_options_data
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth']  # noqa: E501

        return self.api_client.call_api(
            path, 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='VerifiedDocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_verification_barcode_from_url(self, request, **kwargs):  # noqa: E501
        """Verify the url based Document with Barcode Signatures  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param str url: The URL of document. (required)
        :param VerifyOptionsData verify_options_data: Verification Options
        :param str password: Document password if required.
        :param str storage: The file storage which have to be used.
        :return: VerifiedDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.post_verification_barcode_from_url_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.post_verification_barcode_from_url_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.__refresh_token()
                raise ApiException('Access token has expired. Token has been refreshed, please run request again.')
        
    def post_verification_barcode_from_url_with_http_info(self, request, **kwargs):  # noqa: E501
        """Verify the url based Document with Barcode Signatures  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param PostVerificationBarcodeFromUrlRequest request object with parameters
        :return: VerifiedDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_verification_barcode_from_url" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'url' is set
        if request.url is None:
            raise ValueError("Missing the required parameter `url` when calling `post_verification_barcode_from_url`")  # noqa: E501

        collection_formats = {}
        path = '/signature/barcode/verification'
        path_params = {}

        query_params = []
        if self.__downcase_first_letter('Url') in path:
            path = path.replace('{' + self.__downcase_first_letter('Url' + '}'), request.url if request.url is not None else '')
        else:
            if request.url is not None:
                query_params.append((self.__downcase_first_letter('Url'), request.url))  # noqa: E501
        if self.__downcase_first_letter('Password') in path:
            path = path.replace('{' + self.__downcase_first_letter('Password' + '}'), request.password if request.password is not None else '')
        else:
            if request.password is not None:
                query_params.append((self.__downcase_first_letter('Password'), request.password))  # noqa: E501
        if self.__downcase_first_letter('Storage') in path:
            path = path.replace('{' + self.__downcase_first_letter('Storage' + '}'), request.storage if request.storage is not None else '')
        else:
            if request.storage is not None:
                query_params.append((self.__downcase_first_letter('Storage'), request.storage))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        if request.verify_options_data is not None:
            body_params = request.verify_options_data
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth']  # noqa: E501

        return self.api_client.call_api(
            path, 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='VerifiedDocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_verification_collection(self, request, **kwargs):  # noqa: E501
        """Verify the Document.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param str name: The Document name. (required)
        :param VerifyOptionsCollectionData verify_options_collection_data: Verify Options Collection for corresponding Document Type.
        :param str password: Document password if required.
        :param str folder: The folder name.
        :param str storage: The file storage which have to be used.
        :return: VerifiedDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.post_verification_collection_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.post_verification_collection_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.__refresh_token()
                raise ApiException('Access token has expired. Token has been refreshed, please run request again.')
        
    def post_verification_collection_with_http_info(self, request, **kwargs):  # noqa: E501
        """Verify the Document.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param PostVerificationCollectionRequest request object with parameters
        :return: VerifiedDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_verification_collection" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if request.name is None:
            raise ValueError("Missing the required parameter `name` when calling `post_verification_collection`")  # noqa: E501

        collection_formats = {}
        path = '/signature/{name}/collection/verification'
        path_params = {}
        if request.name is not None:
            path_params[self.__downcase_first_letter('Name')] = request.name  # noqa: E501

        query_params = []
        if self.__downcase_first_letter('Password') in path:
            path = path.replace('{' + self.__downcase_first_letter('Password' + '}'), request.password if request.password is not None else '')
        else:
            if request.password is not None:
                query_params.append((self.__downcase_first_letter('Password'), request.password))  # noqa: E501
        if self.__downcase_first_letter('Folder') in path:
            path = path.replace('{' + self.__downcase_first_letter('Folder' + '}'), request.folder if request.folder is not None else '')
        else:
            if request.folder is not None:
                query_params.append((self.__downcase_first_letter('Folder'), request.folder))  # noqa: E501
        if self.__downcase_first_letter('Storage') in path:
            path = path.replace('{' + self.__downcase_first_letter('Storage' + '}'), request.storage if request.storage is not None else '')
        else:
            if request.storage is not None:
                query_params.append((self.__downcase_first_letter('Storage'), request.storage))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        if request.verify_options_collection_data is not None:
            body_params = request.verify_options_collection_data
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth']  # noqa: E501

        return self.api_client.call_api(
            path, 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='VerifiedDocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_verification_collection_from_url(self, request, **kwargs):  # noqa: E501
        """Verify the Document provided by URL.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param str url: The URL to retrieve document. (required)
        :param VerifyOptionsCollectionData verify_options_collection_data: Verify Options Collection for corresponding Document Type.
        :param str password: Document password if required.
        :param str storage: The file storage which have to be used.
        :return: VerifiedDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.post_verification_collection_from_url_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.post_verification_collection_from_url_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.__refresh_token()
                raise ApiException('Access token has expired. Token has been refreshed, please run request again.')
        
    def post_verification_collection_from_url_with_http_info(self, request, **kwargs):  # noqa: E501
        """Verify the Document provided by URL.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param PostVerificationCollectionFromUrlRequest request object with parameters
        :return: VerifiedDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_verification_collection_from_url" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'url' is set
        if request.url is None:
            raise ValueError("Missing the required parameter `url` when calling `post_verification_collection_from_url`")  # noqa: E501

        collection_formats = {}
        path = '/signature/collection/verification'
        path_params = {}

        query_params = []
        if self.__downcase_first_letter('Url') in path:
            path = path.replace('{' + self.__downcase_first_letter('Url' + '}'), request.url if request.url is not None else '')
        else:
            if request.url is not None:
                query_params.append((self.__downcase_first_letter('Url'), request.url))  # noqa: E501
        if self.__downcase_first_letter('Password') in path:
            path = path.replace('{' + self.__downcase_first_letter('Password' + '}'), request.password if request.password is not None else '')
        else:
            if request.password is not None:
                query_params.append((self.__downcase_first_letter('Password'), request.password))  # noqa: E501
        if self.__downcase_first_letter('Storage') in path:
            path = path.replace('{' + self.__downcase_first_letter('Storage' + '}'), request.storage if request.storage is not None else '')
        else:
            if request.storage is not None:
                query_params.append((self.__downcase_first_letter('Storage'), request.storage))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        if request.verify_options_collection_data is not None:
            body_params = request.verify_options_collection_data
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth']  # noqa: E501

        return self.api_client.call_api(
            path, 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='VerifiedDocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_verification_digital(self, request, **kwargs):  # noqa: E501
        """Verify the Document with Digital Signatures  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param str name: The document name. (required)
        :param VerifyOptionsData verify_options_data: Verification Options
        :param str password: Document password if required.
        :param str folder: The folder name.
        :param str certificate_guid: Certificate file guid.
        :param str storage: The file storage which have to be used.
        :return: VerifiedDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.post_verification_digital_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.post_verification_digital_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.__refresh_token()
                raise ApiException('Access token has expired. Token has been refreshed, please run request again.')
        
    def post_verification_digital_with_http_info(self, request, **kwargs):  # noqa: E501
        """Verify the Document with Digital Signatures  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param PostVerificationDigitalRequest request object with parameters
        :return: VerifiedDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_verification_digital" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if request.name is None:
            raise ValueError("Missing the required parameter `name` when calling `post_verification_digital`")  # noqa: E501

        collection_formats = {}
        path = '/signature/{name}/digital/verification'
        path_params = {}
        if request.name is not None:
            path_params[self.__downcase_first_letter('Name')] = request.name  # noqa: E501

        query_params = []
        if self.__downcase_first_letter('Password') in path:
            path = path.replace('{' + self.__downcase_first_letter('Password' + '}'), request.password if request.password is not None else '')
        else:
            if request.password is not None:
                query_params.append((self.__downcase_first_letter('Password'), request.password))  # noqa: E501
        if self.__downcase_first_letter('Folder') in path:
            path = path.replace('{' + self.__downcase_first_letter('Folder' + '}'), request.folder if request.folder is not None else '')
        else:
            if request.folder is not None:
                query_params.append((self.__downcase_first_letter('Folder'), request.folder))  # noqa: E501
        if self.__downcase_first_letter('CertificateGuid') in path:
            path = path.replace('{' + self.__downcase_first_letter('CertificateGuid' + '}'), request.certificate_guid if request.certificate_guid is not None else '')
        else:
            if request.certificate_guid is not None:
                query_params.append((self.__downcase_first_letter('CertificateGuid'), request.certificate_guid))  # noqa: E501
        if self.__downcase_first_letter('Storage') in path:
            path = path.replace('{' + self.__downcase_first_letter('Storage' + '}'), request.storage if request.storage is not None else '')
        else:
            if request.storage is not None:
                query_params.append((self.__downcase_first_letter('Storage'), request.storage))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        if request.verify_options_data is not None:
            body_params = request.verify_options_data
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth']  # noqa: E501

        return self.api_client.call_api(
            path, 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='VerifiedDocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_verification_digital_from_url(self, request, **kwargs):  # noqa: E501
        """Verify the Document from url with Digital Signatures  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param str url: The url of document. (required)
        :param VerifyOptionsData verify_options_data: Verification Options
        :param str password: Document password if required.
        :param str certificate_guid: Digital certificate Guid.
        :param str storage: The file storage which have to be used.
        :return: VerifiedDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.post_verification_digital_from_url_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.post_verification_digital_from_url_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.__refresh_token()
                raise ApiException('Access token has expired. Token has been refreshed, please run request again.')
        
    def post_verification_digital_from_url_with_http_info(self, request, **kwargs):  # noqa: E501
        """Verify the Document from url with Digital Signatures  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param PostVerificationDigitalFromUrlRequest request object with parameters
        :return: VerifiedDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_verification_digital_from_url" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'url' is set
        if request.url is None:
            raise ValueError("Missing the required parameter `url` when calling `post_verification_digital_from_url`")  # noqa: E501

        collection_formats = {}
        path = '/signature/digital/verification'
        path_params = {}

        query_params = []
        if self.__downcase_first_letter('Url') in path:
            path = path.replace('{' + self.__downcase_first_letter('Url' + '}'), request.url if request.url is not None else '')
        else:
            if request.url is not None:
                query_params.append((self.__downcase_first_letter('Url'), request.url))  # noqa: E501
        if self.__downcase_first_letter('Password') in path:
            path = path.replace('{' + self.__downcase_first_letter('Password' + '}'), request.password if request.password is not None else '')
        else:
            if request.password is not None:
                query_params.append((self.__downcase_first_letter('Password'), request.password))  # noqa: E501
        if self.__downcase_first_letter('CertificateGuid') in path:
            path = path.replace('{' + self.__downcase_first_letter('CertificateGuid' + '}'), request.certificate_guid if request.certificate_guid is not None else '')
        else:
            if request.certificate_guid is not None:
                query_params.append((self.__downcase_first_letter('CertificateGuid'), request.certificate_guid))  # noqa: E501
        if self.__downcase_first_letter('Storage') in path:
            path = path.replace('{' + self.__downcase_first_letter('Storage' + '}'), request.storage if request.storage is not None else '')
        else:
            if request.storage is not None:
                query_params.append((self.__downcase_first_letter('Storage'), request.storage))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        if request.verify_options_data is not None:
            body_params = request.verify_options_data
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth']  # noqa: E501

        return self.api_client.call_api(
            path, 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='VerifiedDocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_verification_qr_code(self, request, **kwargs):  # noqa: E501
        """Verify the Document with QRCode Signatures  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param str name: The document name. (required)
        :param VerifyOptionsData verify_options_data: Verification Options
        :param str password: Document password if required.
        :param str folder: The folder name.
        :param str storage: The file storage which have to be used.
        :return: VerifiedDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.post_verification_qr_code_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.post_verification_qr_code_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.__refresh_token()
                raise ApiException('Access token has expired. Token has been refreshed, please run request again.')
        
    def post_verification_qr_code_with_http_info(self, request, **kwargs):  # noqa: E501
        """Verify the Document with QRCode Signatures  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param PostVerificationQrCodeRequest request object with parameters
        :return: VerifiedDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_verification_qr_code" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if request.name is None:
            raise ValueError("Missing the required parameter `name` when calling `post_verification_qr_code`")  # noqa: E501

        collection_formats = {}
        path = '/signature/{name}/qrcode/verification'
        path_params = {}
        if request.name is not None:
            path_params[self.__downcase_first_letter('Name')] = request.name  # noqa: E501

        query_params = []
        if self.__downcase_first_letter('Password') in path:
            path = path.replace('{' + self.__downcase_first_letter('Password' + '}'), request.password if request.password is not None else '')
        else:
            if request.password is not None:
                query_params.append((self.__downcase_first_letter('Password'), request.password))  # noqa: E501
        if self.__downcase_first_letter('Folder') in path:
            path = path.replace('{' + self.__downcase_first_letter('Folder' + '}'), request.folder if request.folder is not None else '')
        else:
            if request.folder is not None:
                query_params.append((self.__downcase_first_letter('Folder'), request.folder))  # noqa: E501
        if self.__downcase_first_letter('Storage') in path:
            path = path.replace('{' + self.__downcase_first_letter('Storage' + '}'), request.storage if request.storage is not None else '')
        else:
            if request.storage is not None:
                query_params.append((self.__downcase_first_letter('Storage'), request.storage))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        if request.verify_options_data is not None:
            body_params = request.verify_options_data
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth']  # noqa: E501

        return self.api_client.call_api(
            path, 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='VerifiedDocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_verification_qr_code_from_url(self, request, **kwargs):  # noqa: E501
        """Verify the url based Document with QRCode Signatures  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param str url: The url of document. (required)
        :param VerifyOptionsData verify_options_data: Verification Options
        :param str password: Document password if required.
        :param str storage: The file storage which have to be used.
        :return: VerifiedDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.post_verification_qr_code_from_url_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.post_verification_qr_code_from_url_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.__refresh_token()
                raise ApiException('Access token has expired. Token has been refreshed, please run request again.')
        
    def post_verification_qr_code_from_url_with_http_info(self, request, **kwargs):  # noqa: E501
        """Verify the url based Document with QRCode Signatures  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param PostVerificationQrCodeFromUrlRequest request object with parameters
        :return: VerifiedDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_verification_qr_code_from_url" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'url' is set
        if request.url is None:
            raise ValueError("Missing the required parameter `url` when calling `post_verification_qr_code_from_url`")  # noqa: E501

        collection_formats = {}
        path = '/signature/qrcode/verification'
        path_params = {}

        query_params = []
        if self.__downcase_first_letter('Url') in path:
            path = path.replace('{' + self.__downcase_first_letter('Url' + '}'), request.url if request.url is not None else '')
        else:
            if request.url is not None:
                query_params.append((self.__downcase_first_letter('Url'), request.url))  # noqa: E501
        if self.__downcase_first_letter('Password') in path:
            path = path.replace('{' + self.__downcase_first_letter('Password' + '}'), request.password if request.password is not None else '')
        else:
            if request.password is not None:
                query_params.append((self.__downcase_first_letter('Password'), request.password))  # noqa: E501
        if self.__downcase_first_letter('Storage') in path:
            path = path.replace('{' + self.__downcase_first_letter('Storage' + '}'), request.storage if request.storage is not None else '')
        else:
            if request.storage is not None:
                query_params.append((self.__downcase_first_letter('Storage'), request.storage))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        if request.verify_options_data is not None:
            body_params = request.verify_options_data
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth']  # noqa: E501

        return self.api_client.call_api(
            path, 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='VerifiedDocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_verification_text(self, request, **kwargs):  # noqa: E501
        """Verify the Document with Text Signatures  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param str name: The document name. (required)
        :param VerifyOptionsData verify_options_data: Verification Options
        :param str password: Document password if required.
        :param str folder: The folder name.
        :param str storage: The file storage which have to be used.
        :return: VerifiedDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.post_verification_text_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.post_verification_text_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.__refresh_token()
                raise ApiException('Access token has expired. Token has been refreshed, please run request again.')
        
    def post_verification_text_with_http_info(self, request, **kwargs):  # noqa: E501
        """Verify the Document with Text Signatures  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param PostVerificationTextRequest request object with parameters
        :return: VerifiedDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_verification_text" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if request.name is None:
            raise ValueError("Missing the required parameter `name` when calling `post_verification_text`")  # noqa: E501

        collection_formats = {}
        path = '/signature/{name}/text/verification'
        path_params = {}
        if request.name is not None:
            path_params[self.__downcase_first_letter('Name')] = request.name  # noqa: E501

        query_params = []
        if self.__downcase_first_letter('Password') in path:
            path = path.replace('{' + self.__downcase_first_letter('Password' + '}'), request.password if request.password is not None else '')
        else:
            if request.password is not None:
                query_params.append((self.__downcase_first_letter('Password'), request.password))  # noqa: E501
        if self.__downcase_first_letter('Folder') in path:
            path = path.replace('{' + self.__downcase_first_letter('Folder' + '}'), request.folder if request.folder is not None else '')
        else:
            if request.folder is not None:
                query_params.append((self.__downcase_first_letter('Folder'), request.folder))  # noqa: E501
        if self.__downcase_first_letter('Storage') in path:
            path = path.replace('{' + self.__downcase_first_letter('Storage' + '}'), request.storage if request.storage is not None else '')
        else:
            if request.storage is not None:
                query_params.append((self.__downcase_first_letter('Storage'), request.storage))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        if request.verify_options_data is not None:
            body_params = request.verify_options_data
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth']  # noqa: E501

        return self.api_client.call_api(
            path, 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='VerifiedDocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_verification_text_from_url(self, request, **kwargs):  # noqa: E501
        """Verify the Document provided by url with Text Signatures  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param str url: The document provided by url. (required)
        :param VerifyOptionsData verify_options_data: Verification Options
        :param str password: Document password if required.
        :param str storage: The file storage which have to be used.
        :return: VerifiedDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        try:
            if kwargs.get('is_async'):
                return self.post_verification_text_from_url_with_http_info(request, **kwargs)  # noqa: E501
            (data) = self.post_verification_text_from_url_with_http_info(request, **kwargs)  # noqa: E501
            return data
        except ApiException as e:
            if e.status == 401:
                self.__refresh_token()
                raise ApiException('Access token has expired. Token has been refreshed, please run request again.')
        
    def post_verification_text_from_url_with_http_info(self, request, **kwargs):  # noqa: E501
        """Verify the Document provided by url with Text Signatures  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param PostVerificationTextFromUrlRequest request object with parameters
        :return: VerifiedDocumentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_verification_text_from_url" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'url' is set
        if request.url is None:
            raise ValueError("Missing the required parameter `url` when calling `post_verification_text_from_url`")  # noqa: E501

        collection_formats = {}
        path = '/signature/text/verification'
        path_params = {}

        query_params = []
        if self.__downcase_first_letter('Url') in path:
            path = path.replace('{' + self.__downcase_first_letter('Url' + '}'), request.url if request.url is not None else '')
        else:
            if request.url is not None:
                query_params.append((self.__downcase_first_letter('Url'), request.url))  # noqa: E501
        if self.__downcase_first_letter('Password') in path:
            path = path.replace('{' + self.__downcase_first_letter('Password' + '}'), request.password if request.password is not None else '')
        else:
            if request.password is not None:
                query_params.append((self.__downcase_first_letter('Password'), request.password))  # noqa: E501
        if self.__downcase_first_letter('Storage') in path:
            path = path.replace('{' + self.__downcase_first_letter('Storage' + '}'), request.storage if request.storage is not None else '')
        else:
            if request.storage is not None:
                query_params.append((self.__downcase_first_letter('Storage'), request.storage))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        if request.verify_options_data is not None:
            body_params = request.verify_options_data
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth']  # noqa: E501

        return self.api_client.call_api(
            path, 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='VerifiedDocumentResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    # Helper method to convert first letter to downcase
    def __downcase_first_letter(self, s):
        if len(s) == 0:
            return str
        else:
            return s[0].lower() + s[1:]


    def __request_token(self):
        config = self.api_client.configuration
        api_version = config.api_version
        config.api_version = ''
        request_url = "oauth2/token"
        form_params = [('grant_type', 'client_credentials'), ('client_id', config.api_key['app_sid']),
                       ('client_secret', config.api_key['api_key'])]

        header_params = {'Accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}

        data = self.api_client.call_api(request_url, 'POST',
                                        {},
                                        [],
                                        header_params,
                                        post_params=form_params,
                                        response_type='object',
                                        files={}, _return_http_data_only=True)
        access_token = data['access_token'] if six.PY3 else data['access_token'].encode('utf8')
        refresh_token = data['refresh_token'] if six.PY3 else data['refresh_token'].encode('utf8')
        self.api_client.configuration.access_token = access_token
        self.api_client.configuration.api_version = api_version
        self.api_client.configuration.refresh_token = refresh_token


    def __refresh_token(self):
        config = self.api_client.configuration
        api_version = config.api_version
        config.api_version = ''
        request_url = "oauth2/token"
        form_params = [('grant_type', 'refresh_token'), ('refresh_token', config.refresh_token)]

        header_params = {'Accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}

        data = self.api_client.call_api(request_url, 'POST',
                                        {},
                                        [],
                                        header_params,
                                        post_params=form_params,
                                        response_type='object',
                                        files={}, _return_http_data_only=True)
        access_token = data['access_token'] if six.PY3 else data['access_token'].encode('utf8')
        refresh_token = data['refresh_token'] if six.PY3 else data['refresh_token'].encode('utf8')
        self.api_client.configuration.access_token = access_token
        self.api_client.configuration.api_version = api_version
        self.api_client.configuration.refresh_token = refresh_token

