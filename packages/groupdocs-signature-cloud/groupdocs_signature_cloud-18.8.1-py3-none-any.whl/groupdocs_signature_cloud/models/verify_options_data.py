# coding: utf-8
# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="VerifyOptionsData.py">
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

class VerifyOptionsData(object):
    """Verify Options - keeps options to verify document.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'is_valid': 'bool',
        'document_page_number': 'int',
        'pages_setup': 'PagesSetupData',
        'options_type': 'str'
    }

    attribute_map = {
        'is_valid': 'IsValid',
        'document_page_number': 'DocumentPageNumber',
        'pages_setup': 'PagesSetup',
        'options_type': 'OptionsType'
    }

    discriminator_value_class_map = {
        'VerifyDigitalOptionsData': 'VerifyDigitalOptionsData',
        'WordsVerifyQRCodeOptionsData': 'WordsVerifyQRCodeOptionsData',
        'ImagesVerifyQRCodeOptionsData': 'ImagesVerifyQRCodeOptionsData',
        'VerifyTextOptionsData': 'VerifyTextOptionsData',
        'WordsVerifyDigitalOptionsData': 'WordsVerifyDigitalOptionsData',
        'CellsVerifyTextOptionsData': 'CellsVerifyTextOptionsData',
        'PdfVerifyBarcodeOptionsData': 'PdfVerifyBarcodeOptionsData',
        'SlidesVerifyQRCodeOptionsData': 'SlidesVerifyQRCodeOptionsData',
        'CellsVerifyDigitalOptionsData': 'CellsVerifyDigitalOptionsData',
        'VerifyQRCodeOptionsData': 'VerifyQRCodeOptionsData',
        'PdfVerifyDigitalOptionsData': 'PdfVerifyDigitalOptionsData',
        'SlidesVerifyBarcodeOptionsData': 'SlidesVerifyBarcodeOptionsData',
        'SlidesVerifyTextOptionsData': 'SlidesVerifyTextOptionsData',
        'CellsVerifyQRCodeOptionsData': 'CellsVerifyQRCodeOptionsData',
        'PdfVerifyTextOptionsData': 'PdfVerifyTextOptionsData',
        'PdfVerifyQRCodeOptionsData': 'PdfVerifyQRCodeOptionsData',
        'WordsVerifyTextOptionsData': 'WordsVerifyTextOptionsData',
        'CellsVerifyBarcodeOptionsData': 'CellsVerifyBarcodeOptionsData',
        'VerifyBarcodeOptionsData': 'VerifyBarcodeOptionsData',
        'WordsVerifyBarcodeOptionsData': 'WordsVerifyBarcodeOptionsData',
        'ImagesVerifyBarcodeOptionsData': 'ImagesVerifyBarcodeOptionsData'
    }

    def __init__(self, is_valid=None, document_page_number=None, pages_setup=None, options_type=None):  # noqa: E501
        """VerifyOptionsData - a model defined in Swagger"""  # noqa: E501

        self._is_valid = None
        self._document_page_number = None
        self._pages_setup = None
        self._options_type = None
        self.discriminator = 'Type'

        if is_valid is not None:
            self.is_valid = is_valid
        if document_page_number is not None:
            self.document_page_number = document_page_number
        if pages_setup is not None:
            self.pages_setup = pages_setup
        if options_type is not None:
            self.options_type = options_type

    @property
    def is_valid(self):
        """Gets the is_valid of this VerifyOptionsData.  # noqa: E501

        Valid property flag  # noqa: E501

        :return: The is_valid of this VerifyOptionsData.  # noqa: E501
        :rtype: bool
        """
        return self._is_valid

    @is_valid.setter
    def is_valid(self, is_valid):
        """Sets the is_valid of this VerifyOptionsData.

        Valid property flag  # noqa: E501

        :param is_valid: The is_valid of this VerifyOptionsData.  # noqa: E501
        :type: bool
        """
        if is_valid is None:
            raise ValueError("Invalid value for `is_valid`, must not be `None`")  # noqa: E501
        self._is_valid = is_valid
    @property
    def document_page_number(self):
        """Gets the document_page_number of this VerifyOptionsData.  # noqa: E501

        Document Page Number to be verified. If property is not set - all Pages of Document will be verified for first occurrence.  # noqa: E501

        :return: The document_page_number of this VerifyOptionsData.  # noqa: E501
        :rtype: int
        """
        return self._document_page_number

    @document_page_number.setter
    def document_page_number(self, document_page_number):
        """Sets the document_page_number of this VerifyOptionsData.

        Document Page Number to be verified. If property is not set - all Pages of Document will be verified for first occurrence.  # noqa: E501

        :param document_page_number: The document_page_number of this VerifyOptionsData.  # noqa: E501
        :type: int
        """
        self._document_page_number = document_page_number
    @property
    def pages_setup(self):
        """Gets the pages_setup of this VerifyOptionsData.  # noqa: E501

        Page Options to specify pages to be verified.  # noqa: E501

        :return: The pages_setup of this VerifyOptionsData.  # noqa: E501
        :rtype: PagesSetupData
        """
        return self._pages_setup

    @pages_setup.setter
    def pages_setup(self, pages_setup):
        """Sets the pages_setup of this VerifyOptionsData.

        Page Options to specify pages to be verified.  # noqa: E501

        :param pages_setup: The pages_setup of this VerifyOptionsData.  # noqa: E501
        :type: PagesSetupData
        """
        self._pages_setup = pages_setup
    @property
    def options_type(self):
        """Gets the options_type of this VerifyOptionsData.  # noqa: E501

        Internal property that specify the name of Options.  # noqa: E501

        :return: The options_type of this VerifyOptionsData.  # noqa: E501
        :rtype: str
        """
        return self._options_type

    @options_type.setter
    def options_type(self, options_type):
        """Sets the options_type of this VerifyOptionsData.

        Internal property that specify the name of Options.  # noqa: E501

        :param options_type: The options_type of this VerifyOptionsData.  # noqa: E501
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
        if not isinstance(other, VerifyOptionsData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
