# GroupDocs.Signature Cloud SDK for Python
This repository contains GroupDocs.Signature Cloud SDK for Python source code. This SDK allows you to work with GroupDocs.Signature Cloud REST APIs in your PHP applications.

## Authorization
To use SDK you need AppSID and AppKey authorization keys. You can your AppSID and AppKey at https://dashboard.groupdocs.cloud (free registration is required).  

## Key Features
* Sign Documents (over 20+ supported formats) with different siganture types 
* - Text Signatures with various format, styles and appearances
* - Image Signatures with additional features according appearances and filters
* - Digital Signatures based on certificates 
* - Barcode Signatures with different Barcode types and appearences
* - QRCode Signatures with different QRCode types and appearences
* - Metadata Signatures with different data types
* - Customer Data Signatures encoded by QRCodes and encrypted with custom algorithms

* Verify Documents for signatures 
* - Text Signatures with verification on text 
* - Digital Signatures with certificates verification 
* - Barcode Signatures
* - QRCode Signatures

* Search for Signatures in Documents
* - Digital Signatures
* - Barcode Signatures
* - QRCode Signatures
* - Metadata Signatures
* - Customer Data Signatures encoded and encrypted

See [API Reference](https://docs.groupdocs.cloud/display/signaturecloud/Home) for full API specification.

## How to use the SDK?
The complete source code is available in this repository folder. You can either directly use it in your project via source code or get [PyPi](https://pypi.org/project/groupdocs_signature_cloud) (recommended). For more details, please visit our [documentation website](https://docs.groupdocs.cloud/display/signaturecloud/Home).

### Prerequisites

To use GroupDocs Signature Cloud SDK you need to register an account with [GroupDocs Cloud](https://www.groupdocs.cloud/) and lookup/create App Key and SID at [Cloud Dashboard](https://dashboard.groupdocs.cloud/#/apps). There is free quota available. For more details, see [GroupDocs Cloud Pricing](https://purchase.groupdocs.cloud/pricing).

## Installation & Usage
### pip install

If the python package is hosted on Github, you can install directly from Github

```sh
pip install groupdocs_signature_cloud
```
(you may need to run `pip` with root permission: `sudo pip install groupdocs_signature_cloud`)

Then import the package:
```python
import groupdocs_signature_cloud
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import groupdocs_signature_cloud
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python
        import asposestoragecloud
        import groupdocs_signature_cloud
        from groupdocs_signature_cloud.models.requests.post_search_barcode_request import PostSearchBarcodeRequest
        from groupdocs_signature_cloud.models import *

        host = "http://api-qa.groupdocs.cloud"   # Put your Host URL here
        base_url = "http://api-qa.groupdocs.cloud/v1" #Put your Base URL here
        api_key = "" #Put your App Key here
        app_sid = "" #Put your App Sid here
        storageName = "Signature-Dev" #Put your storage name here
        storageFolder = "signed" #Put your storage folder path here
        storageFileName = "SignedForVerificationAll.pdf" #Put your storage file name here
        filePassword = "" #Put your file password here if file is encrypted
        localFilePath = "C:\\SignedForVerificationAll.pdf" #Put your local file path here

        # File uploading (it could be skipped if file is already uploaded)
        # initialization of configuration for storage api client
        storageConfiguration = asposestoragecloud.Configuration()
        storageConfiguration.host = host
        storageConfiguration.base_url = base_url
        storageConfiguration.api_key_prefix = "Bearer"

        # initialization of storage api client
        storageApiClient = asposestoragecloud.ApiClient(apiKey = api_key, appSid = app_sid, configuration = storageConfiguration)
        storageApi = asposestoragecloud.apis.StorageApi(storageApiClient)
        # file uploading
        filestream = open(file = localFilePath, mode = "rb")
        storageApi.put_create(path = storageFolder + "\\" + storageFileName, file = filestream, storage = storageName)      
        filestream.close()    
        print("Uploaded: " + storageFolder + "\\" + storageFileName)     

        # Signature search
        # initialization of configuration for signature api client
        configuration = groupdocs_signature_cloud.Configuration()
        configuration.host = host
        configuration.base_url = base_url
        configuration.api_key["api_key"] = api_key
        configuration.api_key["app_sid"] = app_sid
        
        # initialization of signature api client
        signatureApi = groupdocs_signature_cloud.SignatureApi(configuration=configuration)

        # initialization of search options
        options = PdfSearchBarcodeOptionsData()
        # set barcode properties
        options.barcode_type_name ="Code39Standard"
        options.text = "12345678"
        # set match type
        options.match_type ="Contains"
        #set pages for search
        options.document_page_number = 1

        # initialization of search request
        request = PostSearchBarcodeRequest(storageFileName, options, filePassword, storageFolder, storageName)

        # getting response
        response = signatureApi.post_search_barcode(request)
        
        # checking response
        self.assertNotEqual(response, False)
        self.assertEqual(response.code, "200")
        self.assertEqual(response.status, "OK")
        self.assertIn(storageFileName, response.file_name)
        self.assertEqual(response.folder, storageFolder)
        self.assertNotEqual(response.signatures, False)
        self.assertGreater(len(response.signatures), 0)
        signature = response.signatures[0]
        self.assertEqual(signature.text, "123456789012")
        self.assertEqual(signature.barcode_type_name, "Code39Standard")
        self.assertIn("BarcodeSignatureData", signature.signature_type)  

```

[Test](test/) contain various examples of using the SDK.
Please put your credentials into [Configuration](groupdocs_signature_cloud/configuration.py).

## Dependencies
- Python 2.7 and 3.4+
- referenced packages (see [here](setup.py) for more details)

## Licensing
GroupDocs.Signature for Cloud SDK for Python is licensed under [MIT License](LICENSE).

## Resources
+ [**Website**](https://www.groupdocs.cloud)
+ [**Product Home**](https://products.groupdocs.cloud/signature)
+ [**Documentation**](https://docs.groupdocs.cloud/display/signaturecloud/Home)
+ [**Free Support Forum**](https://forum.groupdocs.cloud/c/signature)
+ [**Blog**](https://blog.groupdocs.cloud/category/signature)


## Contact Us
Your feedback is very important to us. Please feel free to contact us using our [Support Forums](https://forum.groupdocs.cloud/c/signature).