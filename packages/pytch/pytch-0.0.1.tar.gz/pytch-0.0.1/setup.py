# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pytch', 'pytch.codegen', 'pytch.typesystem']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=18.2,<19.0',
 'click>=7.0,<8.0',
 'distance>=0.1.3,<0.2.0',
 'pyrsistent>=0.14.8,<0.15.0',
 'typing-extensions>=3.6,<4.0',
 'typing>=3.6,<4.0']

extras_require = \
{'fuzz': ['cython>=0.29.2,<0.30.0', 'python-afl>=0.7.1,<0.8.0']}

entry_points = \
{'console_scripts': ['pytch = pytch.__main__:cli']}

setup_kwargs = {
    'name': 'pytch',
    'version': '0.0.1',
    'description': 'An expression-oriented, tooling-focused language that compiles down to Python.',
    'long_description': '[![Build Status](https://travis-ci.org/arxanas/pytch.svg?branch=master)](https://travis-ci.org/arxanas/pytch)\n\n## Development\n\n### Setup\n\nThe Pytch compiler is currently written in Python 3.7.\n\nTo install the development environment, run\n\n```sh\n$ poetry install\n```\n\n### Running\n\nTo launch the REPL:\n\n```sh\n$ poetry run pytch repl\n```\n\nTo execute a file as a Pytch script:\n\n```sh\n$ poetry run pytch run file.pytch\n```\n\n### Updating the syntax trees\n\nTo modify the syntax tree node types, update `pytch/syntax_tree.txt`, then run:\n\n```sh\n$ ./bin/generate_syntax_trees.sh\n```\n\n### Fuzzing the parser\n\nTo run the fuzzer on the Pytch parser, first be sure that [the AFL\nfuzzer][afl-fuzz] is installed (e.g. with `brew install afl-fuzz`). Next,\ninstall the fuzzing dependencies:\n\n  [afl-fuzz]: http://lcamtuf.coredump.cx/afl/\n\n```sh\n$ poetry install --extras fuzz\n```\n\nThen you can run:\n\n```sh\n$ ./bin/fuzz.sh\n```\n',
    'author': 'Waleed Khan',
    'author_email': 'me@waleedkhan.name',
    'url': 'https://github.com/arxanas/pytch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
