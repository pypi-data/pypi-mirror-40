# coding: utf-8
# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="PdfSignTextOptionsData.py">
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
class PdfSignTextOptionsData(SignTextOptionsData):
    """Represents the Text Sign Options for PDF Documents.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'opacity': 'float',
        'signature_id': 'int',
        'signature_implementation': 'str',
        'form_text_field_title': 'str',
        'form_text_field_type': 'str',
        'background_brush': 'BrushData',
        'text_horizontal_alignment': 'str',
        'text_vertical_alignment': 'str'
    }

    attribute_map = {
        'opacity': 'Opacity',
        'signature_id': 'SignatureID',
        'signature_implementation': 'SignatureImplementation',
        'form_text_field_title': 'FormTextFieldTitle',
        'form_text_field_type': 'FormTextFieldType',
        'background_brush': 'BackgroundBrush',
        'text_horizontal_alignment': 'TextHorizontalAlignment',
        'text_vertical_alignment': 'TextVerticalAlignment'
    }

    def __init__(self, opacity=None, signature_id=None, signature_implementation=None, form_text_field_title=None, form_text_field_type=None, background_brush=None, text_horizontal_alignment=None, text_vertical_alignment=None):  # noqa: E501
        """PdfSignTextOptionsData - a model defined in Swagger"""  # noqa: E501
        SignTextOptionsData.__init__(self)
        self.swagger_types.update(SignTextOptionsData.swagger_types)
        self.attribute_map.update(SignTextOptionsData.attribute_map)

        self._opacity = None
        self._signature_id = None
        self._signature_implementation = None
        self._form_text_field_title = None
        self._form_text_field_type = None
        self._background_brush = None
        self._text_horizontal_alignment = None
        self._text_vertical_alignment = None
        self.discriminator = None
        self.options_type = "PdfSignTextOptionsData"

        if opacity is not None:
            self.opacity = opacity
        if signature_id is not None:
            self.signature_id = signature_id
        if signature_implementation is not None:
            self.signature_implementation = signature_implementation
        if form_text_field_title is not None:
            self.form_text_field_title = form_text_field_title
        if form_text_field_type is not None:
            self.form_text_field_type = form_text_field_type
        if background_brush is not None:
            self.background_brush = background_brush
        if text_horizontal_alignment is not None:
            self.text_horizontal_alignment = text_horizontal_alignment
        if text_vertical_alignment is not None:
            self.text_vertical_alignment = text_vertical_alignment

    @property
    def opacity(self):
        """Gets the opacity of this PdfSignTextOptionsData.  # noqa: E501

        Gets or sets the signature opacity (value from 0.0 (clear) through 1.0 (opaque)). By default the value is 1.0.  # noqa: E501

        :return: The opacity of this PdfSignTextOptionsData.  # noqa: E501
        :rtype: float
        """
        return self._opacity

    @opacity.setter
    def opacity(self, opacity):
        """Sets the opacity of this PdfSignTextOptionsData.

        Gets or sets the signature opacity (value from 0.0 (clear) through 1.0 (opaque)). By default the value is 1.0.  # noqa: E501

        :param opacity: The opacity of this PdfSignTextOptionsData.  # noqa: E501
        :type: float
        """
        self._opacity = opacity
    @property
    def signature_id(self):
        """Gets the signature_id of this PdfSignTextOptionsData.  # noqa: E501

        Gets or sets the unique ID of signature. It can be used in signature verification options.  # noqa: E501

        :return: The signature_id of this PdfSignTextOptionsData.  # noqa: E501
        :rtype: int
        """
        return self._signature_id

    @signature_id.setter
    def signature_id(self, signature_id):
        """Sets the signature_id of this PdfSignTextOptionsData.

        Gets or sets the unique ID of signature. It can be used in signature verification options.  # noqa: E501

        :param signature_id: The signature_id of this PdfSignTextOptionsData.  # noqa: E501
        :type: int
        """
        self._signature_id = signature_id
    @property
    def signature_implementation(self):
        """Gets the signature_implementation of this PdfSignTextOptionsData.  # noqa: E501

        Gets or sets the type of text signature implementation.  # noqa: E501

        :return: The signature_implementation of this PdfSignTextOptionsData.  # noqa: E501
        :rtype: str
        """
        return self._signature_implementation

    @signature_implementation.setter
    def signature_implementation(self, signature_implementation):
        """Sets the signature_implementation of this PdfSignTextOptionsData.

        Gets or sets the type of text signature implementation.  # noqa: E501

        :param signature_implementation: The signature_implementation of this PdfSignTextOptionsData.  # noqa: E501
        :type: str
        """
        allowed_values = ["Stamp", "Image", "Annotation", "Sticker", "TextToFormField", "Watermark"]  # noqa: E501
        if not signature_implementation.isdigit():	
            if signature_implementation not in allowed_values:
                raise ValueError(
                    "Invalid value for `signature_implementation` ({0}), must be one of {1}"  # noqa: E501
                    .format(signature_implementation, allowed_values))
            self._signature_implementation = signature_implementation
        else:
            self._signature_implementation = allowed_values[int(signature_implementation) if six.PY3 else long(signature_implementation)]
    @property
    def form_text_field_title(self):
        """Gets the form_text_field_title of this PdfSignTextOptionsData.  # noqa: E501

        Gets or sets the title of text form field to put text signature into it. This property could be used only with PdfTextSignatureImplementation = TextToFormField.  # noqa: E501

        :return: The form_text_field_title of this PdfSignTextOptionsData.  # noqa: E501
        :rtype: str
        """
        return self._form_text_field_title

    @form_text_field_title.setter
    def form_text_field_title(self, form_text_field_title):
        """Sets the form_text_field_title of this PdfSignTextOptionsData.

        Gets or sets the title of text form field to put text signature into it. This property could be used only with PdfTextSignatureImplementation = TextToFormField.  # noqa: E501

        :param form_text_field_title: The form_text_field_title of this PdfSignTextOptionsData.  # noqa: E501
        :type: str
        """
        self._form_text_field_title = form_text_field_title
    @property
    def form_text_field_type(self):
        """Gets the form_text_field_type of this PdfSignTextOptionsData.  # noqa: E501

        Gets or sets the type of form field to put text signature into it. This property could be used only with PdfTextSignatureImplementation = TextToFormField. Value by default is AllTextTypes.  # noqa: E501

        :return: The form_text_field_type of this PdfSignTextOptionsData.  # noqa: E501
        :rtype: str
        """
        return self._form_text_field_type

    @form_text_field_type.setter
    def form_text_field_type(self, form_text_field_type):
        """Sets the form_text_field_type of this PdfSignTextOptionsData.

        Gets or sets the type of form field to put text signature into it. This property could be used only with PdfTextSignatureImplementation = TextToFormField. Value by default is AllTextTypes.  # noqa: E501

        :param form_text_field_type: The form_text_field_type of this PdfSignTextOptionsData.  # noqa: E501
        :type: str
        """
        allowed_values = ["AllTextTypes", "PlainText", "RichText"]  # noqa: E501
        if not form_text_field_type.isdigit():	
            if form_text_field_type not in allowed_values:
                raise ValueError(
                    "Invalid value for `form_text_field_type` ({0}), must be one of {1}"  # noqa: E501
                    .format(form_text_field_type, allowed_values))
            self._form_text_field_type = form_text_field_type
        else:
            self._form_text_field_type = allowed_values[int(form_text_field_type) if six.PY3 else long(form_text_field_type)]
    @property
    def background_brush(self):
        """Gets the background_brush of this PdfSignTextOptionsData.  # noqa: E501

        Gets or sets the signature background brush. Value by default is null.  When property has a value it is used instead BackgroundBrush property. For Stamp implementation LinearGradientBrush (ColorStart) and RadialGradientBrush (ColorInner) are used   as SolidBrush. It is not used for Annotation, Sticker, TextToFormField and Watermark implementations.  # noqa: E501

        :return: The background_brush of this PdfSignTextOptionsData.  # noqa: E501
        :rtype: BrushData
        """
        return self._background_brush

    @background_brush.setter
    def background_brush(self, background_brush):
        """Sets the background_brush of this PdfSignTextOptionsData.

        Gets or sets the signature background brush. Value by default is null.  When property has a value it is used instead BackgroundBrush property. For Stamp implementation LinearGradientBrush (ColorStart) and RadialGradientBrush (ColorInner) are used   as SolidBrush. It is not used for Annotation, Sticker, TextToFormField and Watermark implementations.  # noqa: E501

        :param background_brush: The background_brush of this PdfSignTextOptionsData.  # noqa: E501
        :type: BrushData
        """
        self._background_brush = background_brush
    @property
    def text_horizontal_alignment(self):
        """Gets the text_horizontal_alignment of this PdfSignTextOptionsData.  # noqa: E501

        Horizontal alignment of text inside a signature. This feature is supported only for Image and Annotation signature implementations  (see  SignatureImplementation property).  # noqa: E501

        :return: The text_horizontal_alignment of this PdfSignTextOptionsData.  # noqa: E501
        :rtype: str
        """
        return self._text_horizontal_alignment

    @text_horizontal_alignment.setter
    def text_horizontal_alignment(self, text_horizontal_alignment):
        """Sets the text_horizontal_alignment of this PdfSignTextOptionsData.

        Horizontal alignment of text inside a signature. This feature is supported only for Image and Annotation signature implementations  (see  SignatureImplementation property).  # noqa: E501

        :param text_horizontal_alignment: The text_horizontal_alignment of this PdfSignTextOptionsData.  # noqa: E501
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
        """Gets the text_vertical_alignment of this PdfSignTextOptionsData.  # noqa: E501

        Vertical alignment of text inside a signature. This feature is supported only for Image signature implementation  (see  SignatureImplementation property).          # noqa: E501

        :return: The text_vertical_alignment of this PdfSignTextOptionsData.  # noqa: E501
        :rtype: str
        """
        return self._text_vertical_alignment

    @text_vertical_alignment.setter
    def text_vertical_alignment(self, text_vertical_alignment):
        """Sets the text_vertical_alignment of this PdfSignTextOptionsData.

        Vertical alignment of text inside a signature. This feature is supported only for Image signature implementation  (see  SignatureImplementation property).          # noqa: E501

        :param text_vertical_alignment: The text_vertical_alignment of this PdfSignTextOptionsData.  # noqa: E501
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
        if not isinstance(other, PdfSignTextOptionsData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
