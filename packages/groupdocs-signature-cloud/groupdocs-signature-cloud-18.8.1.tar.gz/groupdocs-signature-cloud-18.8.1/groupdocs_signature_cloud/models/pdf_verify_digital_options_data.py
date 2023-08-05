# coding: utf-8
# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="PdfVerifyDigitalOptionsData.py">
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
class PdfVerifyDigitalOptionsData(VerifyDigitalOptionsData):
    """Pdf Verify Digital Options - keeps options to verify Digital Signature of Pdf Documents
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'reason': 'str',
        'contact': 'str',
        'location': 'str'
    }

    attribute_map = {
        'reason': 'Reason',
        'contact': 'Contact',
        'location': 'Location'
    }

    def __init__(self, reason=None, contact=None, location=None):  # noqa: E501
        """PdfVerifyDigitalOptionsData - a model defined in Swagger"""  # noqa: E501
        VerifyDigitalOptionsData.__init__(self)
        self.swagger_types.update(VerifyDigitalOptionsData.swagger_types)
        self.attribute_map.update(VerifyDigitalOptionsData.attribute_map)

        self._reason = None
        self._contact = None
        self._location = None
        self.discriminator = None
        self.options_type = "PdfVerifyDigitalOptionsData"

        if reason is not None:
            self.reason = reason
        if contact is not None:
            self.contact = contact
        if location is not None:
            self.location = location

    @property
    def reason(self):
        """Gets the reason of this PdfVerifyDigitalOptionsData.  # noqa: E501

        Reason of Digital Signature to validate  # noqa: E501

        :return: The reason of this PdfVerifyDigitalOptionsData.  # noqa: E501
        :rtype: str
        """
        return self._reason

    @reason.setter
    def reason(self, reason):
        """Sets the reason of this PdfVerifyDigitalOptionsData.

        Reason of Digital Signature to validate  # noqa: E501

        :param reason: The reason of this PdfVerifyDigitalOptionsData.  # noqa: E501
        :type: str
        """
        self._reason = reason
    @property
    def contact(self):
        """Gets the contact of this PdfVerifyDigitalOptionsData.  # noqa: E501

        Signature Contact to validate  # noqa: E501

        :return: The contact of this PdfVerifyDigitalOptionsData.  # noqa: E501
        :rtype: str
        """
        return self._contact

    @contact.setter
    def contact(self, contact):
        """Sets the contact of this PdfVerifyDigitalOptionsData.

        Signature Contact to validate  # noqa: E501

        :param contact: The contact of this PdfVerifyDigitalOptionsData.  # noqa: E501
        :type: str
        """
        self._contact = contact
    @property
    def location(self):
        """Gets the location of this PdfVerifyDigitalOptionsData.  # noqa: E501

        Signature Location to validate  # noqa: E501

        :return: The location of this PdfVerifyDigitalOptionsData.  # noqa: E501
        :rtype: str
        """
        return self._location

    @location.setter
    def location(self, location):
        """Sets the location of this PdfVerifyDigitalOptionsData.

        Signature Location to validate  # noqa: E501

        :param location: The location of this PdfVerifyDigitalOptionsData.  # noqa: E501
        :type: str
        """
        self._location = location
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
        if not isinstance(other, PdfVerifyDigitalOptionsData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
