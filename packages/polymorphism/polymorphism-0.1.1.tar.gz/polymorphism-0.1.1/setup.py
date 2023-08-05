# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['polymorphism']

package_data = \
{'': ['*']}

install_requires = \
['pytest-cov>=2.6,<3.0']

setup_kwargs = {
    'name': 'polymorphism',
    'version': '0.1.1',
    'description': 'Ad hoc polymorphism for Python classes!',
    'long_description': 'Ad hoc polymorphism for Python classes!\n=====================================================\n\nInstallation\n------------\n::\n\n    pip install polymorphism\n\npolymorphism support python 3.4+\n\nUsage\n-----\nTo use the ``polymorphism`` simply inherit from the ``Polymorphism`` class::\n\n    from polymorphism import Polymorphism\n\n\n    class Simple(Polymorphism):\n        def calc(self, x: int, y: int) -> None:\n            pass\n\n        def calc(self, x: float, y: float) -> None:\n            pass\n\nOr use it as metaclass::\n\n    from polymorphism import PolymorphismMeta\n\n    class Simple(metaclass=PolymorphismMeta):\n        ...\n\n\nSometimes adding another class to the inheritance is undesirable, then you can use the ``overload`` decorator::\n\n    from polymorphism import overload\n\n\n    class Simple(Polymorphism):\n        @overload\n        def calc(self, x: int, y: int) -> None:\n            pass\n\n        @calc.overload\n        def calc(self, x: float, y: float) -> None:\n            pass\n\nThe only difference between using a decorator and inheriting it is checking for method shading. With ``overload`` the next example will not raise exception::\n\n    from polymorphism import overload\n\n\n    class Simple(Polymorphism):\n        @overload\n        def calc(self, x: int, y: int) -> None:\n            pass\n\n        calc = 5\n\nAnd ``calc`` would be only the attribute.\n\nWhy?\n----\nThe idea to implement polymorphism is not new. Many libraries `implement <https://github.com/mrocklin/multipledispatch>`_ this idea. Even the `standard library <http://docs.python.org/3.4/library/functools.html#functools.singledispatch>`_ has an implementation.\n\nBut they do not support use with classes or standard type annotation.\n\nThe basic idea of the implementation was inspired by the great book `Python Cookbook 3rd Edition <http://shop.oreilly.com/product/0636920027072.do>`_ by David Beazley and Brian K. Jones. But the implementation in the book did not support usage of keyword arguments!\n\nAdvantages\n----------\nIn addition to named arguments the library allows:\n\n* Use standard and custom descriptors\n* Use naming (keyword) arguments\n* Checks for:\n\n  * Arguments for variable length\n  * Missed argument annotation\n  * Name of wrapped function of descriptor\n  * Shading method by attribute or data descriptor (like ``property``)\n  * Redefining the method with the same types\n\n* Using any name for instance, not only ``self``\n\nFor all checks is raised ``TypeError`` exception.\n\nLimitations\n-----------\n\n* Simple types for dispatching\n* ``overload`` should be top of decorators\n* Custom descriptor should save wrapped function  under "__wrapped__" name\n* Obvious, method argument can\'t be variable length (\\* and \\*\\*)\n\n\nExamples\n--------\nThere are no restrictions on the use of the number of decorators, you only need to comply the naming convention.\n\nFor example::\n\n    class Simple(Polymorphism):\n        def calc(self, x: int, y: int) -> None:\n            pass\n\n        @classmethod\n        def calc(cls, x: float, y: float) -> None:\n            pass\n\n        @staticmethod\n        def calc(x: str, y: str) -> None:\n            pass\n\n    Simple().calc(1.0, y=2.0)\n\nWhile use ``overload`` decorator place it on top::\n\n    class Simple:\n        @overload\n        def calc(self, x: int, y: int) -> None:\n            pass\n\n        @calc.overload\n        @classmethod\n        def calc_float(cls, x: float, y: float) -> None:\n            pass\n\n        @calc.overload\n        @staticmethod\n        def calc_str(x: str, y: str) -> None:\n            pass\n\nWith ``overload`` only first method name matter. Other methods can have any other names.\n\npolymorphism checks the class at the time of creation::\n\n    class Simple(Polymorphism):\n        def calc(self, x: int, y: int) -> None:\n            pass\n\n        def calc(self, x: int, y: int, z: int = 3) -> None:\n            pass\n\nThe below example will raise ``TypeError`` exception because ``calc`` method overloaded with ``z`` parameter with default value and it is impossible distinct last method from first.\n\n``polymorphism`` will raise ``TypeError`` exception on any wrong overloading, so you don\'t need worry about correctness of it.\n\nSee more examples in `tests.py <https://github.com/asduj/polymorphism/blob/master/tests.py>`_.\n\nTo-do\n-----\n\n* Complex types for dispatching like ``List[int]``',
    'author': 'asduj',
    'author_email': 'asduj@ya.ru',
    'url': 'https://github.com/asduj/polymorphism',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.4',
}


setup(**setup_kwargs)
