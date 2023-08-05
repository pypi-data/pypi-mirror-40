# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['napy', 'napy.console', 'napy.ipyext', 'napy.template', 'napy.tools']

package_data = \
{'': ['*']}

install_requires = \
['better_exceptions>=0.2.1,<0.3.0',
 'cleo>=0.7.2,<0.8.0',
 'requests>=2.21,<3.0',
 'requests_html>=0.9.0,<0.10.0']

extras_require = \
{'math': ['numpy>=1.15,<2.0',
          'jupyter>=1.0,<2.0',
          'sympy>=1.3,<2.0',
          'pandas>=0.23.4,<0.24.0'],
 'others': ['pendulum>=2.0,<3.0', 'tqdm>=4.28,<5.0', 'bs4>=0.0.1,<0.0.2']}

entry_points = \
{'console_scripts': ['napy = napy.console:run']}

setup_kwargs = {
    'name': 'napy',
    'version': '0.2.1',
    'description': 'Here is everything frequently use in python.',
    'long_description': '# Table of Contents\n\n-   [Prologue](#org76774da)\n-   [Introduction](#org96a0d13)\n-   [Usage](#org08dde91)\n    -   [Tools (Libs)](#org32fac2d)\n        -   [Utility](#org2f3eb3e)\n            -   [Flatten](#orgd29860a)\n    -   [Comand Line Tools](#org219e84d)\n        -   [Template](#orgb5b1237)\n            -   [Crawler](#orgafe8f23)\n    -   [More](#orga4b15d9)\n-   [Packages](#orga721f60)\n    -   [Normal](#org4b4510a)\n    -   [Science](#org4034141)\n    -   [Crawler](#orgc3f72b5)\n    -   [Development](#org5b345b8)\n-   [Epoligue](#org2f16717)\n    -   [History](#org111d8b7)\n        -   [0.2.1 <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-22 Sat&gt;</span></span>](#org00f2e11)\n        -   [0.1.1 <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-17 Mon&gt;</span></span>](#org0808725)\n        -   [0.1.0 <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-16 Sun&gt;</span></span>](#orgade8c74)\n\nHere is everything frequently use in python.\n\n\n<a id="org76774da"></a>\n\n# Prologue\n\nI often need to configure a new Python development environment.  Whether it is to help others or for\nmyself, it is very troublesome to manage packages with pip.  Besides, there are fascinating and\nimpressive ipython extensions, and every installation of them has to bother Google again.\n\nTherefore, I created this napy.\n\n*This package is still under development, and although is only for myself now, you can use it as you\nlike.*\n\n\n<a id="org96a0d13"></a>\n\n# Introduction\n\nNapy includes some packages that I frequently use in python, such as `requests`, for crawlers; `sympy`\nfor mathematics.  Also, napy has some ipython extensions I write.  A template Napy also has that I\noften use (of course, it\'s still straightforward now).  Hope you like it.\n\n*Due to the `.dir-local.el` contains `(org-html-klipsify-src . nil)`, it is warning that it is not safe.*\n\n\n<a id="org08dde91"></a>\n\n# Usage\n\n\n<a id="org32fac2d"></a>\n\n## Tools (Libs)\n\n\n<a id="org2f3eb3e"></a>\n\n### Utility\n\n\n<a id="orgd29860a"></a>\n\n#### Flatten\n\nFlatten list of iterable objects.\n\n    from napy.tools import flatten, flatten_str\n\n    list(flatten([1, 2, "ab", [3, "c", [4, ["d"]]]]))\n    # [1, 2, "ab", 3, "c", 4, "d"]\n\n    list(flatten("abc"))\n    # ["a", "b", "c"]\n    # regard "abc" as ["a", "b", "c"]\n\n    list(flatten_str([1, 2, "ab", [3, "c", [4, ["d"]]]]))\n    # or list(flatten([1, 2, "ab", [3, "c", [4, ["d"]]]], True))\n    # [1, 2, "a", "b", 3, "c", 4, "d"]\n\n\n<a id="org219e84d"></a>\n\n## Comand Line Tools\n\n\n<a id="orgb5b1237"></a>\n\n### Template\n\n\n<a id="orgafe8f23"></a>\n\n#### Crawler\n\n    $ napy template --help\n    Usage:\n      template [options]\n\n    Options:\n      -c, --category[=CATEGORY]       Category of template\n      -o, --output[=OUTPUT]           Output file (default: "stdout")\n      -y, --yes                       Confirmation\n      -h, --help                      Display this help message\n      -q, --quiet                     Do not output any message\n      -V, --version                   Display this application version\n          --ansi                      Force ANSI output\n          --no-ansi                   Disable ANSI output\n      -n, --no-interaction            Do not ask any interactive question\n      -v|vv|vvv, --verbose[=VERBOSE]  Increase the verbosity of messages: 1 for normal output, 2 for more verbose output and 3 for debug\n\n    Help:\n     Template command line tool.\n\nIt will generate this:\n\n    from requests_html import HtmlSession as s\n    import requests as req\n\n\n    def crawler() -> None:\n        """Crawler."""\n        pass\n\n\n    if __name__ == "__main__":\n        pass\n\n\n<a id="orga4b15d9"></a>\n\n## More\n\nStill under development.\n\n\n<a id="orga721f60"></a>\n\n# Packages\n\n\n<a id="org4b4510a"></a>\n\n## Normal\n\n-   **better\\_exceptions:** Pretty and helpful exceptions, automatically.\n-   **pendulum:** Python datetimes made easy.\n-   **tqdm:** Fast, Extensible Progress Meter.\n\n\n<a id="org4034141"></a>\n\n## Science\n\n-   **jupyter :: Jupyter Notebook + IPython:** Jupyter metapackage. Install all the Jupyter components in\n    one go.\n-   **numpy:** NumPy: array processing for numbers, strings, records, and objects\n-   **pandas:** Powerful data structures for data analysis, time series, and statistics\n-   **sympy:** Computer algebra system (CAS) in Python\n\n\n<a id="orgc3f72b5"></a>\n\n## Crawler\n\n-   **requests:** Python HTTP for Humans.\n-   **requests\\_html:** HTML Parsing for Humans.\n-   **BeautifulSoup4:** Screen-scraping library\n\n\n<a id="org5b345b8"></a>\n\n## Development\n\n-   **cleo:** Cleo allows you to create beautiful and testable command-line interfaces.\n\n\n<a id="org2f16717"></a>\n\n# Epoligue\n\n\n<a id="org111d8b7"></a>\n\n## History\n\n\n<a id="org00f2e11"></a>\n\n### 0.2.1 <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-22 Sat&gt;</span></span>\n\nAdd a new tool flatten\n\n\n<a id="org0808725"></a>\n\n### 0.1.1 <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-17 Mon&gt;</span></span>\n\nUse README.md instead of README.org\n\n\n<a id="orgade8c74"></a>\n\n### 0.1.0 <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-16 Sun&gt;</span></span>\n\nThe beginning of everything\n',
    'author': 'Nasy',
    'author_email': 'nasyxx+napy@gmail.com',
    'url': 'https://nasyxx.gitlab.io/napy/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
