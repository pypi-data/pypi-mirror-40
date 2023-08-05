====
errs
====


.. image:: https://img.shields.io/pypi/v/errs.svg
        :target: https://pypi.python.org/pypi/errs

.. image:: https://img.shields.io/travis/nicksettje/errs.svg
        :target: https://travis-ci.org/nicksettje/errs

.. image:: https://codecov.io/gh/nicksettje/errs/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/nicksettje/errs

.. image:: https://readthedocs.org/projects/errs/badge/?version=latest
        :target: https://errs.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/nicksettje/errs/shield.svg
     :target: https://pyup.io/repos/github/nicksettje/errs/
     :alt: Updates



Type-safe error handling for Python.


* Free software: MIT license
* Documentation: https://errs.readthedocs.io.

Installation
------------
`pip install errs`

Usage
-----
The `@errs` decorator marks any function or method that raises an `Exception`. Rather than handling the `Exception` explicitly, we collect the result of the function and then check whether an error occurred. 

This leads to code that is more explicit about error handling as well as resilient to the raising of unforeseen exceptions. This style is similar to error handling in Go.

Additionally, all exceptions wrapped by `@errs` will be logged to the default Python logger on the error level. This provides a powerful abstraction where runtime behaviors are logged and separated from current application state.

.. code-block:: python

        from errs import errs

        @errs
        def raises(): #type: () -> int
            raise Exception('this will get logged')
            return 0

        def check_error(): #type: () -> None
            out, err = raises()
            print('Error: {err}'.format(err.check()))

        if __name__ == '__main__':
            check_error() #prints Error: True


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
