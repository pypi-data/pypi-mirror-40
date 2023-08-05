# coding: utf-8
# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="DigitalSignatureData.py">
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
class DigitalSignatureData(BaseSignatureData):
    """Contains digital Signature properties.
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
        'is_valid': 'bool',
        'digital_signature_type': 'str',
        'sign_time': 'datetime'
    }

    attribute_map = {
        'comments': 'Comments',
        'is_valid': 'IsValid',
        'digital_signature_type': 'DigitalSignatureType',
        'sign_time': 'SignTime'
    }

    def __init__(self, comments=None, is_valid=None, digital_signature_type=None, sign_time=None):  # noqa: E501
        """DigitalSignatureData - a model defined in Swagger"""  # noqa: E501
        BaseSignatureData.__init__(self)
        self.swagger_types.update(BaseSignatureData.swagger_types)
        self.attribute_map.update(BaseSignatureData.attribute_map)

        self._comments = None
        self._is_valid = None
        self._digital_signature_type = None
        self._sign_time = None
        self.discriminator = None
        self.options_type = "DigitalSignatureData"

        if comments is not None:
            self.comments = comments
        if is_valid is not None:
            self.is_valid = is_valid
        if digital_signature_type is not None:
            self.digital_signature_type = digital_signature_type
        if sign_time is not None:
            self.sign_time = sign_time

    @property
    def comments(self):
        """Gets the comments of this DigitalSignatureData.  # noqa: E501

        Gets or sets the signing purpose comment.  # noqa: E501

        :return: The comments of this DigitalSignatureData.  # noqa: E501
        :rtype: str
        """
        return self._comments

    @comments.setter
    def comments(self, comments):
        """Sets the comments of this DigitalSignatureData.

        Gets or sets the signing purpose comment.  # noqa: E501

        :param comments: The comments of this DigitalSignatureData.  # noqa: E501
        :type: str
        """
        self._comments = comments
    @property
    def is_valid(self):
        """Gets the is_valid of this DigitalSignatureData.  # noqa: E501

        Keeps true if this digital signature is valid and the document has not been tampered with.  # noqa: E501

        :return: The is_valid of this DigitalSignatureData.  # noqa: E501
        :rtype: bool
        """
        return self._is_valid

    @is_valid.setter
    def is_valid(self, is_valid):
        """Sets the is_valid of this DigitalSignatureData.

        Keeps true if this digital signature is valid and the document has not been tampered with.  # noqa: E501

        :param is_valid: The is_valid of this DigitalSignatureData.  # noqa: E501
        :type: bool
        """
        self._is_valid = is_valid
    @property
    def digital_signature_type(self):
        """Gets the digital_signature_type of this DigitalSignatureData.  # noqa: E501

        Gets or sets the type of the digital signature.  # noqa: E501

        :return: The digital_signature_type of this DigitalSignatureData.  # noqa: E501
        :rtype: str
        """
        return self._digital_signature_type

    @digital_signature_type.setter
    def digital_signature_type(self, digital_signature_type):
        """Sets the digital_signature_type of this DigitalSignatureData.

        Gets or sets the type of the digital signature.  # noqa: E501

        :param digital_signature_type: The digital_signature_type of this DigitalSignatureData.  # noqa: E501
        :type: str
        """
        allowed_values = ["Unknown", "CryptoApi", "XmlDsig"]  # noqa: E501
        if not digital_signature_type.isdigit():	
            if digital_signature_type not in allowed_values:
                raise ValueError(
                    "Invalid value for `digital_signature_type` ({0}), must be one of {1}"  # noqa: E501
                    .format(digital_signature_type, allowed_values))
            self._digital_signature_type = digital_signature_type
        else:
            self._digital_signature_type = allowed_values[int(digital_signature_type) if six.PY3 else long(digital_signature_type)]
    @property
    def sign_time(self):
        """Gets the sign_time of this DigitalSignatureData.  # noqa: E501

        Gets or sets the time the document was signed.  # noqa: E501

        :return: The sign_time of this DigitalSignatureData.  # noqa: E501
        :rtype: datetime
        """
        return self._sign_time

    @sign_time.setter
    def sign_time(self, sign_time):
        """Sets the sign_time of this DigitalSignatureData.

        Gets or sets the time the document was signed.  # noqa: E501

        :param sign_time: The sign_time of this DigitalSignatureData.  # noqa: E501
        :type: datetime
        """
        self._sign_time = sign_time
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
        if not isinstance(other, DigitalSignatureData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
