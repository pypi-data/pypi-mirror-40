# coding: utf-8
# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="SignQRCodeOptionsData.py">
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

from groupdocs_signature_cloud.models import SignTextOptionsData
class SignQRCodeOptionsData(SignTextOptionsData):
    """Represents the QRCode Signature Options.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'qr_code_type_name': 'str',
        'fore_color': 'Color',
        'border_color': 'Color',
        'background_color': 'Color',
        'background_brush': 'BrushData',
        'border_visiblity': 'bool',
        'border_dash_style': 'str',
        'border_weight': 'float',
        'opacity': 'float',
        'code_text_alignment': 'str',
        'inner_margins': 'PaddingData',
        'logo_guid': 'str'
    }

    attribute_map = {
        'qr_code_type_name': 'QRCodeTypeName',
        'fore_color': 'ForeColor',
        'border_color': 'BorderColor',
        'background_color': 'BackgroundColor',
        'background_brush': 'BackgroundBrush',
        'border_visiblity': 'BorderVisiblity',
        'border_dash_style': 'BorderDashStyle',
        'border_weight': 'BorderWeight',
        'opacity': 'Opacity',
        'code_text_alignment': 'CodeTextAlignment',
        'inner_margins': 'InnerMargins',
        'logo_guid': 'LogoGuid'
    }

    def __init__(self, qr_code_type_name=None, fore_color=None, border_color=None, background_color=None, background_brush=None, border_visiblity=None, border_dash_style=None, border_weight=None, opacity=None, code_text_alignment=None, inner_margins=None, logo_guid=None):  # noqa: E501
        """SignQRCodeOptionsData - a model defined in Swagger"""  # noqa: E501
        SignTextOptionsData.__init__(self)
        self.swagger_types.update(SignTextOptionsData.swagger_types)
        self.attribute_map.update(SignTextOptionsData.attribute_map)

        self._qr_code_type_name = None
        self._fore_color = None
        self._border_color = None
        self._background_color = None
        self._background_brush = None
        self._border_visiblity = None
        self._border_dash_style = None
        self._border_weight = None
        self._opacity = None
        self._code_text_alignment = None
        self._inner_margins = None
        self._logo_guid = None
        self.discriminator = None
        self.options_type = "SignQRCodeOptionsData"

        if qr_code_type_name is not None:
            self.qr_code_type_name = qr_code_type_name
        if fore_color is not None:
            self.fore_color = fore_color
        if border_color is not None:
            self.border_color = border_color
        if background_color is not None:
            self.background_color = background_color
        if background_brush is not None:
            self.background_brush = background_brush
        if border_visiblity is not None:
            self.border_visiblity = border_visiblity
        if border_dash_style is not None:
            self.border_dash_style = border_dash_style
        if border_weight is not None:
            self.border_weight = border_weight
        if opacity is not None:
            self.opacity = opacity
        if code_text_alignment is not None:
            self.code_text_alignment = code_text_alignment
        if inner_margins is not None:
            self.inner_margins = inner_margins
        if logo_guid is not None:
            self.logo_guid = logo_guid

    @property
    def qr_code_type_name(self):
        """Gets the qr_code_type_name of this SignQRCodeOptionsData.  # noqa: E501

        Get or set QRCode type. Pick one from supported QRCode Types list.  # noqa: E501

        :return: The qr_code_type_name of this SignQRCodeOptionsData.  # noqa: E501
        :rtype: str
        """
        return self._qr_code_type_name

    @qr_code_type_name.setter
    def qr_code_type_name(self, qr_code_type_name):
        """Sets the qr_code_type_name of this SignQRCodeOptionsData.

        Get or set QRCode type. Pick one from supported QRCode Types list.  # noqa: E501

        :param qr_code_type_name: The qr_code_type_name of this SignQRCodeOptionsData.  # noqa: E501
        :type: str
        """
        self._qr_code_type_name = qr_code_type_name
    @property
    def fore_color(self):
        """Gets the fore_color of this SignQRCodeOptionsData.  # noqa: E501

        Gets or sets the Fore color of Barcode bars Using of this property could cause problems with verification. Use it carefully with maximum contrast with background.  # noqa: E501

        :return: The fore_color of this SignQRCodeOptionsData.  # noqa: E501
        :rtype: Color
        """
        return self._fore_color

    @fore_color.setter
    def fore_color(self, fore_color):
        """Sets the fore_color of this SignQRCodeOptionsData.

        Gets or sets the Fore color of Barcode bars Using of this property could cause problems with verification. Use it carefully with maximum contrast with background.  # noqa: E501

        :param fore_color: The fore_color of this SignQRCodeOptionsData.  # noqa: E501
        :type: Color
        """
        self._fore_color = fore_color
    @property
    def border_color(self):
        """Gets the border_color of this SignQRCodeOptionsData.  # noqa: E501

        Gets or sets the border color of signature. Using of this property could cause problems with verification. Use it carefully with maximum contrast with background.  # noqa: E501

        :return: The border_color of this SignQRCodeOptionsData.  # noqa: E501
        :rtype: Color
        """
        return self._border_color

    @border_color.setter
    def border_color(self, border_color):
        """Sets the border_color of this SignQRCodeOptionsData.

        Gets or sets the border color of signature. Using of this property could cause problems with verification. Use it carefully with maximum contrast with background.  # noqa: E501

        :param border_color: The border_color of this SignQRCodeOptionsData.  # noqa: E501
        :type: Color
        """
        self._border_color = border_color
    @property
    def background_color(self):
        """Gets the background_color of this SignQRCodeOptionsData.  # noqa: E501

        Gets or sets the background color of signature. Using of this property could cause problems with verification. Use it carefully with maximum contrast with background.  # noqa: E501

        :return: The background_color of this SignQRCodeOptionsData.  # noqa: E501
        :rtype: Color
        """
        return self._background_color

    @background_color.setter
    def background_color(self, background_color):
        """Sets the background_color of this SignQRCodeOptionsData.

        Gets or sets the background color of signature. Using of this property could cause problems with verification. Use it carefully with maximum contrast with background.  # noqa: E501

        :param background_color: The background_color of this SignQRCodeOptionsData.  # noqa: E501
        :type: Color
        """
        self._background_color = background_color
    @property
    def background_brush(self):
        """Gets the background_brush of this SignQRCodeOptionsData.  # noqa: E501

        Gets or sets the signature background brush. Value by default is null.  When property has a value it is used instead BackgroundBrush property. BackgroundBrush has limited scope of application for Qr-codes. SolidBrush, LinearGradientBrush (ColorStart) and RadialGradientBrush (ColorInner) are used   instead BackgroundColor. TextureBrush is not used.  # noqa: E501

        :return: The background_brush of this SignQRCodeOptionsData.  # noqa: E501
        :rtype: BrushData
        """
        return self._background_brush

    @background_brush.setter
    def background_brush(self, background_brush):
        """Sets the background_brush of this SignQRCodeOptionsData.

        Gets or sets the signature background brush. Value by default is null.  When property has a value it is used instead BackgroundBrush property. BackgroundBrush has limited scope of application for Qr-codes. SolidBrush, LinearGradientBrush (ColorStart) and RadialGradientBrush (ColorInner) are used   instead BackgroundColor. TextureBrush is not used.  # noqa: E501

        :param background_brush: The background_brush of this SignQRCodeOptionsData.  # noqa: E501
        :type: BrushData
        """
        self._background_brush = background_brush
    @property
    def border_visiblity(self):
        """Gets the border_visiblity of this SignQRCodeOptionsData.  # noqa: E501

        Gets or sets the signature border visibility.  # noqa: E501

        :return: The border_visiblity of this SignQRCodeOptionsData.  # noqa: E501
        :rtype: bool
        """
        return self._border_visiblity

    @border_visiblity.setter
    def border_visiblity(self, border_visiblity):
        """Sets the border_visiblity of this SignQRCodeOptionsData.

        Gets or sets the signature border visibility.  # noqa: E501

        :param border_visiblity: The border_visiblity of this SignQRCodeOptionsData.  # noqa: E501
        :type: bool
        """
        self._border_visiblity = border_visiblity
    @property
    def border_dash_style(self):
        """Gets the border_dash_style of this SignQRCodeOptionsData.  # noqa: E501

        Gets or sets the signature border style.  # noqa: E501

        :return: The border_dash_style of this SignQRCodeOptionsData.  # noqa: E501
        :rtype: str
        """
        return self._border_dash_style

    @border_dash_style.setter
    def border_dash_style(self, border_dash_style):
        """Sets the border_dash_style of this SignQRCodeOptionsData.

        Gets or sets the signature border style.  # noqa: E501

        :param border_dash_style: The border_dash_style of this SignQRCodeOptionsData.  # noqa: E501
        :type: str
        """
        allowed_values = ["Dash", "DashDot", "DashDotDot", "DashLongDash", "DashLongDashDot", "RoundDot", "Solid", "SquareDot"]  # noqa: E501
        if not border_dash_style.isdigit():	
            if border_dash_style not in allowed_values:
                raise ValueError(
                    "Invalid value for `border_dash_style` ({0}), must be one of {1}"  # noqa: E501
                    .format(border_dash_style, allowed_values))
            self._border_dash_style = border_dash_style
        else:
            self._border_dash_style = allowed_values[int(border_dash_style) if six.PY3 else long(border_dash_style)]
    @property
    def border_weight(self):
        """Gets the border_weight of this SignQRCodeOptionsData.  # noqa: E501

        Gets or sets the weight of the signature border.   # noqa: E501

        :return: The border_weight of this SignQRCodeOptionsData.  # noqa: E501
        :rtype: float
        """
        return self._border_weight

    @border_weight.setter
    def border_weight(self, border_weight):
        """Sets the border_weight of this SignQRCodeOptionsData.

        Gets or sets the weight of the signature border.   # noqa: E501

        :param border_weight: The border_weight of this SignQRCodeOptionsData.  # noqa: E501
        :type: float
        """
        self._border_weight = border_weight
    @property
    def opacity(self):
        """Gets the opacity of this SignQRCodeOptionsData.  # noqa: E501

        Gets or sets the signature opacity (value from 0.0 (clear) through 1.0 (opaque)). By default the value is 1.0.  # noqa: E501

        :return: The opacity of this SignQRCodeOptionsData.  # noqa: E501
        :rtype: float
        """
        return self._opacity

    @opacity.setter
    def opacity(self, opacity):
        """Sets the opacity of this SignQRCodeOptionsData.

        Gets or sets the signature opacity (value from 0.0 (clear) through 1.0 (opaque)). By default the value is 1.0.  # noqa: E501

        :param opacity: The opacity of this SignQRCodeOptionsData.  # noqa: E501
        :type: float
        """
        self._opacity = opacity
    @property
    def code_text_alignment(self):
        """Gets the code_text_alignment of this SignQRCodeOptionsData.  # noqa: E501

        Gets or sets the alignment of text in the result QRCode. Default value is None.  # noqa: E501

        :return: The code_text_alignment of this SignQRCodeOptionsData.  # noqa: E501
        :rtype: str
        """
        return self._code_text_alignment

    @code_text_alignment.setter
    def code_text_alignment(self, code_text_alignment):
        """Sets the code_text_alignment of this SignQRCodeOptionsData.

        Gets or sets the alignment of text in the result QRCode. Default value is None.  # noqa: E501

        :param code_text_alignment: The code_text_alignment of this SignQRCodeOptionsData.  # noqa: E501
        :type: str
        """
        allowed_values = ["None", "Above", "Below", "Right"]  # noqa: E501
        if not code_text_alignment.isdigit():	
            if code_text_alignment not in allowed_values:
                raise ValueError(
                    "Invalid value for `code_text_alignment` ({0}), must be one of {1}"  # noqa: E501
                    .format(code_text_alignment, allowed_values))
            self._code_text_alignment = code_text_alignment
        else:
            self._code_text_alignment = allowed_values[int(code_text_alignment) if six.PY3 else long(code_text_alignment)]
    @property
    def inner_margins(self):
        """Gets the inner_margins of this SignQRCodeOptionsData.  # noqa: E501

        Gets or sets the space between QRCode elements and result image borders.  # noqa: E501

        :return: The inner_margins of this SignQRCodeOptionsData.  # noqa: E501
        :rtype: PaddingData
        """
        return self._inner_margins

    @inner_margins.setter
    def inner_margins(self, inner_margins):
        """Sets the inner_margins of this SignQRCodeOptionsData.

        Gets or sets the space between QRCode elements and result image borders.  # noqa: E501

        :param inner_margins: The inner_margins of this SignQRCodeOptionsData.  # noqa: E501
        :type: PaddingData
        """
        self._inner_margins = inner_margins
    @property
    def logo_guid(self):
        """Gets the logo_guid of this SignQRCodeOptionsData.  # noqa: E501

        Gets or sets the QR-code logo image file name. This property in use only if LogoStream is not specified. Using of this property could cause problems with verification. Use it carefully.  # noqa: E501

        :return: The logo_guid of this SignQRCodeOptionsData.  # noqa: E501
        :rtype: str
        """
        return self._logo_guid

    @logo_guid.setter
    def logo_guid(self, logo_guid):
        """Sets the logo_guid of this SignQRCodeOptionsData.

        Gets or sets the QR-code logo image file name. This property in use only if LogoStream is not specified. Using of this property could cause problems with verification. Use it carefully.  # noqa: E501

        :param logo_guid: The logo_guid of this SignQRCodeOptionsData.  # noqa: E501
        :type: str
        """
        self._logo_guid = logo_guid
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
        if not isinstance(other, SignQRCodeOptionsData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
