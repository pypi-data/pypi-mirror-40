# coding: utf-8
# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="VerifyOptionsCollectionData.py">
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

class VerifyOptionsCollectionData(object):
    """Collection of Verify Options - keeps list of options to verify the document.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'items': 'list[VerifyOptionsData]',
        'is_valid': 'bool'
    }

    attribute_map = {
        'items': 'Items',
        'is_valid': 'IsValid'
    }

    def __init__(self, items=None, is_valid=None):  # noqa: E501
        """VerifyOptionsCollectionData - a model defined in Swagger"""  # noqa: E501

        self._items = None
        self._is_valid = None
        self.discriminator = None

        if items is not None:
            self.items = items
        if is_valid is not None:
            self.is_valid = is_valid

    @property
    def items(self):
        """Gets the items of this VerifyOptionsCollectionData.  # noqa: E501

        List of Verify Options records.  # noqa: E501

        :return: The items of this VerifyOptionsCollectionData.  # noqa: E501
        :rtype: list[VerifyOptionsData]
        """
        return self._items

    @items.setter
    def items(self, items):
        """Sets the items of this VerifyOptionsCollectionData.

        List of Verify Options records.  # noqa: E501

        :param items: The items of this VerifyOptionsCollectionData.  # noqa: E501
        :type: list[VerifyOptionsData]
        """
        self._items = items
    @property
    def is_valid(self):
        """Gets the is_valid of this VerifyOptionsCollectionData.  # noqa: E501

        Returns summary value of all collection items. If at least one has Valid as false then return values is false.  If all items were verified successfully then return value is true.  # noqa: E501

        :return: The is_valid of this VerifyOptionsCollectionData.  # noqa: E501
        :rtype: bool
        """
        return self._is_valid

    @is_valid.setter
    def is_valid(self, is_valid):
        """Sets the is_valid of this VerifyOptionsCollectionData.

        Returns summary value of all collection items. If at least one has Valid as false then return values is false.  If all items were verified successfully then return value is true.  # noqa: E501

        :param is_valid: The is_valid of this VerifyOptionsCollectionData.  # noqa: E501
        :type: bool
        """
        if is_valid is None:
            raise ValueError("Invalid value for `is_valid`, must not be `None`")  # noqa: E501
        self._is_valid = is_valid
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
        if not isinstance(other, VerifyOptionsCollectionData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
