# coding: utf-8
# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="DocumentResponse.py">
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

class DocumentResponse(object):
    """Base class for all responses.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'file_name': 'str',
        'folder': 'str',
        'code': 'str',
        'status': 'str'
    }

    attribute_map = {
        'file_name': 'FileName',
        'folder': 'Folder',
        'code': 'Code',
        'status': 'Status'
    }

    discriminator_value_class_map = {
        'SignatureDocumentResponse': 'SignatureDocumentResponse',
        'VerifiedDocumentResponse': 'VerifiedDocumentResponse',
        'SearchDocumentResponse': 'SearchDocumentResponse'
    }

    def __init__(self, file_name=None, folder=None, code=None, status=None):  # noqa: E501
        """DocumentResponse - a model defined in Swagger"""  # noqa: E501

        self._file_name = None
        self._folder = None
        self._code = None
        self._status = None
        self.discriminator = 'Type'

        if file_name is not None:
            self.file_name = file_name
        if folder is not None:
            self.folder = folder
        if code is not None:
            self.code = code
        if status is not None:
            self.status = status

    @property
    def file_name(self):
        """Gets the file_name of this DocumentResponse.  # noqa: E501

        Output File Name.  # noqa: E501

        :return: The file_name of this DocumentResponse.  # noqa: E501
        :rtype: str
        """
        return self._file_name

    @file_name.setter
    def file_name(self, file_name):
        """Sets the file_name of this DocumentResponse.

        Output File Name.  # noqa: E501

        :param file_name: The file_name of this DocumentResponse.  # noqa: E501
        :type: str
        """
        self._file_name = file_name
    @property
    def folder(self):
        """Gets the folder of this DocumentResponse.  # noqa: E501

        Output folder.  # noqa: E501

        :return: The folder of this DocumentResponse.  # noqa: E501
        :rtype: str
        """
        return self._folder

    @folder.setter
    def folder(self, folder):
        """Sets the folder of this DocumentResponse.

        Output folder.  # noqa: E501

        :param folder: The folder of this DocumentResponse.  # noqa: E501
        :type: str
        """
        self._folder = folder
    @property
    def code(self):
        """Gets the code of this DocumentResponse.  # noqa: E501

        Response status code.  # noqa: E501

        :return: The code of this DocumentResponse.  # noqa: E501
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this DocumentResponse.

        Response status code.  # noqa: E501

        :param code: The code of this DocumentResponse.  # noqa: E501
        :type: str
        """
        if code is None:
            raise ValueError("Invalid value for `code`, must not be `None`")  # noqa: E501
        allowed_values = ["Continue", "SwitchingProtocols", "OK", "Created", "Accepted", "NonAuthoritativeInformation", "NoContent", "ResetContent", "PartialContent", "MultipleChoices", "Ambiguous", "MovedPermanently", "Moved", "Found", "Redirect", "SeeOther", "RedirectMethod", "NotModified", "UseProxy", "Unused", "TemporaryRedirect", "RedirectKeepVerb", "BadRequest", "Unauthorized", "PaymentRequired", "Forbidden", "NotFound", "MethodNotAllowed", "NotAcceptable", "ProxyAuthenticationRequired", "RequestTimeout", "Conflict", "Gone", "LengthRequired", "PreconditionFailed", "RequestEntityTooLarge", "RequestUriTooLong", "UnsupportedMediaType", "RequestedRangeNotSatisfiable", "ExpectationFailed", "UpgradeRequired", "InternalServerError", "NotImplemented", "BadGateway", "ServiceUnavailable", "GatewayTimeout", "HttpVersionNotSupported"]  # noqa: E501
        if not code.isdigit():	
            if code not in allowed_values:
                raise ValueError(
                    "Invalid value for `code` ({0}), must be one of {1}"  # noqa: E501
                    .format(code, allowed_values))
            self._code = code
        else:
            self._code = allowed_values[int(code) if six.PY3 else long(code)]
    @property
    def status(self):
        """Gets the status of this DocumentResponse.  # noqa: E501

        Response status.  # noqa: E501

        :return: The status of this DocumentResponse.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this DocumentResponse.

        Response status.  # noqa: E501

        :param status: The status of this DocumentResponse.  # noqa: E501
        :type: str
        """
        self._status = status
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
        if not isinstance(other, DocumentResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
