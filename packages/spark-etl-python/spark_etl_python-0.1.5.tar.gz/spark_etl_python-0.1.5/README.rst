================
Spark ETL Python
================


.. image:: https://img.shields.io/pypi/v/spark_etl_python.svg
        :target: https://pypi.python.org/pypi/spark_etl_python

.. image:: https://img.shields.io/travis/flavianh/spark_etl_python.svg
        :target: https://travis-ci.org/flavianh/spark_etl_python

.. image:: https://readthedocs.org/projects/spark-etl-python/badge/?version=latest
        :target: https://spark-etl-python.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/flavianh/spark_etl_python/shield.svg
     :target: https://pyup.io/repos/github/flavianh/spark_etl_python/
     :alt: Updates



A Python package that provides helpers for cleaning, deduplication, enrichment, etc. in Spark


* Free software: MIT license
* Documentation: https://spark-etl-python.readthedocs.io.


Features
--------

* TODO


Develop
-------

In order to be able to develop on this package:

1. Create a virtual environment
2. Install pip-tools: `pip install pip-tools`
3. Run `pip-sync requirements_dev.txt requirements.txt`

To update dependencies, add them to `requirements.in` (if they are needed to run the package) or `requirements_dev.in`.
Then run `pip-compile requirements.in` or `pip-compile requirements_dev.in`.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
