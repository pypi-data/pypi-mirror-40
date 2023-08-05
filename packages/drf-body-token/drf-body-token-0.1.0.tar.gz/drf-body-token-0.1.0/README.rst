==============
DRF Body Token
==============

Provide a `Django REST Framework <https://www.django-rest-framework.org>`_ authentication class, to look for token
in HTTP body, instead of HTTP header.

This use case is uncommon and may be less secure,
but some REST client application doesn't let customize HTTP header,
and hence, user cannot set ``Authorization`` header.
One such client is `Blynk Webhook <http://docs.blynk.cc/#widgets-other-webhook>`_ Widget.


Install
-------

.. code-block:: shell

    pip3 install drf-body-token

`DRF Body Token` only supports Python 3.5+

Usage
-----

Add ``BodyTokenAuthentication`` to ``authentication_classes`` atrribute of your viewset.
Example:

.. code-block:: python

    from drf_body_token.authentication import BodyTokenAuthentication

    class MyAwesomeViewSet(GenericViewSet):
        authentication_classes = (TokenAuthentication, BodyTokenAuthentication)

You can also add it to ``REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES']`` settings, to make it available for every viewset.

By default, ``BodyTokenAuthentication`` looks for ``acess_token`` field in HTTP body.
If you want it to look for another field, add this to your `settings.py` file:

.. code-block:: python

    REST_BODY_TOKEN_FIELD = 'your_field'
