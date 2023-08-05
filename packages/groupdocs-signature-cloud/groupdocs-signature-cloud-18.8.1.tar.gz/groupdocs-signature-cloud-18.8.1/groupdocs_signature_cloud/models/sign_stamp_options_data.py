# coding: utf-8
# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="SignStampOptionsData.py">
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

from groupdocs_signature_cloud.models import SignImageOptionsData
class SignStampOptionsData(SignImageOptionsData):
    """Represents the Stamp Signature Options.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'outer_lines': 'list[StampLineData]',
        'inner_lines': 'list[StampLineData]',
        'background_color': 'Color',
        'background_brush': 'BrushData',
        'background_color_crop_type': 'str',
        'background_image_crop_type': 'str'
    }

    attribute_map = {
        'outer_lines': 'OuterLines',
        'inner_lines': 'InnerLines',
        'background_color': 'BackgroundColor',
        'background_brush': 'BackgroundBrush',
        'background_color_crop_type': 'BackgroundColorCropType',
        'background_image_crop_type': 'BackgroundImageCropType'
    }

    def __init__(self, outer_lines=None, inner_lines=None, background_color=None, background_brush=None, background_color_crop_type=None, background_image_crop_type=None):  # noqa: E501
        """SignStampOptionsData - a model defined in Swagger"""  # noqa: E501
        SignImageOptionsData.__init__(self)
        self.swagger_types.update(SignImageOptionsData.swagger_types)
        self.attribute_map.update(SignImageOptionsData.attribute_map)

        self._outer_lines = None
        self._inner_lines = None
        self._background_color = None
        self._background_brush = None
        self._background_color_crop_type = None
        self._background_image_crop_type = None
        self.discriminator = None
        self.options_type = "SignStampOptionsData"

        if outer_lines is not None:
            self.outer_lines = outer_lines
        if inner_lines is not None:
            self.inner_lines = inner_lines
        if background_color is not None:
            self.background_color = background_color
        if background_brush is not None:
            self.background_brush = background_brush
        if background_color_crop_type is not None:
            self.background_color_crop_type = background_color_crop_type
        if background_image_crop_type is not None:
            self.background_image_crop_type = background_image_crop_type

    @property
    def outer_lines(self):
        """Gets the outer_lines of this SignStampOptionsData.  # noqa: E501

        List of Outer Lines rendered as concentric circles.  # noqa: E501

        :return: The outer_lines of this SignStampOptionsData.  # noqa: E501
        :rtype: list[StampLineData]
        """
        return self._outer_lines

    @outer_lines.setter
    def outer_lines(self, outer_lines):
        """Sets the outer_lines of this SignStampOptionsData.

        List of Outer Lines rendered as concentric circles.  # noqa: E501

        :param outer_lines: The outer_lines of this SignStampOptionsData.  # noqa: E501
        :type: list[StampLineData]
        """
        self._outer_lines = outer_lines
    @property
    def inner_lines(self):
        """Gets the inner_lines of this SignStampOptionsData.  # noqa: E501

        List of Inner Lines rendered as set of rectangles.  # noqa: E501

        :return: The inner_lines of this SignStampOptionsData.  # noqa: E501
        :rtype: list[StampLineData]
        """
        return self._inner_lines

    @inner_lines.setter
    def inner_lines(self, inner_lines):
        """Sets the inner_lines of this SignStampOptionsData.

        List of Inner Lines rendered as set of rectangles.  # noqa: E501

        :param inner_lines: The inner_lines of this SignStampOptionsData.  # noqa: E501
        :type: list[StampLineData]
        """
        self._inner_lines = inner_lines
    @property
    def background_color(self):
        """Gets the background_color of this SignStampOptionsData.  # noqa: E501

        Gets or sets the background color of signature.  # noqa: E501

        :return: The background_color of this SignStampOptionsData.  # noqa: E501
        :rtype: Color
        """
        return self._background_color

    @background_color.setter
    def background_color(self, background_color):
        """Sets the background_color of this SignStampOptionsData.

        Gets or sets the background color of signature.  # noqa: E501

        :param background_color: The background_color of this SignStampOptionsData.  # noqa: E501
        :type: Color
        """
        self._background_color = background_color
    @property
    def background_brush(self):
        """Gets the background_brush of this SignStampOptionsData.  # noqa: E501

        Gets or sets the signature background brush. Value by default is null.  When property has a value it is used instead BackgroundBrush property.  # noqa: E501

        :return: The background_brush of this SignStampOptionsData.  # noqa: E501
        :rtype: BrushData
        """
        return self._background_brush

    @background_brush.setter
    def background_brush(self, background_brush):
        """Sets the background_brush of this SignStampOptionsData.

        Gets or sets the signature background brush. Value by default is null.  When property has a value it is used instead BackgroundBrush property.  # noqa: E501

        :param background_brush: The background_brush of this SignStampOptionsData.  # noqa: E501
        :type: BrushData
        """
        self._background_brush = background_brush
    @property
    def background_color_crop_type(self):
        """Gets the background_color_crop_type of this SignStampOptionsData.  # noqa: E501

        Gets or sets the background color crop type of signature.  # noqa: E501

        :return: The background_color_crop_type of this SignStampOptionsData.  # noqa: E501
        :rtype: str
        """
        return self._background_color_crop_type

    @background_color_crop_type.setter
    def background_color_crop_type(self, background_color_crop_type):
        """Sets the background_color_crop_type of this SignStampOptionsData.

        Gets or sets the background color crop type of signature.  # noqa: E501

        :param background_color_crop_type: The background_color_crop_type of this SignStampOptionsData.  # noqa: E501
        :type: str
        """
        allowed_values = ["None", "OuterArea", "MiddleArea", "InnerArea"]  # noqa: E501
        if not background_color_crop_type.isdigit():	
            if background_color_crop_type not in allowed_values:
                raise ValueError(
                    "Invalid value for `background_color_crop_type` ({0}), must be one of {1}"  # noqa: E501
                    .format(background_color_crop_type, allowed_values))
            self._background_color_crop_type = background_color_crop_type
        else:
            self._background_color_crop_type = allowed_values[int(background_color_crop_type) if six.PY3 else long(background_color_crop_type)]
    @property
    def background_image_crop_type(self):
        """Gets the background_image_crop_type of this SignStampOptionsData.  # noqa: E501

        Gets or sets the background image crop type of signature.  # noqa: E501

        :return: The background_image_crop_type of this SignStampOptionsData.  # noqa: E501
        :rtype: str
        """
        return self._background_image_crop_type

    @background_image_crop_type.setter
    def background_image_crop_type(self, background_image_crop_type):
        """Sets the background_image_crop_type of this SignStampOptionsData.

        Gets or sets the background image crop type of signature.  # noqa: E501

        :param background_image_crop_type: The background_image_crop_type of this SignStampOptionsData.  # noqa: E501
        :type: str
        """
        allowed_values = ["None", "OuterArea", "MiddleArea", "InnerArea"]  # noqa: E501
        if not background_image_crop_type.isdigit():	
            if background_image_crop_type not in allowed_values:
                raise ValueError(
                    "Invalid value for `background_image_crop_type` ({0}), must be one of {1}"  # noqa: E501
                    .format(background_image_crop_type, allowed_values))
            self._background_image_crop_type = background_image_crop_type
        else:
            self._background_image_crop_type = allowed_values[int(background_image_crop_type) if six.PY3 else long(background_image_crop_type)]
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
        if not isinstance(other, SignStampOptionsData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
