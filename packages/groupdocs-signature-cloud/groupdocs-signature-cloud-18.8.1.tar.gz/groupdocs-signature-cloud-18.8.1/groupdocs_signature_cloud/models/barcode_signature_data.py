# coding: utf-8
# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="BarcodeSignatureData.py">
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

from groupdocs_signature_cloud.models import BaseSignatureData
class BarcodeSignatureData(BaseSignatureData):
    """Contains Bar-code Signature properties.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'barcode_type_name': 'str',
        'text': 'str'
    }

    attribute_map = {
        'barcode_type_name': 'BarcodeTypeName',
        'text': 'Text'
    }

    def __init__(self, barcode_type_name=None, text=None):  # noqa: E501
        """BarcodeSignatureData - a model defined in Swagger"""  # noqa: E501
        BaseSignatureData.__init__(self)
        self.swagger_types.update(BaseSignatureData.swagger_types)
        self.attribute_map.update(BaseSignatureData.attribute_map)

        self._barcode_type_name = None
        self._text = None
        self.discriminator = None
        self.options_type = "BarcodeSignatureData"

        if barcode_type_name is not None:
            self.barcode_type_name = barcode_type_name
        if text is not None:
            self.text = text

    @property
    def barcode_type_name(self):
        """Gets the barcode_type_name of this BarcodeSignatureData.  # noqa: E501

        Specifies the Barcode type.  # noqa: E501

        :return: The barcode_type_name of this BarcodeSignatureData.  # noqa: E501
        :rtype: str
        """
        return self._barcode_type_name

    @barcode_type_name.setter
    def barcode_type_name(self, barcode_type_name):
        """Sets the barcode_type_name of this BarcodeSignatureData.

        Specifies the Barcode type.  # noqa: E501

        :param barcode_type_name: The barcode_type_name of this BarcodeSignatureData.  # noqa: E501
        :type: str
        """
        self._barcode_type_name = barcode_type_name
    @property
    def text(self):
        """Gets the text of this BarcodeSignatureData.  # noqa: E501

        Specifies text of Bar-code.  # noqa: E501

        :return: The text of this BarcodeSignatureData.  # noqa: E501
        :rtype: str
        """
        return self._text

    @text.setter
    def text(self, text):
        """Sets the text of this BarcodeSignatureData.

        Specifies text of Bar-code.  # noqa: E501

        :param text: The text of this BarcodeSignatureData.  # noqa: E501
        :type: str
        """
        self._text = text
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
        if not isinstance(other, BarcodeSignatureData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
