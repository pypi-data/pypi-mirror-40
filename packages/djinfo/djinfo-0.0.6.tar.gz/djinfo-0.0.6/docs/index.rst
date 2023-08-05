Django djinfo |version| documentation
=====================================

Debugging information page intented for production use.

.. figure:: https://gitlab.com/h3/djinfo/raw/master/docs/topics/img/djinfo-screenshot.png
    :alt: Screenshot
    :align: center
    :width: 1003px


Installation
------------

From Pypi:


.. code:: bash

    pip install djinfo


Add `djinfo` to your setting's `INSTALLED_APPS`.


Add `djinfo` URL to your projecr's `urls.py`:

.. code:: python

    from django.conf.urls import url
    from django.contrib import admin

    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^djinfo/', 'djinfo.urls'),
    ]

You can then navigate to 
`http://127.0.0.1:8000/djinfo/ <http://127.0.0.1:8000/djinfo/>`_


.. note:: Only super user will be able to acess this page!


Settings
--------

**DJINFO_MASK_SETTINGS**

Default: ``[r'.*PASSPHRASE.*', r'.*PASSWORD.*', r'.*SECRET.*']``

Settings keys matching any of the provided regex list will have their value
masked with asterisks.

**DJINFO_MASK_ENV**

Default: ``[r'.*PASSPHRASE.*', r'.*PASSWORD.*', r'.*SECRET.*']``

Environment keys matching any of the provided regex list will have their value
masked with asterisks.

**DJINFO_EXCLUDE_ENV**

Default: ``[r'^_fzf.*']``

So far this setting exists solely because fzf is polluting the environment with
every single setting it has in bank.

**DJINFO_USER_TEST**

Default: ``lambda u: u.is_superuser``



Integration
-----------

If you need to integrate a link to djinfo in a template:


.. code:: html

    {% if request.user.is_superuser %}
    <a href="{% url "djinfo:index" %}">djinfo</a>
    {% endif %}


It is also possible to access the data shown on the page as JSON by adding
``?json`` to the URL: ``{% url "djinfo:index" %}?json``.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
