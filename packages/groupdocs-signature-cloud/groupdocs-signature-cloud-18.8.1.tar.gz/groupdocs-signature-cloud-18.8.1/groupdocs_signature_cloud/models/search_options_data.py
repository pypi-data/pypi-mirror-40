# coding: utf-8
# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="SearchOptionsData.py">
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
import pprint
import re  # noqa: F401

import six

class SearchOptionsData(object):
    """Search Options - keeps options to Search document
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'document_page_number': 'int',
        'pages_setup': 'PagesSetupData',
        'search_all_pages': 'bool',
        'options_type': 'str'
    }

    attribute_map = {
        'document_page_number': 'DocumentPageNumber',
        'pages_setup': 'PagesSetup',
        'search_all_pages': 'SearchAllPages',
        'options_type': 'OptionsType'
    }

    discriminator_value_class_map = {
        'CellsSearchBarcodeOptionsData': 'CellsSearchBarcodeOptionsData',
        'CellsSearchQRCodeOptionsData': 'CellsSearchQRCodeOptionsData',
        'ImagesSearchBarcodeOptionsData': 'ImagesSearchBarcodeOptionsData',
        'SearchBarcodeOptionsData': 'SearchBarcodeOptionsData',
        'WordsSearchBarcodeOptionsData': 'WordsSearchBarcodeOptionsData',
        'ImagesSearchQRCodeOptionsData': 'ImagesSearchQRCodeOptionsData',
        'SearchQRCodeOptionsData': 'SearchQRCodeOptionsData',
        'PdfSearchDigitalOptionsData': 'PdfSearchDigitalOptionsData',
        'WordsSearchQRCodeOptionsData': 'WordsSearchQRCodeOptionsData',
        'CellsSearchDigitalOptionsData': 'CellsSearchDigitalOptionsData',
        'SlidesSearchQRCodeOptionsData': 'SlidesSearchQRCodeOptionsData',
        'WordsSearchDigitalOptionsData': 'WordsSearchDigitalOptionsData',
        'SlidesSearchBarcodeOptionsData': 'SlidesSearchBarcodeOptionsData',
        'PdfSearchQRCodeOptionsData': 'PdfSearchQRCodeOptionsData',
        'PdfSearchBarcodeOptionsData': 'PdfSearchBarcodeOptionsData',
        'SearchDigitalOptionsData': 'SearchDigitalOptionsData'
    }

    def __init__(self, document_page_number=None, pages_setup=None, search_all_pages=None, options_type=None):  # noqa: E501
        """SearchOptionsData - a model defined in Swagger"""  # noqa: E501

        self._document_page_number = None
        self._pages_setup = None
        self._search_all_pages = None
        self._options_type = None
        self.discriminator = 'Type'

        if document_page_number is not None:
            self.document_page_number = document_page_number
        if pages_setup is not None:
            self.pages_setup = pages_setup
        if search_all_pages is not None:
            self.search_all_pages = search_all_pages
        if options_type is not None:
            self.options_type = options_type

    @property
    def document_page_number(self):
        """Gets the document_page_number of this SearchOptionsData.  # noqa: E501

        Gets or sets Document page number for searching. Value is optional.  # noqa: E501

        :return: The document_page_number of this SearchOptionsData.  # noqa: E501
        :rtype: int
        """
        return self._document_page_number

    @document_page_number.setter
    def document_page_number(self, document_page_number):
        """Sets the document_page_number of this SearchOptionsData.

        Gets or sets Document page number for searching. Value is optional.  # noqa: E501

        :param document_page_number: The document_page_number of this SearchOptionsData.  # noqa: E501
        :type: int
        """
        self._document_page_number = document_page_number
    @property
    def pages_setup(self):
        """Gets the pages_setup of this SearchOptionsData.  # noqa: E501

        Options to specify pages for Signature searching.  # noqa: E501

        :return: The pages_setup of this SearchOptionsData.  # noqa: E501
        :rtype: PagesSetupData
        """
        return self._pages_setup

    @pages_setup.setter
    def pages_setup(self, pages_setup):
        """Sets the pages_setup of this SearchOptionsData.

        Options to specify pages for Signature searching.  # noqa: E501

        :param pages_setup: The pages_setup of this SearchOptionsData.  # noqa: E501
        :type: PagesSetupData
        """
        self._pages_setup = pages_setup
    @property
    def search_all_pages(self):
        """Gets the search_all_pages of this SearchOptionsData.  # noqa: E501

        Flag to search on each Document page.  # noqa: E501

        :return: The search_all_pages of this SearchOptionsData.  # noqa: E501
        :rtype: bool
        """
        return self._search_all_pages

    @search_all_pages.setter
    def search_all_pages(self, search_all_pages):
        """Sets the search_all_pages of this SearchOptionsData.

        Flag to search on each Document page.  # noqa: E501

        :param search_all_pages: The search_all_pages of this SearchOptionsData.  # noqa: E501
        :type: bool
        """
        if search_all_pages is None:
            raise ValueError("Invalid value for `search_all_pages`, must not be `None`")  # noqa: E501
        self._search_all_pages = search_all_pages
    @property
    def options_type(self):
        """Gets the options_type of this SearchOptionsData.  # noqa: E501

        Internal property that specify the name of Options.  # noqa: E501

        :return: The options_type of this SearchOptionsData.  # noqa: E501
        :rtype: str
        """
        return self._options_type

    @options_type.setter
    def options_type(self, options_type):
        """Sets the options_type of this SearchOptionsData.

        Internal property that specify the name of Options.  # noqa: E501

        :param options_type: The options_type of this SearchOptionsData.  # noqa: E501
        :type: str
        """
        self._options_type = options_type
    def get_real_child_model(self, data):
        """Returns the real base class specified by the discriminator"""
        discriminator_value = data[self.discriminator].lower()
        return self.discriminator_value_class_map.get(discriminator_value)

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, SearchOptionsData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
