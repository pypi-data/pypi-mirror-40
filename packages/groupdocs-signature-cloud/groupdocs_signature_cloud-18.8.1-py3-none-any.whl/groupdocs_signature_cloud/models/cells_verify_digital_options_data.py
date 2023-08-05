# coding: utf-8
# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="CellsVerifyDigitalOptionsData.py">
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

from groupdocs_signature_cloud.models import VerifyDigitalOptionsData
class CellsVerifyDigitalOptionsData(VerifyDigitalOptionsData):
    """Cells Verify Digital Options - keeps options to verify Digital Signature of Cells Documents
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'comments': 'str',
        'sign_date_time_from': 'datetime',
        'sign_date_time_to': 'datetime'
    }

    attribute_map = {
        'comments': 'Comments',
        'sign_date_time_from': 'SignDateTimeFrom',
        'sign_date_time_to': 'SignDateTimeTo'
    }

    def __init__(self, comments=None, sign_date_time_from=None, sign_date_time_to=None):  # noqa: E501
        """CellsVerifyDigitalOptionsData - a model defined in Swagger"""  # noqa: E501
        VerifyDigitalOptionsData.__init__(self)
        self.swagger_types.update(VerifyDigitalOptionsData.swagger_types)
        self.attribute_map.update(VerifyDigitalOptionsData.attribute_map)

        self._comments = None
        self._sign_date_time_from = None
        self._sign_date_time_to = None
        self.discriminator = None
        self.options_type = "CellsVerifyDigitalOptionsData"

        if comments is not None:
            self.comments = comments
        if sign_date_time_from is not None:
            self.sign_date_time_from = sign_date_time_from
        if sign_date_time_to is not None:
            self.sign_date_time_to = sign_date_time_to

    @property
    def comments(self):
        """Gets the comments of this CellsVerifyDigitalOptionsData.  # noqa: E501

        Comments of Digital Signature to validate  # noqa: E501

        :return: The comments of this CellsVerifyDigitalOptionsData.  # noqa: E501
        :rtype: str
        """
        return self._comments

    @comments.setter
    def comments(self, comments):
        """Sets the comments of this CellsVerifyDigitalOptionsData.

        Comments of Digital Signature to validate  # noqa: E501

        :param comments: The comments of this CellsVerifyDigitalOptionsData.  # noqa: E501
        :type: str
        """
        self._comments = comments
    @property
    def sign_date_time_from(self):
        """Gets the sign_date_time_from of this CellsVerifyDigitalOptionsData.  # noqa: E501

        Date and time range of Digital Signature to validate. Nullable value will be ignored.  # noqa: E501

        :return: The sign_date_time_from of this CellsVerifyDigitalOptionsData.  # noqa: E501
        :rtype: datetime
        """
        return self._sign_date_time_from

    @sign_date_time_from.setter
    def sign_date_time_from(self, sign_date_time_from):
        """Sets the sign_date_time_from of this CellsVerifyDigitalOptionsData.

        Date and time range of Digital Signature to validate. Nullable value will be ignored.  # noqa: E501

        :param sign_date_time_from: The sign_date_time_from of this CellsVerifyDigitalOptionsData.  # noqa: E501
        :type: datetime
        """
        self._sign_date_time_from = sign_date_time_from
    @property
    def sign_date_time_to(self):
        """Gets the sign_date_time_to of this CellsVerifyDigitalOptionsData.  # noqa: E501

        Date and time range of Digital Signature to validate. Nullable value will be ignored.  # noqa: E501

        :return: The sign_date_time_to of this CellsVerifyDigitalOptionsData.  # noqa: E501
        :rtype: datetime
        """
        return self._sign_date_time_to

    @sign_date_time_to.setter
    def sign_date_time_to(self, sign_date_time_to):
        """Sets the sign_date_time_to of this CellsVerifyDigitalOptionsData.

        Date and time range of Digital Signature to validate. Nullable value will be ignored.  # noqa: E501

        :param sign_date_time_to: The sign_date_time_to of this CellsVerifyDigitalOptionsData.  # noqa: E501
        :type: datetime
        """
        self._sign_date_time_to = sign_date_time_to
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
        if not isinstance(other, CellsVerifyDigitalOptionsData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
