# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['cnab']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cnab',
    'version': '0.1.1',
    'description': 'A module for working with Cloud Native Application Bundles in Python',
    'long_description': '# Python CNAB Library\n\n_Work-in-progress_ library for working with [CNAB](https://cnab.io/) in Python.\n\nThere are probably three main areas of interest for a CNAB client:\n\n1. Creation/parsing of the `bundle.json` format\n2. Building invocation images\n3. Running actions against a CNAB\n\nAt this early stage only the first of these is currently work-in-progress.\n\n## Parsing `bundle.json`\n\nNothing too fancy here, the `Bundle` class  has a `from_dict` static method which\nbuilds a full `Bundle` object.\n\n```python\nimport json\nfrom cnab import Bundle\n\nwith open("bundle.json") as f:\n    data = json.load(f)\n\nbundle = Bundle.from_dict(data)\n```\n\nThis could for example be used for validation purposes, or for building user interfaces for `bundle.json` files.\n\n\n## Describing `bundle.json` in Python \n\nYou can also describe the `bundle.json` file in Python. This will correctly validate the\nstructure based on the current specification and would allow for building a custom DSL or other\nuser interface for generating `bundle.json` files.\n\n```python\nimport json\nfrom cnab import Bundle, InvocationImage\n\nbundle = Bundle(\n    name="hello",\n    version="0.1.0",\n    invocation_images=[\n        InvocationImage(\n            image_type="docker",\n            image="technosophos/helloworld:0.1.0",\n            digest="sha256:aaaaaaa...",\n        )\n    ],\n)\n\nprint(json.dumps(bundle.to_dict(), indent=4))\n```\n\n\n## Thanks\n\nThanks to [QuickType](https://quicktype.io/) for bootstrapping the creation of the Python code for manipulating `bundle.json` based on the current JSON Schema.\n\n',
    'author': 'Gareth Rushgrove',
    'author_email': 'gareth@morethanseven.net',
    'url': 'https://github.com/garethr/pycnab',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
