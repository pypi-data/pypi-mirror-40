# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['byu_jwt']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=2.4,<3.0', 'pyjwt>=1.7,<2.0', 'requests>=2.21,<3.0']

setup_kwargs = {
    'name': 'byu-jwt',
    'version': '2.0.0',
    'description': '',
    'long_description': '# byu-jwt-python\nA python JWT validator that does all the BYU specific stuff as well as handle caching well-known and cert fetching\n\n# Installation\n`pip install byu_jwt`\n\n## API\n\n---\n**Note: It is important to declare the handler at a global level. This allows the caching of the well-known data as well as using the cache-control headers on the certificates only re-fetching those when cache-control has timed out. Reinitializing the class object will negate any benefit of the caching**\n\n---\nInstantiate the class and reuse the object to utilize caching:\n```python\nimport byu_jwt\nbyujwt = byu_jwt.JWT_Handler()\n```\n\n### Check only if JWT is valid\n```python\nassert byujwt.is_valid(jwt_to_validate)\n```\n\n### Decode JWT and Check validity\n```python\ntry:\n    jwt = byujwt.decode(jwt_to_validate)\n    return f"Hello, {jwt[\'preferredFirstName\']}"\nexcept byu_jwt.exceptions.JWTVerifyError as ex_info:\n    return "Invalid JWT"\nexcept byu_jwt.exceptions.JWTHandlerError as ex_info:\n    return "Error attempting to verify the jwt"\n```\n\n### JWT Header Names\n\nBYU\'s API Manager creates an HTTP header that contains a signed [JWT](https://jwt.io/). The names of the designed BYU signed headers can be referenced here for lookup convenience.\n\n### BYU_JWT_HEADER_CURRENT\n\nThe property containing the name of the HTTP header that contains the BYU signed JWT sent directly from BYU\'s API Manager.\n\nValue is X-JWT-Assertion.\n\nExample\n\n```python\ncurrent_jwt_header = byu_jwt.JWT_HEADER\n```\n\n### BYU_JWT_HEADER_ORIGINAL\n\nThe property containing the name of the HTTP header that contains the BYU signed JWT forwarded on from a service that received the BYU signed JWT sent directly from BYU\'s API Manager.\n\nValue is X-JWT-Assertion-Original.\n\nExample\n\n```python\noriginal_jwt_header = byu_jwt.JWT_HEADER_ORIGINAL\n```\n\n### Example Python Lambda function that makes use of caching\n```python\nimport byu_jwt\n\nbyujwt = byu_jwt.JWT_Handler()\n\ndef handler(event, context):\n    jwt_to_decode = event[\'headers\'][byu_jwt.JWT_HEADER]\n    try:\n        jwt = byujwt.decode(jwt_to_validate)\n        return {\'statusCode\': 200, \'body\': f\'Hello, {jwt["preferredFirstName"]}\'}\n    except byu_jwt.exceptions.JWTVerifyError as ex_info:\n        return {\'statusCode\': 403, \'body\': "Invalid JWT"}\n    except byu_jwt.exceptions.JWTHandlerError as ex_info:\n        return {\'statusCode\': 500, \'body\': "Error attempting to verify the jwt"}\n```\n\n\n### Example Decoded JWT Structure\n```json\n{\n  "iss": "https://api.byu.edu",\n  "exp": 1545425710,\n  "byu": {\n    "client": {\n      "byuId": "",\n      "claimSource": "",\n      "netId": "",\n      "personId": "",\n      "preferredFirstName": "",\n      "prefix": "",\n      "restOfName": "",\n      "sortName": "",\n      "subscriberNetId": "",\n      "suffix": "",\n      "surname": "",\n      "surnamePosition": ""\n    },\n    "resourceOwner": {\n      "byuId": "",\n      "netId": "",\n      "personId": "",\n      "preferredFirstName": "",\n      "prefix": "",\n      "restOfName": "",\n      "sortName": "",\n      "suffix": "",\n      "surname": "",\n      "surnamePosition": ""\n    }\n  },\n  "wso2": {\n    "apiContext": "",\n    "application": {\n      "id": "",\n      "name": "",\n      "tier": ""\n    },\n    "clientId": "",\n    "endUser": "",\n    "endUserTenantId": "",\n    "keyType": "",\n    "subscriber": "",\n    "tier": "",\n    "userType": "",\n    "version": ""\n  }\n}\n```',
    'author': 'Nate Peterson',
    'author_email': 'nate_peterson@byu.edu',
    'url': 'https://github.com/byu-oit/byu-jwt-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
