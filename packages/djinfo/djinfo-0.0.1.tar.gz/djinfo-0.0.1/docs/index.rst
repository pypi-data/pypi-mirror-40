Django djinfo |version| documentation
=====================================

Debugging information page intented for production use.

.. figure:: topics/img/djinfo-screenshot.png
    :alt: Screenshot
    :align: center
    :width: 1003px


Installation
------------

From Pypi:


.. code:: bash

    pip install djinfo


Add djinfo URL to your project:

.. code:: python

    from django.conf.urls import url
    from django.contrib import admin

    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^djinfo/', 'djinfo.urls'),
    ]

You can then navigate to 
`http://127.0.0.1:8000/djinfo/ <http://127.0.0.1:8000/djinfo/>`_


Integration
-----------

If you need to integrate a link to djinfo in a template:


.. code:: html

    <a href="{% url "djinfo:index" %}">djinfo</a>


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
