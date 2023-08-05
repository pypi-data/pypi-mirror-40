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
    'version': '0.1.1',
    'description': 'Nasy Crawler Framework -- Never had such a pure crawler.',
    'long_description': '# Table of Contents\n\n-   [Prologue](#org591fabd)\n-   [Packages](#orgfab1ac5)\n-   [Development Process](#orgf9ac559)\n    -   [Http Functions](#org0c20f86)\n        -   [Get](#org7d426ca)\n        -   [Post](#org40e101b)\n        -   [Bugs](#org2b33a0e)\n            -   [Fix an error from inspect.Parameter which caused the function parallel down.](#orgb794b62)\n-   [Epoligue](#org1b62763)\n    -   [History](#org953eff6)\n        -   [Version 0.1.1](#org40f41b8)\n        -   [Version 0.1.0](#org18b1472)\n\n\n\n<a id="org591fabd"></a>\n\n# Prologue\n\nNever had such a pure crawler like this `nacf`.\n\nAlthough I often write crawlers, I don&rsquo;t like to use huge frameworks, such as scrapy, but prefer\nsimple `requests+bs4` or more general `requests_html`.  However, these two are inconvenient for a\ncrawler.  E.g. Places, such as error retrying or parallel crawling, need to be handwritten by\nmyself.  It is not very difficult to write it while writing too much can be tedious.  Hence I\nstarted writing this nacf (Nasy Crawler Framework), hoping to simplify some error retrying or\nparallel writing of crawlers.\n\n\n<a id="orgfab1ac5"></a>\n\n# Packages\n\n<table>\n<caption class="t-above"><span class="table-number">Table 1:</span> Packages</caption>\n\n<colgroup>\n<col  class="org-left">\n\n<col  class="org-right">\n\n<col  class="org-left">\n</colgroup>\n<thead>\n<tr>\n<th scope="col" class="org-left">Package</th>\n<th scope="col" class="org-right">Version</th>\n<th scope="col" class="org-left">Description</th>\n</tr>\n</thead>\n\n<tbody>\n<tr>\n<td class="org-left">requests-html</td>\n<td class="org-right">0.9.0</td>\n<td class="org-left">HTML Parsing for Humans.</td>\n</tr>\n</tbody>\n</table>\n\n\n<a id="orgf9ac559"></a>\n\n# Development Process\n\n\n<a id="org0c20f86"></a>\n\n## TODO Http Functions\n\n\n<a id="org7d426ca"></a>\n\n### DONE Get\n\n<p><span class="timestamp-wrapper"><span class="timestamp-kwd">CLOSED:</span> <span class="timestamp">[2018-12-25 Tue 17:36]</span></span></p>\n\n\n<a id="org40e101b"></a>\n\n### NEXT Post\n\n\n<a id="org2b33a0e"></a>\n\n### TODO Bugs\n\n\n<a id="orgb794b62"></a>\n\n#### TODO Fix an error from inspect.Parameter which caused the function parallel down.\n\n\n<a id="org1b62763"></a>\n\n# Epoligue\n\n\n<a id="org953eff6"></a>\n\n## History\n\n\n<a id="org40f41b8"></a>\n\n### Version 0.1.1\n\n-   **Data:** <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-26 Wed&gt;</span></span>\n-   **Ignored:** An error caused by `inspect.Parameter`\n-   **Help Wanted:** Can someone help me about the Parameter?\n\n\n<a id="org18b1472"></a>\n\n### Version 0.1.0\n\n-   **Date:** <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-23 Sun&gt;</span></span>\n-   **Commemorate Version:** First Version\n    -   Basic Functions.\n',
    'author': 'Nasy',
    'author_email': 'nasyxx+nacf@gmail.com',
    'url': 'https://github.com/nasyxx/nacf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
