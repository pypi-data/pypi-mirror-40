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
    'version': '0.1.2',
    'description': 'Nasy Crawler Framework -- Never had such a pure crawler.',
    'long_description': '# Table of Contents\n\n-   [Prologue](#orge8b2d63)\n-   [Packages](#org2d6e4f2)\n-   [Development Process](#orgcdb2d25)\n    -   [Http Functions](#org2562d26)\n        -   [Get](#org268a91b)\n        -   [Post](#org39534ac)\n        -   [Bugs](#org60b0f47)\n            -   [Fix an error from inspect.Parameter which caused the function parallel down.](#org5f07c18):err:1:\n-   [Epoligue](#orga79b864)\n    -   [History](#orgd2e0e7c)\n        -   [Version 0.1.2](#org1180830)\n        -   [Version 0.1.1](#org3b9e479)\n        -   [Version 0.1.0](#orga1b8a28)\n\n\n\n<a id="orge8b2d63"></a>\n\n# Prologue\n\nNever had such a pure crawler like this `nacf`.\n\nAlthough I often write crawlers, I don&rsquo;t like to use huge frameworks, such as scrapy, but prefer\nsimple `requests+bs4` or more general `requests_html`.  However, these two are inconvenient for a\ncrawler.  E.g. Places, such as error retrying or parallel crawling, need to be handwritten by\nmyself.  It is not very difficult to write it while writing too much can be tedious.  Hence I\nstarted writing this nacf (Nasy Crawler Framework), hoping to simplify some error retrying or\nparallel writing of crawlers.\n\n\n<a id="org2d6e4f2"></a>\n\n# Packages\n\n<table>\n<caption class="t-above"><span class="table-number">Table 1:</span> Packages</caption>\n\n<colgroup>\n<col  class="org-left">\n\n<col  class="org-right">\n\n<col  class="org-left">\n</colgroup>\n<thead>\n<tr>\n<th scope="col" class="org-left">Package</th>\n<th scope="col" class="org-right">Version</th>\n<th scope="col" class="org-left">Description</th>\n</tr>\n</thead>\n\n<tbody>\n<tr>\n<td class="org-left">requests-html</td>\n<td class="org-right">0.9.0</td>\n<td class="org-left">HTML Parsing for Humans.</td>\n</tr>\n</tbody>\n</table>\n\n\n<a id="orgcdb2d25"></a>\n\n# Development Process\n\n\n<a id="org2562d26"></a>\n\n## TODO Http Functions\n\n\n<a id="org268a91b"></a>\n\n### DONE Get\n\n<p><span class="timestamp-wrapper"><span class="timestamp-kwd">CLOSED:</span> <span class="timestamp">[2018-12-25 Tue 17:36]</span></span></p>\n\n\n<a id="org39534ac"></a>\n\n### NEXT Post\n\n\n<a id="org60b0f47"></a>\n\n### TODO Bugs\n\n\n<a id="org5f07c18"></a>\n\n#### DONE Fix an error from inspect.Parameter which caused the function parallel down.     :err:1:\n\n<p><span class="timestamp-wrapper"><span class="timestamp-kwd">CLOSED:</span> <span class="timestamp">[2018-12-26 Wed 20:26]</span></span></p>\n\n\n<a id="orga79b864"></a>\n\n# Epoligue\n\n\n<a id="orgd2e0e7c"></a>\n\n## History\n\n\n<a id="org1180830"></a>\n\n### Version 0.1.2\n\n-   **Data:** <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-26 Wed&gt;</span></span>\n-   **Fixed:** `inspect.Parameter` error in last version.\n\n\n<a id="org3b9e479"></a>\n\n### Version 0.1.1\n\n-   **Data:** <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-26 Wed&gt;</span></span>\n-   **Ignored:** An error caused by `inspect.Parameter`\n-   **Help Wanted:** Can someone help me about the Parameter?\n\n\n<a id="orga1b8a28"></a>\n\n### Version 0.1.0\n\n-   **Date:** <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-23 Sun&gt;</span></span>\n-   **Commemorate Version:** First Version\n    -   Basic Functions.\n',
    'author': 'Nasy',
    'author_email': 'nasyxx+nacf@gmail.com',
    'url': 'https://github.com/nasyxx/nacf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
