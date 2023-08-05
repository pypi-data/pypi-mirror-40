# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['nacf']

package_data = \
{'': ['*']}

install_requires = \
['requests_html>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'nacf',
    'version': '0.1.0',
    'description': 'Nasy Crawler Framework -- Never had such a pure crawler.',
    'long_description': '# Table of Contents\n\n-   [Prologue](#orgefdab53)\n-   [Packages](#orgc11b1dc)\n-   [Development Process](#org6e3c1eb)\n    -   [Http Functions](#org89395ee)\n        -   [Get](#org063529e)\n        -   [Post](#orge045e05)\n-   [Epoligue](#org0f619c0)\n    -   [History](#org90eabca)\n        -   [Version 0.1.0](#org8af289f)\n\n\n\n<a id="orgefdab53"></a>\n\n# Prologue\n\nNever had such a pure crawler like this `nacf`.\n\nAlthough I often write crawlers, I don&rsquo;t like to use huge frameworks, such as scrapy, but prefer\nsimple `requests+bs4` or more general `requests_html`.  However, these two are inconvenient for a\ncrawler.  E.g. Places, such as error retrying or parallel crawling, need to be handwritten by\nmyself.  It is not very difficult to write it while writing too much can be tedious.  Hence I\nstarted writing this nacf (Nasy Crawler Framework), hoping to simplify some error retrying or\nparallel writing of crawlers.\n\n\n<a id="orgc11b1dc"></a>\n\n# Packages\n\n<table>\n<caption class="t-above"><span class="table-number">Table 1:</span> Packages</caption>\n\n<colgroup>\n<col  class="org-left">\n\n<col  class="org-right">\n\n<col  class="org-left">\n</colgroup>\n<thead>\n<tr>\n<th scope="col" class="org-left">Package</th>\n<th scope="col" class="org-right">Version</th>\n<th scope="col" class="org-left">Description</th>\n</tr>\n</thead>\n\n<tbody>\n<tr>\n<td class="org-left">requests-html</td>\n<td class="org-right">0.9.0</td>\n<td class="org-left">HTML Parsing for Humans.</td>\n</tr>\n</tbody>\n</table>\n\n\n<a id="org6e3c1eb"></a>\n\n# Development Process\n\n\n<a id="org89395ee"></a>\n\n## TODO Http Functions\n\n\n<a id="org063529e"></a>\n\n### DONE Get\n\n<p><span class="timestamp-wrapper"><span class="timestamp-kwd">CLOSED:</span> <span class="timestamp">[2018-12-25 Tue 17:36]</span></span></p>\n\n\n<a id="orge045e05"></a>\n\n### NEXT Post\n\n\n<a id="org0f619c0"></a>\n\n# Epoligue\n\n\n<a id="org90eabca"></a>\n\n## History\n\n\n<a id="org8af289f"></a>\n\n### Version 0.1.0\n\n-   **Date:** <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-23 Sun&gt;</span></span>\n-   **Commemorate Version:** First Version\n    -   Basic Functions.\n',
    'author': 'Nasy',
    'author_email': 'nasyxx+nacf@gmail.com',
    'url': 'https://github.com/nasyxx/nacf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
