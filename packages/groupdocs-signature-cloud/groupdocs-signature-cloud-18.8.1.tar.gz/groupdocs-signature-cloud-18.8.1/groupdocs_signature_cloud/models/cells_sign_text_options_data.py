# coding: utf-8
# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="CellsSignTextOptionsData.py">
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
class CellsSignTextOptionsData(SignTextOptionsData):
    """Represents the Text Sign Options for Cells Documents.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'document_page_number': 'int',
        'top': 'int',
        'left': 'int',
        'margin': 'PaddingData',
        'background_brush': 'BrushData',
        'sheet_number': 'int',
        'row_number': 'int',
        'column_number': 'int',
        'border_visiblity': 'bool',
        'border_dash_style': 'str',
        'border_transparency': 'float',
        'border_weight': 'float',
        'background_transparency': 'float',
        'signature_implementation': 'str',
        'text_horizontal_alignment': 'str',
        'text_vertical_alignment': 'str'
    }

    attribute_map = {
        'document_page_number': 'DocumentPageNumber',
        'top': 'Top',
        'left': 'Left',
        'margin': 'Margin',
        'background_brush': 'BackgroundBrush',
        'sheet_number': 'SheetNumber',
        'row_number': 'RowNumber',
        'column_number': 'ColumnNumber',
        'border_visiblity': 'BorderVisiblity',
        'border_dash_style': 'BorderDashStyle',
        'border_transparency': 'BorderTransparency',
        'border_weight': 'BorderWeight',
        'background_transparency': 'BackgroundTransparency',
        'signature_implementation': 'SignatureImplementation',
        'text_horizontal_alignment': 'TextHorizontalAlignment',
        'text_vertical_alignment': 'TextVerticalAlignment'
    }

    def __init__(self, document_page_number=None, top=None, left=None, margin=None, background_brush=None, sheet_number=None, row_number=None, column_number=None, border_visiblity=None, border_dash_style=None, border_transparency=None, border_weight=None, background_transparency=None, signature_implementation=None, text_horizontal_alignment=None, text_vertical_alignment=None):  # noqa: E501
        """CellsSignTextOptionsData - a model defined in Swagger"""  # noqa: E501
        SignTextOptionsData.__init__(self)
        self.swagger_types.update(SignTextOptionsData.swagger_types)
        self.attribute_map.update(SignTextOptionsData.attribute_map)

        self._document_page_number = None
        self._top = None
        self._left = None
        self._margin = None
        self._background_brush = None
        self._sheet_number = None
        self._row_number = None
        self._column_number = None
        self._border_visiblity = None
        self._border_dash_style = None
        self._border_transparency = None
        self._border_weight = None
        self._background_transparency = None
        self._signature_implementation = None
        self._text_horizontal_alignment = None
        self._text_vertical_alignment = None
        self.discriminator = None
        self.options_type = "CellsSignTextOptionsData"

        if document_page_number is not None:
            self.document_page_number = document_page_number
        if top is not None:
            self.top = top
        if left is not None:
            self.left = left
        if margin is not None:
            self.margin = margin
        if background_brush is not None:
            self.background_brush = background_brush
        if sheet_number is not None:
            self.sheet_number = sheet_number
        if row_number is not None:
            self.row_number = row_number
        if column_number is not None:
            self.column_number = column_number
        if border_visiblity is not None:
            self.border_visiblity = border_visiblity
        if border_dash_style is not None:
            self.border_dash_style = border_dash_style
        if border_transparency is not None:
            self.border_transparency = border_transparency
        if border_weight is not None:
            self.border_weight = border_weight
        if background_transparency is not None:
            self.background_transparency = background_transparency
        if signature_implementation is not None:
            self.signature_implementation = signature_implementation
        if text_horizontal_alignment is not None:
            self.text_horizontal_alignment = text_horizontal_alignment
        if text_vertical_alignment is not None:
            self.text_vertical_alignment = text_vertical_alignment

    @property
    def document_page_number(self):
        """Gets the document_page_number of this CellsSignTextOptionsData.  # noqa: E501

        Gets or sets worksheet number for signing. Minimal value is 1.  # noqa: E501

        :return: The document_page_number of this CellsSignTextOptionsData.  # noqa: E501
        :rtype: int
        """
        return self._document_page_number

    @document_page_number.setter
    def document_page_number(self, document_page_number):
        """Sets the document_page_number of this CellsSignTextOptionsData.

        Gets or sets worksheet number for signing. Minimal value is 1.  # noqa: E501

        :param document_page_number: The document_page_number of this CellsSignTextOptionsData.  # noqa: E501
        :type: int
        """
        self._document_page_number = document_page_number
    @property
    def top(self):
        """Gets the top of this CellsSignTextOptionsData.  # noqa: E501

        Gets or sets the position of the top edge of the Signature area in pixels. This property is mutually exclusive with Row property. If Top property is set RowNumber will be reset to 0.  # noqa: E501

        :return: The top of this CellsSignTextOptionsData.  # noqa: E501
        :rtype: int
        """
        return self._top

    @top.setter
    def top(self, top):
        """Sets the top of this CellsSignTextOptionsData.

        Gets or sets the position of the top edge of the Signature area in pixels. This property is mutually exclusive with Row property. If Top property is set RowNumber will be reset to 0.  # noqa: E501

        :param top: The top of this CellsSignTextOptionsData.  # noqa: E501
        :type: int
        """
        self._top = top
    @property
    def left(self):
        """Gets the left of this CellsSignTextOptionsData.  # noqa: E501

        Gets or sets the position of the left edge of the Signature area in pixels. This property is mutually exclusive with Column property. If Left property is set ColumnNumber will be reset to 0.  # noqa: E501

        :return: The left of this CellsSignTextOptionsData.  # noqa: E501
        :rtype: int
        """
        return self._left

    @left.setter
    def left(self, left):
        """Sets the left of this CellsSignTextOptionsData.

        Gets or sets the position of the left edge of the Signature area in pixels. This property is mutually exclusive with Column property. If Left property is set ColumnNumber will be reset to 0.  # noqa: E501

        :param left: The left of this CellsSignTextOptionsData.  # noqa: E501
        :type: int
        """
        self._left = left
    @property
    def margin(self):
        """Gets the margin of this CellsSignTextOptionsData.  # noqa: E501

        Gets or sets the space between Sign and worksheet edges. (works ONLY if horizontal or vertical alignment are specified).  # noqa: E501

        :return: The margin of this CellsSignTextOptionsData.  # noqa: E501
        :rtype: PaddingData
        """
        return self._margin

    @margin.setter
    def margin(self, margin):
        """Sets the margin of this CellsSignTextOptionsData.

        Gets or sets the space between Sign and worksheet edges. (works ONLY if horizontal or vertical alignment are specified).  # noqa: E501

        :param margin: The margin of this CellsSignTextOptionsData.  # noqa: E501
        :type: PaddingData
        """
        self._margin = margin
    @property
    def background_brush(self):
        """Gets the background_brush of this CellsSignTextOptionsData.  # noqa: E501

        Gets or sets the signature background brush. Value by default is null.  When property has a value it is used instead BackgroundBrush property. For TextStamp implementation RadialGradientBrush is not applicable, it is replaced by LinearGradientBrush. It is not used for Watermark implementation.  # noqa: E501

        :return: The background_brush of this CellsSignTextOptionsData.  # noqa: E501
        :rtype: BrushData
        """
        return self._background_brush

    @background_brush.setter
    def background_brush(self, background_brush):
        """Sets the background_brush of this CellsSignTextOptionsData.

        Gets or sets the signature background brush. Value by default is null.  When property has a value it is used instead BackgroundBrush property. For TextStamp implementation RadialGradientBrush is not applicable, it is replaced by LinearGradientBrush. It is not used for Watermark implementation.  # noqa: E501

        :param background_brush: The background_brush of this CellsSignTextOptionsData.  # noqa: E501
        :type: BrushData
        """
        self._background_brush = background_brush
    @property
    def sheet_number(self):
        """Gets the sheet_number of this CellsSignTextOptionsData.  # noqa: E501

        Gets or sets worksheet number for signing. DocumentPageNumber parameter contains the same value.  # noqa: E501

        :return: The sheet_number of this CellsSignTextOptionsData.  # noqa: E501
        :rtype: int
        """
        return self._sheet_number

    @sheet_number.setter
    def sheet_number(self, sheet_number):
        """Sets the sheet_number of this CellsSignTextOptionsData.

        Gets or sets worksheet number for signing. DocumentPageNumber parameter contains the same value.  # noqa: E501

        :param sheet_number: The sheet_number of this CellsSignTextOptionsData.  # noqa: E501
        :type: int
        """
        self._sheet_number = sheet_number
    @property
    def row_number(self):
        """Gets the row_number of this CellsSignTextOptionsData.  # noqa: E501

        Gets or sets the top row number of signature (min value is 0). Top parameter contains the same value.  # noqa: E501

        :return: The row_number of this CellsSignTextOptionsData.  # noqa: E501
        :rtype: int
        """
        return self._row_number

    @row_number.setter
    def row_number(self, row_number):
        """Sets the row_number of this CellsSignTextOptionsData.

        Gets or sets the top row number of signature (min value is 0). Top parameter contains the same value.  # noqa: E501

        :param row_number: The row_number of this CellsSignTextOptionsData.  # noqa: E501
        :type: int
        """
        self._row_number = row_number
    @property
    def column_number(self):
        """Gets the column_number of this CellsSignTextOptionsData.  # noqa: E501

        Gets or sets the left column number of signature (min value is 0). Left parameter contains the same value.  # noqa: E501

        :return: The column_number of this CellsSignTextOptionsData.  # noqa: E501
        :rtype: int
        """
        return self._column_number

    @column_number.setter
    def column_number(self, column_number):
        """Sets the column_number of this CellsSignTextOptionsData.

        Gets or sets the left column number of signature (min value is 0). Left parameter contains the same value.  # noqa: E501

        :param column_number: The column_number of this CellsSignTextOptionsData.  # noqa: E501
        :type: int
        """
        self._column_number = column_number
    @property
    def border_visiblity(self):
        """Gets the border_visiblity of this CellsSignTextOptionsData.  # noqa: E501

        Gets or sets the signature border visibility.  # noqa: E501

        :return: The border_visiblity of this CellsSignTextOptionsData.  # noqa: E501
        :rtype: bool
        """
        return self._border_visiblity

    @border_visiblity.setter
    def border_visiblity(self, border_visiblity):
        """Sets the border_visiblity of this CellsSignTextOptionsData.

        Gets or sets the signature border visibility.  # noqa: E501

        :param border_visiblity: The border_visiblity of this CellsSignTextOptionsData.  # noqa: E501
        :type: bool
        """
        self._border_visiblity = border_visiblity
    @property
    def border_dash_style(self):
        """Gets the border_dash_style of this CellsSignTextOptionsData.  # noqa: E501

        Gets or sets the signature border style.  # noqa: E501

        :return: The border_dash_style of this CellsSignTextOptionsData.  # noqa: E501
        :rtype: str
        """
        return self._border_dash_style

    @border_dash_style.setter
    def border_dash_style(self, border_dash_style):
        """Sets the border_dash_style of this CellsSignTextOptionsData.

        Gets or sets the signature border style.  # noqa: E501

        :param border_dash_style: The border_dash_style of this CellsSignTextOptionsData.  # noqa: E501
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
    def border_transparency(self):
        """Gets the border_transparency of this CellsSignTextOptionsData.  # noqa: E501

        Gets or sets the signature border transparency (value from 0.0 (opaque) through 1.0 (clear)).  # noqa: E501

        :return: The border_transparency of this CellsSignTextOptionsData.  # noqa: E501
        :rtype: float
        """
        return self._border_transparency

    @border_transparency.setter
    def border_transparency(self, border_transparency):
        """Sets the border_transparency of this CellsSignTextOptionsData.

        Gets or sets the signature border transparency (value from 0.0 (opaque) through 1.0 (clear)).  # noqa: E501

        :param border_transparency: The border_transparency of this CellsSignTextOptionsData.  # noqa: E501
        :type: float
        """
        self._border_transparency = border_transparency
    @property
    def border_weight(self):
        """Gets the border_weight of this CellsSignTextOptionsData.  # noqa: E501

        Gets or sets the weight of the signature border.   # noqa: E501

        :return: The border_weight of this CellsSignTextOptionsData.  # noqa: E501
        :rtype: float
        """
        return self._border_weight

    @border_weight.setter
    def border_weight(self, border_weight):
        """Sets the border_weight of this CellsSignTextOptionsData.

        Gets or sets the weight of the signature border.   # noqa: E501

        :param border_weight: The border_weight of this CellsSignTextOptionsData.  # noqa: E501
        :type: float
        """
        self._border_weight = border_weight
    @property
    def background_transparency(self):
        """Gets the background_transparency of this CellsSignTextOptionsData.  # noqa: E501

        Gets or sets the signature background transparency (value from 0.0 (opaque) through 1.0 (clear)).  # noqa: E501

        :return: The background_transparency of this CellsSignTextOptionsData.  # noqa: E501
        :rtype: float
        """
        return self._background_transparency

    @background_transparency.setter
    def background_transparency(self, background_transparency):
        """Sets the background_transparency of this CellsSignTextOptionsData.

        Gets or sets the signature background transparency (value from 0.0 (opaque) through 1.0 (clear)).  # noqa: E501

        :param background_transparency: The background_transparency of this CellsSignTextOptionsData.  # noqa: E501
        :type: float
        """
        self._background_transparency = background_transparency
    @property
    def signature_implementation(self):
        """Gets the signature_implementation of this CellsSignTextOptionsData.  # noqa: E501

        Gets or sets the type of text signature implementation.  # noqa: E501

        :return: The signature_implementation of this CellsSignTextOptionsData.  # noqa: E501
        :rtype: str
        """
        return self._signature_implementation

    @signature_implementation.setter
    def signature_implementation(self, signature_implementation):
        """Sets the signature_implementation of this CellsSignTextOptionsData.

        Gets or sets the type of text signature implementation.  # noqa: E501

        :param signature_implementation: The signature_implementation of this CellsSignTextOptionsData.  # noqa: E501
        :type: str
        """
        allowed_values = ["TextStamp", "TextAsImage"]  # noqa: E501
        if not signature_implementation.isdigit():	
            if signature_implementation not in allowed_values:
                raise ValueError(
                    "Invalid value for `signature_implementation` ({0}), must be one of {1}"  # noqa: E501
                    .format(signature_implementation, allowed_values))
            self._signature_implementation = signature_implementation
        else:
            self._signature_implementation = allowed_values[int(signature_implementation) if six.PY3 else long(signature_implementation)]
    @property
    def text_horizontal_alignment(self):
        """Gets the text_horizontal_alignment of this CellsSignTextOptionsData.  # noqa: E501

        Horizontal alignment of text inside a signature.  # noqa: E501

        :return: The text_horizontal_alignment of this CellsSignTextOptionsData.  # noqa: E501
        :rtype: str
        """
        return self._text_horizontal_alignment

    @text_horizontal_alignment.setter
    def text_horizontal_alignment(self, text_horizontal_alignment):
        """Sets the text_horizontal_alignment of this CellsSignTextOptionsData.

        Horizontal alignment of text inside a signature.  # noqa: E501

        :param text_horizontal_alignment: The text_horizontal_alignment of this CellsSignTextOptionsData.  # noqa: E501
        :type: str
        """
        allowed_values = ["Left", "Center", "Right"]  # noqa: E501
        if not text_horizontal_alignment.isdigit():	
            if text_horizontal_alignment not in allowed_values:
                raise ValueError(
                    "Invalid value for `text_horizontal_alignment` ({0}), must be one of {1}"  # noqa: E501
                    .format(text_horizontal_alignment, allowed_values))
            self._text_horizontal_alignment = text_horizontal_alignment
        else:
            self._text_horizontal_alignment = allowed_values[int(text_horizontal_alignment) if six.PY3 else long(text_horizontal_alignment)]
    @property
    def text_vertical_alignment(self):
        """Gets the text_vertical_alignment of this CellsSignTextOptionsData.  # noqa: E501

        Vertical alignment of text inside a signature.  # noqa: E501

        :return: The text_vertical_alignment of this CellsSignTextOptionsData.  # noqa: E501
        :rtype: str
        """
        return self._text_vertical_alignment

    @text_vertical_alignment.setter
    def text_vertical_alignment(self, text_vertical_alignment):
        """Sets the text_vertical_alignment of this CellsSignTextOptionsData.

        Vertical alignment of text inside a signature.  # noqa: E501

        :param text_vertical_alignment: The text_vertical_alignment of this CellsSignTextOptionsData.  # noqa: E501
        :type: str
        """
        allowed_values = ["Top", "Center", "Bottom"]  # noqa: E501
        if not text_vertical_alignment.isdigit():	
            if text_vertical_alignment not in allowed_values:
                raise ValueError(
                    "Invalid value for `text_vertical_alignment` ({0}), must be one of {1}"  # noqa: E501
                    .format(text_vertical_alignment, allowed_values))
            self._text_vertical_alignment = text_vertical_alignment
        else:
            self._text_vertical_alignment = allowed_values[int(text_vertical_alignment) if six.PY3 else long(text_vertical_alignment)]
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
        if not isinstance(other, CellsSignTextOptionsData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
