# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['drf_body_token']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.0,<3.0', 'djangorestframework>=3.0,<4.0']

setup_kwargs = {
    'name': 'drf-body-token',
    'version': '0.1.0',
    'description': 'REST authentication class to get token from HTTP body',
    'long_description': "==============\nDRF Body Token\n==============\n\nProvide a `Django REST Framework <https://www.django-rest-framework.org>`_ authentication class, to look for token\nin HTTP body, instead of HTTP header.\n\nThis use case is uncommon and may be less secure,\nbut some REST client application doesn't let customize HTTP header,\nand hence, user cannot set ``Authorization`` header.\nOne such client is `Blynk Webhook <http://docs.blynk.cc/#widgets-other-webhook>`_ Widget.\n\n\nInstall\n-------\n\n.. code-block:: shell\n\n    pip3 install drf-body-token\n\n`DRF Body Token` only supports Python 3.5+\n\nUsage\n-----\n\nAdd ``BodyTokenAuthentication`` to ``authentication_classes`` atrribute of your viewset.\nExample:\n\n.. code-block:: python\n\n    from drf_body_token.authentication import BodyTokenAuthentication\n\n    class MyAwesomeViewSet(GenericViewSet):\n        authentication_classes = (TokenAuthentication, BodyTokenAuthentication)\n\nYou can also add it to ``REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES']`` settings, to make it available for every viewset.\n\nBy default, ``BodyTokenAuthentication`` looks for ``acess_token`` field in HTTP body.\nIf you want it to look for another field, add this to your `settings.py` file:\n\n.. code-block:: python\n\n    REST_BODY_TOKEN_FIELD = 'your_field'\n",
    'author': 'Nguyễn Hồng Quân',
    'author_email': 'ng.hong.quan@gmail.com',
    'url': '',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
