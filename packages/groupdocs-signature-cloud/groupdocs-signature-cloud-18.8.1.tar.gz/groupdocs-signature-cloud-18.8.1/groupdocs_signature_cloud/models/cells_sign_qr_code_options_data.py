# coding: utf-8
# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="CellsSignQRCodeOptionsData.py">
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

from groupdocs_signature_cloud.models import SignQRCodeOptionsData
class CellsSignQRCodeOptionsData(SignQRCodeOptionsData):
    """Represents the QRCode Signature Options for Cells Documents.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'sheet_number': 'int',
        'row_number': 'int',
        'column_number': 'int'
    }

    attribute_map = {
        'sheet_number': 'SheetNumber',
        'row_number': 'RowNumber',
        'column_number': 'ColumnNumber'
    }

    def __init__(self, sheet_number=None, row_number=None, column_number=None):  # noqa: E501
        """CellsSignQRCodeOptionsData - a model defined in Swagger"""  # noqa: E501
        SignQRCodeOptionsData.__init__(self)
        self.swagger_types.update(SignQRCodeOptionsData.swagger_types)
        self.attribute_map.update(SignQRCodeOptionsData.attribute_map)

        self._sheet_number = None
        self._row_number = None
        self._column_number = None
        self.discriminator = None
        self.options_type = "CellsSignQRCodeOptionsData"

        if sheet_number is not None:
            self.sheet_number = sheet_number
        if row_number is not None:
            self.row_number = row_number
        if column_number is not None:
            self.column_number = column_number

    @property
    def sheet_number(self):
        """Gets the sheet_number of this CellsSignQRCodeOptionsData.  # noqa: E501

        Gets or sets worksheet number for signing. DocumentPageNumber parameter contains the same value.  # noqa: E501

        :return: The sheet_number of this CellsSignQRCodeOptionsData.  # noqa: E501
        :rtype: int
        """
        return self._sheet_number

    @sheet_number.setter
    def sheet_number(self, sheet_number):
        """Sets the sheet_number of this CellsSignQRCodeOptionsData.

        Gets or sets worksheet number for signing. DocumentPageNumber parameter contains the same value.  # noqa: E501

        :param sheet_number: The sheet_number of this CellsSignQRCodeOptionsData.  # noqa: E501
        :type: int
        """
        self._sheet_number = sheet_number
    @property
    def row_number(self):
        """Gets the row_number of this CellsSignQRCodeOptionsData.  # noqa: E501

        Gets or sets the top row number of signature (min value is 0). Top parameter contains the same value.  # noqa: E501

        :return: The row_number of this CellsSignQRCodeOptionsData.  # noqa: E501
        :rtype: int
        """
        return self._row_number

    @row_number.setter
    def row_number(self, row_number):
        """Sets the row_number of this CellsSignQRCodeOptionsData.

        Gets or sets the top row number of signature (min value is 0). Top parameter contains the same value.  # noqa: E501

        :param row_number: The row_number of this CellsSignQRCodeOptionsData.  # noqa: E501
        :type: int
        """
        self._row_number = row_number
    @property
    def column_number(self):
        """Gets the column_number of this CellsSignQRCodeOptionsData.  # noqa: E501

        Gets or sets the left column number of signature (min value is 0). Left parameter contains the same value.  # noqa: E501

        :return: The column_number of this CellsSignQRCodeOptionsData.  # noqa: E501
        :rtype: int
        """
        return self._column_number

    @column_number.setter
    def column_number(self, column_number):
        """Sets the column_number of this CellsSignQRCodeOptionsData.

        Gets or sets the left column number of signature (min value is 0). Left parameter contains the same value.  # noqa: E501

        :param column_number: The column_number of this CellsSignQRCodeOptionsData.  # noqa: E501
        :type: int
        """
        self._column_number = column_number
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
        if not isinstance(other, CellsSignQRCodeOptionsData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
