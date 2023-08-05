# coding: utf-8
# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="DocumentInfo.py">
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

class DocumentInfo(object):
    """Describes document information.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'name': 'str',
        'folder': 'str',
        'extension': 'str',
        'file_format': 'str',
        'size': 'int',
        'date_modified': 'datetime',
        'pages': 'PagesInfo'
    }

    attribute_map = {
        'name': 'Name',
        'folder': 'Folder',
        'extension': 'Extension',
        'file_format': 'FileFormat',
        'size': 'Size',
        'date_modified': 'DateModified',
        'pages': 'Pages'
    }

    def __init__(self, name=None, folder=None, extension=None, file_format=None, size=None, date_modified=None, pages=None):  # noqa: E501
        """DocumentInfo - a model defined in Swagger"""  # noqa: E501

        self._name = None
        self._folder = None
        self._extension = None
        self._file_format = None
        self._size = None
        self._date_modified = None
        self._pages = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if folder is not None:
            self.folder = folder
        if extension is not None:
            self.extension = extension
        if file_format is not None:
            self.file_format = file_format
        if size is not None:
            self.size = size
        if date_modified is not None:
            self.date_modified = date_modified
        if pages is not None:
            self.pages = pages

    @property
    def name(self):
        """Gets the name of this DocumentInfo.  # noqa: E501

        Document name  # noqa: E501

        :return: The name of this DocumentInfo.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this DocumentInfo.

        Document name  # noqa: E501

        :param name: The name of this DocumentInfo.  # noqa: E501
        :type: str
        """
        self._name = name
    @property
    def folder(self):
        """Gets the folder of this DocumentInfo.  # noqa: E501

        File name.  # noqa: E501

        :return: The folder of this DocumentInfo.  # noqa: E501
        :rtype: str
        """
        return self._folder

    @folder.setter
    def folder(self, folder):
        """Sets the folder of this DocumentInfo.

        File name.  # noqa: E501

        :param folder: The folder of this DocumentInfo.  # noqa: E501
        :type: str
        """
        self._folder = folder
    @property
    def extension(self):
        """Gets the extension of this DocumentInfo.  # noqa: E501

        Extension  # noqa: E501

        :return: The extension of this DocumentInfo.  # noqa: E501
        :rtype: str
        """
        return self._extension

    @extension.setter
    def extension(self, extension):
        """Sets the extension of this DocumentInfo.

        Extension  # noqa: E501

        :param extension: The extension of this DocumentInfo.  # noqa: E501
        :type: str
        """
        self._extension = extension
    @property
    def file_format(self):
        """Gets the file_format of this DocumentInfo.  # noqa: E501

        File format.  # noqa: E501

        :return: The file_format of this DocumentInfo.  # noqa: E501
        :rtype: str
        """
        return self._file_format

    @file_format.setter
    def file_format(self, file_format):
        """Sets the file_format of this DocumentInfo.

        File format.  # noqa: E501

        :param file_format: The file_format of this DocumentInfo.  # noqa: E501
        :type: str
        """
        self._file_format = file_format
    @property
    def size(self):
        """Gets the size of this DocumentInfo.  # noqa: E501

        Size in bytes.  # noqa: E501

        :return: The size of this DocumentInfo.  # noqa: E501
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        """Sets the size of this DocumentInfo.

        Size in bytes.  # noqa: E501

        :param size: The size of this DocumentInfo.  # noqa: E501
        :type: int
        """
        if size is None:
            raise ValueError("Invalid value for `size`, must not be `None`")  # noqa: E501
        self._size = size
    @property
    def date_modified(self):
        """Gets the date_modified of this DocumentInfo.  # noqa: E501

        Modification date.  # noqa: E501

        :return: The date_modified of this DocumentInfo.  # noqa: E501
        :rtype: datetime
        """
        return self._date_modified

    @date_modified.setter
    def date_modified(self, date_modified):
        """Sets the date_modified of this DocumentInfo.

        Modification date.  # noqa: E501

        :param date_modified: The date_modified of this DocumentInfo.  # noqa: E501
        :type: datetime
        """
        if date_modified is None:
            raise ValueError("Invalid value for `date_modified`, must not be `None`")  # noqa: E501
        self._date_modified = date_modified
    @property
    def pages(self):
        """Gets the pages of this DocumentInfo.  # noqa: E501

        Pages information.  # noqa: E501

        :return: The pages of this DocumentInfo.  # noqa: E501
        :rtype: PagesInfo
        """
        return self._pages

    @pages.setter
    def pages(self, pages):
        """Sets the pages of this DocumentInfo.

        Pages information.  # noqa: E501

        :param pages: The pages of this DocumentInfo.  # noqa: E501
        :type: PagesInfo
        """
        self._pages = pages
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
        if not isinstance(other, DocumentInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
