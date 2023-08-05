# coding: utf-8
# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="ImagesVerifyBarcodeOptionsData.py">
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

from groupdocs_signature_cloud.models import VerifyBarcodeOptionsData
class ImagesVerifyBarcodeOptionsData(VerifyBarcodeOptionsData):
    """Represents the Barcode Verify Options for Images Documents.
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
        'verify_all_pages': 'bool'
    }

    attribute_map = {
        'document_page_number': 'DocumentPageNumber',
        'pages_setup': 'PagesSetup',
        'verify_all_pages': 'VerifyAllPages'
    }

    def __init__(self, document_page_number=None, pages_setup=None, verify_all_pages=None):  # noqa: E501
        """ImagesVerifyBarcodeOptionsData - a model defined in Swagger"""  # noqa: E501
        VerifyBarcodeOptionsData.__init__(self)
        self.swagger_types.update(VerifyBarcodeOptionsData.swagger_types)
        self.attribute_map.update(VerifyBarcodeOptionsData.attribute_map)

        self._document_page_number = None
        self._pages_setup = None
        self._verify_all_pages = None
        self.discriminator = None
        self.options_type = "ImagesVerifyBarcodeOptionsData"

        if document_page_number is not None:
            self.document_page_number = document_page_number
        if pages_setup is not None:
            self.pages_setup = pages_setup
        if verify_all_pages is not None:
            self.verify_all_pages = verify_all_pages

    @property
    def document_page_number(self):
        """Gets the document_page_number of this ImagesVerifyBarcodeOptionsData.  # noqa: E501

        Gets or sets document page number for verifying. This property can only be used for multi-frames image formats (Tiff). Minimal value is 1.  # noqa: E501

        :return: The document_page_number of this ImagesVerifyBarcodeOptionsData.  # noqa: E501
        :rtype: int
        """
        return self._document_page_number

    @document_page_number.setter
    def document_page_number(self, document_page_number):
        """Sets the document_page_number of this ImagesVerifyBarcodeOptionsData.

        Gets or sets document page number for verifying. This property can only be used for multi-frames image formats (Tiff). Minimal value is 1.  # noqa: E501

        :param document_page_number: The document_page_number of this ImagesVerifyBarcodeOptionsData.  # noqa: E501
        :type: int
        """
        self._document_page_number = document_page_number
    @property
    def pages_setup(self):
        """Gets the pages_setup of this ImagesVerifyBarcodeOptionsData.  # noqa: E501

        Options to specify pages to be verified. This property can only be used for multi-frames image formats (Tiff).  # noqa: E501

        :return: The pages_setup of this ImagesVerifyBarcodeOptionsData.  # noqa: E501
        :rtype: PagesSetupData
        """
        return self._pages_setup

    @pages_setup.setter
    def pages_setup(self, pages_setup):
        """Sets the pages_setup of this ImagesVerifyBarcodeOptionsData.

        Options to specify pages to be verified. This property can only be used for multi-frames image formats (Tiff).  # noqa: E501

        :param pages_setup: The pages_setup of this ImagesVerifyBarcodeOptionsData.  # noqa: E501
        :type: PagesSetupData
        """
        self._pages_setup = pages_setup
    @property
    def verify_all_pages(self):
        """Gets the verify_all_pages of this ImagesVerifyBarcodeOptionsData.  # noqa: E501

        Verify all document pages. This property can only be used for multi-frames image formats (Tiff).  # noqa: E501

        :return: The verify_all_pages of this ImagesVerifyBarcodeOptionsData.  # noqa: E501
        :rtype: bool
        """
        return self._verify_all_pages

    @verify_all_pages.setter
    def verify_all_pages(self, verify_all_pages):
        """Sets the verify_all_pages of this ImagesVerifyBarcodeOptionsData.

        Verify all document pages. This property can only be used for multi-frames image formats (Tiff).  # noqa: E501

        :param verify_all_pages: The verify_all_pages of this ImagesVerifyBarcodeOptionsData.  # noqa: E501
        :type: bool
        """
        self._verify_all_pages = verify_all_pages
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
        if not isinstance(other, ImagesVerifyBarcodeOptionsData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
