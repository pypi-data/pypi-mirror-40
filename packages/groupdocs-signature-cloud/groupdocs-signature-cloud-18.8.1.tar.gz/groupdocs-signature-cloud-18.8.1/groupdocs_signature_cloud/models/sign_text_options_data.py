# coding: utf-8
# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="SignTextOptionsData.py">
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

from groupdocs_signature_cloud.models import SignOptionsData
class SignTextOptionsData(SignOptionsData):
    """Base container class for signature options data
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'left': 'int',
        'top': 'int',
        'width': 'int',
        'height': 'int',
        'location_measure_type': 'str',
        'size_measure_type': 'str',
        'stretch': 'str',
        'rotation_angle': 'int',
        'horizontal_alignment': 'str',
        'vertical_alignment': 'str',
        'margin': 'PaddingData',
        'margin_measure_type': 'str',
        'text': 'str',
        'sign_all_pages': 'bool',
        'font': 'SignatureFontData',
        'fore_color': 'Color',
        'border_color': 'Color',
        'background_color': 'Color',
        'background_brush': 'BrushData'
    }

    attribute_map = {
        'left': 'Left',
        'top': 'Top',
        'width': 'Width',
        'height': 'Height',
        'location_measure_type': 'LocationMeasureType',
        'size_measure_type': 'SizeMeasureType',
        'stretch': 'Stretch',
        'rotation_angle': 'RotationAngle',
        'horizontal_alignment': 'HorizontalAlignment',
        'vertical_alignment': 'VerticalAlignment',
        'margin': 'Margin',
        'margin_measure_type': 'MarginMeasureType',
        'text': 'Text',
        'sign_all_pages': 'SignAllPages',
        'font': 'Font',
        'fore_color': 'ForeColor',
        'border_color': 'BorderColor',
        'background_color': 'BackgroundColor',
        'background_brush': 'BackgroundBrush'
    }

    def __init__(self, left=None, top=None, width=None, height=None, location_measure_type=None, size_measure_type=None, stretch=None, rotation_angle=None, horizontal_alignment=None, vertical_alignment=None, margin=None, margin_measure_type=None, text=None, sign_all_pages=None, font=None, fore_color=None, border_color=None, background_color=None, background_brush=None):  # noqa: E501
        """SignTextOptionsData - a model defined in Swagger"""  # noqa: E501
        SignOptionsData.__init__(self)
        self.swagger_types.update(SignOptionsData.swagger_types)
        self.attribute_map.update(SignOptionsData.attribute_map)

        self._left = None
        self._top = None
        self._width = None
        self._height = None
        self._location_measure_type = None
        self._size_measure_type = None
        self._stretch = None
        self._rotation_angle = None
        self._horizontal_alignment = None
        self._vertical_alignment = None
        self._margin = None
        self._margin_measure_type = None
        self._text = None
        self._sign_all_pages = None
        self._font = None
        self._fore_color = None
        self._border_color = None
        self._background_color = None
        self._background_brush = None
        self.discriminator = None
        self.options_type = "SignTextOptionsData"

        if left is not None:
            self.left = left
        if top is not None:
            self.top = top
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        if location_measure_type is not None:
            self.location_measure_type = location_measure_type
        if size_measure_type is not None:
            self.size_measure_type = size_measure_type
        if stretch is not None:
            self.stretch = stretch
        if rotation_angle is not None:
            self.rotation_angle = rotation_angle
        if horizontal_alignment is not None:
            self.horizontal_alignment = horizontal_alignment
        if vertical_alignment is not None:
            self.vertical_alignment = vertical_alignment
        if margin is not None:
            self.margin = margin
        if margin_measure_type is not None:
            self.margin_measure_type = margin_measure_type
        if text is not None:
            self.text = text
        if sign_all_pages is not None:
            self.sign_all_pages = sign_all_pages
        if font is not None:
            self.font = font
        if fore_color is not None:
            self.fore_color = fore_color
        if border_color is not None:
            self.border_color = border_color
        if background_color is not None:
            self.background_color = background_color
        if background_brush is not None:
            self.background_brush = background_brush

    @property
    def left(self):
        """Gets the left of this SignTextOptionsData.  # noqa: E501

        Left X position of Signature on Document Page in Measure values (pixels or percent see  LocationMeasureType property)  # noqa: E501

        :return: The left of this SignTextOptionsData.  # noqa: E501
        :rtype: int
        """
        return self._left

    @left.setter
    def left(self, left):
        """Sets the left of this SignTextOptionsData.

        Left X position of Signature on Document Page in Measure values (pixels or percent see  LocationMeasureType property)  # noqa: E501

        :param left: The left of this SignTextOptionsData.  # noqa: E501
        :type: int
        """
        self._left = left
    @property
    def top(self):
        """Gets the top of this SignTextOptionsData.  # noqa: E501

        Top Y Position of Signature on Document Page in Measure values (pixels or percent see  LocationMeasureType property)  # noqa: E501

        :return: The top of this SignTextOptionsData.  # noqa: E501
        :rtype: int
        """
        return self._top

    @top.setter
    def top(self, top):
        """Sets the top of this SignTextOptionsData.

        Top Y Position of Signature on Document Page in Measure values (pixels or percent see  LocationMeasureType property)  # noqa: E501

        :param top: The top of this SignTextOptionsData.  # noqa: E501
        :type: int
        """
        self._top = top
    @property
    def width(self):
        """Gets the width of this SignTextOptionsData.  # noqa: E501

        Width of Signature area on Document Page in Measure values (pixels or percent see  SizeMeasureType property)  # noqa: E501

        :return: The width of this SignTextOptionsData.  # noqa: E501
        :rtype: int
        """
        return self._width

    @width.setter
    def width(self, width):
        """Sets the width of this SignTextOptionsData.

        Width of Signature area on Document Page in Measure values (pixels or percent see  SizeMeasureType property)  # noqa: E501

        :param width: The width of this SignTextOptionsData.  # noqa: E501
        :type: int
        """
        self._width = width
    @property
    def height(self):
        """Gets the height of this SignTextOptionsData.  # noqa: E501

        Height of Signature are on Document Page in Measure values (pixels or percent see  SizeMeasureType property)  # noqa: E501

        :return: The height of this SignTextOptionsData.  # noqa: E501
        :rtype: int
        """
        return self._height

    @height.setter
    def height(self, height):
        """Sets the height of this SignTextOptionsData.

        Height of Signature are on Document Page in Measure values (pixels or percent see  SizeMeasureType property)  # noqa: E501

        :param height: The height of this SignTextOptionsData.  # noqa: E501
        :type: int
        """
        self._height = height
    @property
    def location_measure_type(self):
        """Gets the location_measure_type of this SignTextOptionsData.  # noqa: E501

        Measure type (pixels or percent) for Left and Top properties.  # noqa: E501

        :return: The location_measure_type of this SignTextOptionsData.  # noqa: E501
        :rtype: str
        """
        return self._location_measure_type

    @location_measure_type.setter
    def location_measure_type(self, location_measure_type):
        """Sets the location_measure_type of this SignTextOptionsData.

        Measure type (pixels or percent) for Left and Top properties.  # noqa: E501

        :param location_measure_type: The location_measure_type of this SignTextOptionsData.  # noqa: E501
        :type: str
        """
        allowed_values = ["Pixels", "Percents", "Millimeters"]  # noqa: E501
        if not location_measure_type.isdigit():	
            if location_measure_type not in allowed_values:
                raise ValueError(
                    "Invalid value for `location_measure_type` ({0}), must be one of {1}"  # noqa: E501
                    .format(location_measure_type, allowed_values))
            self._location_measure_type = location_measure_type
        else:
            self._location_measure_type = allowed_values[int(location_measure_type) if six.PY3 else long(location_measure_type)]
    @property
    def size_measure_type(self):
        """Gets the size_measure_type of this SignTextOptionsData.  # noqa: E501

        Measure type (pixels or percent) for Width and Height properties.  # noqa: E501

        :return: The size_measure_type of this SignTextOptionsData.  # noqa: E501
        :rtype: str
        """
        return self._size_measure_type

    @size_measure_type.setter
    def size_measure_type(self, size_measure_type):
        """Sets the size_measure_type of this SignTextOptionsData.

        Measure type (pixels or percent) for Width and Height properties.  # noqa: E501

        :param size_measure_type: The size_measure_type of this SignTextOptionsData.  # noqa: E501
        :type: str
        """
        allowed_values = ["Pixels", "Percents", "Millimeters"]  # noqa: E501
        if not size_measure_type.isdigit():	
            if size_measure_type not in allowed_values:
                raise ValueError(
                    "Invalid value for `size_measure_type` ({0}), must be one of {1}"  # noqa: E501
                    .format(size_measure_type, allowed_values))
            self._size_measure_type = size_measure_type
        else:
            self._size_measure_type = allowed_values[int(size_measure_type) if six.PY3 else long(size_measure_type)]
    @property
    def stretch(self):
        """Gets the stretch of this SignTextOptionsData.  # noqa: E501

        Stretch mode on Document Page  # noqa: E501

        :return: The stretch of this SignTextOptionsData.  # noqa: E501
        :rtype: str
        """
        return self._stretch

    @stretch.setter
    def stretch(self, stretch):
        """Sets the stretch of this SignTextOptionsData.

        Stretch mode on Document Page  # noqa: E501

        :param stretch: The stretch of this SignTextOptionsData.  # noqa: E501
        :type: str
        """
        allowed_values = ["None", "PageWidth", "PageHeight", "PageArea"]  # noqa: E501
        if not stretch.isdigit():	
            if stretch not in allowed_values:
                raise ValueError(
                    "Invalid value for `stretch` ({0}), must be one of {1}"  # noqa: E501
                    .format(stretch, allowed_values))
            self._stretch = stretch
        else:
            self._stretch = allowed_values[int(stretch) if six.PY3 else long(stretch)]
    @property
    def rotation_angle(self):
        """Gets the rotation_angle of this SignTextOptionsData.  # noqa: E501

        Rotation angle of signature on document page (clockwise).  # noqa: E501

        :return: The rotation_angle of this SignTextOptionsData.  # noqa: E501
        :rtype: int
        """
        return self._rotation_angle

    @rotation_angle.setter
    def rotation_angle(self, rotation_angle):
        """Sets the rotation_angle of this SignTextOptionsData.

        Rotation angle of signature on document page (clockwise).  # noqa: E501

        :param rotation_angle: The rotation_angle of this SignTextOptionsData.  # noqa: E501
        :type: int
        """
        self._rotation_angle = rotation_angle
    @property
    def horizontal_alignment(self):
        """Gets the horizontal_alignment of this SignTextOptionsData.  # noqa: E501

        Horizontal alignment of signature on document page.  # noqa: E501

        :return: The horizontal_alignment of this SignTextOptionsData.  # noqa: E501
        :rtype: str
        """
        return self._horizontal_alignment

    @horizontal_alignment.setter
    def horizontal_alignment(self, horizontal_alignment):
        """Sets the horizontal_alignment of this SignTextOptionsData.

        Horizontal alignment of signature on document page.  # noqa: E501

        :param horizontal_alignment: The horizontal_alignment of this SignTextOptionsData.  # noqa: E501
        :type: str
        """
        allowed_values = ["Default", "None", "Left", "Center", "Right"]  # noqa: E501
        if not horizontal_alignment.isdigit():	
            if horizontal_alignment not in allowed_values:
                raise ValueError(
                    "Invalid value for `horizontal_alignment` ({0}), must be one of {1}"  # noqa: E501
                    .format(horizontal_alignment, allowed_values))
            self._horizontal_alignment = horizontal_alignment
        else:
            self._horizontal_alignment = allowed_values[int(horizontal_alignment) if six.PY3 else long(horizontal_alignment)]
    @property
    def vertical_alignment(self):
        """Gets the vertical_alignment of this SignTextOptionsData.  # noqa: E501

        Vertical alignment of signature on document page.  # noqa: E501

        :return: The vertical_alignment of this SignTextOptionsData.  # noqa: E501
        :rtype: str
        """
        return self._vertical_alignment

    @vertical_alignment.setter
    def vertical_alignment(self, vertical_alignment):
        """Sets the vertical_alignment of this SignTextOptionsData.

        Vertical alignment of signature on document page.  # noqa: E501

        :param vertical_alignment: The vertical_alignment of this SignTextOptionsData.  # noqa: E501
        :type: str
        """
        allowed_values = ["Default", "None", "Top", "Center", "Bottom"]  # noqa: E501
        if not vertical_alignment.isdigit():	
            if vertical_alignment not in allowed_values:
                raise ValueError(
                    "Invalid value for `vertical_alignment` ({0}), must be one of {1}"  # noqa: E501
                    .format(vertical_alignment, allowed_values))
            self._vertical_alignment = vertical_alignment
        else:
            self._vertical_alignment = allowed_values[int(vertical_alignment) if six.PY3 else long(vertical_alignment)]
    @property
    def margin(self):
        """Gets the margin of this SignTextOptionsData.  # noqa: E501

        Gets or sets the space between Sign and Document edges. (works ONLY if horizontal or vertical alignment are specified).  # noqa: E501

        :return: The margin of this SignTextOptionsData.  # noqa: E501
        :rtype: PaddingData
        """
        return self._margin

    @margin.setter
    def margin(self, margin):
        """Sets the margin of this SignTextOptionsData.

        Gets or sets the space between Sign and Document edges. (works ONLY if horizontal or vertical alignment are specified).  # noqa: E501

        :param margin: The margin of this SignTextOptionsData.  # noqa: E501
        :type: PaddingData
        """
        self._margin = margin
    @property
    def margin_measure_type(self):
        """Gets the margin_measure_type of this SignTextOptionsData.  # noqa: E501

        Gets or sets the measure type (pixels or percent) for Margin.  # noqa: E501

        :return: The margin_measure_type of this SignTextOptionsData.  # noqa: E501
        :rtype: str
        """
        return self._margin_measure_type

    @margin_measure_type.setter
    def margin_measure_type(self, margin_measure_type):
        """Sets the margin_measure_type of this SignTextOptionsData.

        Gets or sets the measure type (pixels or percent) for Margin.  # noqa: E501

        :param margin_measure_type: The margin_measure_type of this SignTextOptionsData.  # noqa: E501
        :type: str
        """
        allowed_values = ["Pixels", "Percents", "Millimeters"]  # noqa: E501
        if not margin_measure_type.isdigit():	
            if margin_measure_type not in allowed_values:
                raise ValueError(
                    "Invalid value for `margin_measure_type` ({0}), must be one of {1}"  # noqa: E501
                    .format(margin_measure_type, allowed_values))
            self._margin_measure_type = margin_measure_type
        else:
            self._margin_measure_type = allowed_values[int(margin_measure_type) if six.PY3 else long(margin_measure_type)]
    @property
    def text(self):
        """Gets the text of this SignTextOptionsData.  # noqa: E501

        Text of signature  # noqa: E501

        :return: The text of this SignTextOptionsData.  # noqa: E501
        :rtype: str
        """
        return self._text

    @text.setter
    def text(self, text):
        """Sets the text of this SignTextOptionsData.

        Text of signature  # noqa: E501

        :param text: The text of this SignTextOptionsData.  # noqa: E501
        :type: str
        """
        self._text = text
    @property
    def sign_all_pages(self):
        """Gets the sign_all_pages of this SignTextOptionsData.  # noqa: E501

        Put signature on all document pages.  # noqa: E501

        :return: The sign_all_pages of this SignTextOptionsData.  # noqa: E501
        :rtype: bool
        """
        return self._sign_all_pages

    @sign_all_pages.setter
    def sign_all_pages(self, sign_all_pages):
        """Sets the sign_all_pages of this SignTextOptionsData.

        Put signature on all document pages.  # noqa: E501

        :param sign_all_pages: The sign_all_pages of this SignTextOptionsData.  # noqa: E501
        :type: bool
        """
        self._sign_all_pages = sign_all_pages
    @property
    def font(self):
        """Gets the font of this SignTextOptionsData.  # noqa: E501

        Gets or sets the font of signature.  # noqa: E501

        :return: The font of this SignTextOptionsData.  # noqa: E501
        :rtype: SignatureFontData
        """
        return self._font

    @font.setter
    def font(self, font):
        """Sets the font of this SignTextOptionsData.

        Gets or sets the font of signature.  # noqa: E501

        :param font: The font of this SignTextOptionsData.  # noqa: E501
        :type: SignatureFontData
        """
        self._font = font
    @property
    def fore_color(self):
        """Gets the fore_color of this SignTextOptionsData.  # noqa: E501

        Gets or sets the fore color of signature.  # noqa: E501

        :return: The fore_color of this SignTextOptionsData.  # noqa: E501
        :rtype: Color
        """
        return self._fore_color

    @fore_color.setter
    def fore_color(self, fore_color):
        """Sets the fore_color of this SignTextOptionsData.

        Gets or sets the fore color of signature.  # noqa: E501

        :param fore_color: The fore_color of this SignTextOptionsData.  # noqa: E501
        :type: Color
        """
        self._fore_color = fore_color
    @property
    def border_color(self):
        """Gets the border_color of this SignTextOptionsData.  # noqa: E501

        Gets or sets the border color of signature.  # noqa: E501

        :return: The border_color of this SignTextOptionsData.  # noqa: E501
        :rtype: Color
        """
        return self._border_color

    @border_color.setter
    def border_color(self, border_color):
        """Sets the border_color of this SignTextOptionsData.

        Gets or sets the border color of signature.  # noqa: E501

        :param border_color: The border_color of this SignTextOptionsData.  # noqa: E501
        :type: Color
        """
        self._border_color = border_color
    @property
    def background_color(self):
        """Gets the background_color of this SignTextOptionsData.  # noqa: E501

        Gets or sets the background color of signature.  # noqa: E501

        :return: The background_color of this SignTextOptionsData.  # noqa: E501
        :rtype: Color
        """
        return self._background_color

    @background_color.setter
    def background_color(self, background_color):
        """Sets the background_color of this SignTextOptionsData.

        Gets or sets the background color of signature.  # noqa: E501

        :param background_color: The background_color of this SignTextOptionsData.  # noqa: E501
        :type: Color
        """
        self._background_color = background_color
    @property
    def background_brush(self):
        """Gets the background_brush of this SignTextOptionsData.  # noqa: E501

        Gets or sets the signature background brush. Value by default is null.  If this property has a value it will be used instead BackgroundBrush property.  # noqa: E501

        :return: The background_brush of this SignTextOptionsData.  # noqa: E501
        :rtype: BrushData
        """
        return self._background_brush

    @background_brush.setter
    def background_brush(self, background_brush):
        """Sets the background_brush of this SignTextOptionsData.

        Gets or sets the signature background brush. Value by default is null.  If this property has a value it will be used instead BackgroundBrush property.  # noqa: E501

        :param background_brush: The background_brush of this SignTextOptionsData.  # noqa: E501
        :type: BrushData
        """
        self._background_brush = background_brush
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
        if not isinstance(other, SignTextOptionsData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
