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
{'all': ['numpy>=1.15,<2.0',
         'jupyter>=1.0,<2.0',
         'sympy>=1.3,<2.0',
         'pandas>=0.23.4,<0.24.0',
         'pendulum>=2.0,<3.0',
         'tqdm>=4.28,<5.0',
         'bs4>=0.0.1,<0.0.2'],
 'math': ['numpy>=1.15,<2.0',
          'jupyter>=1.0,<2.0',
          'sympy>=1.3,<2.0',
          'pandas>=0.23.4,<0.24.0'],
 'others': ['pendulum>=2.0,<3.0', 'tqdm>=4.28,<5.0', 'bs4>=0.0.1,<0.0.2']}

entry_points = \
{'console_scripts': ['napy = napy.console:run']}

setup_kwargs = {
    'name': 'napy',
    'version': '0.2.2',
    'description': 'Here is everything frequently use in python.',
    'long_description': '# Table of Contents\n\n-   [Prologue](#orge7c993d)\n-   [Introduction](#org34ce89a)\n-   [Usage](#org50b2bae)\n    -   [Tools (Libs)](#org6834eee)\n        -   [Utility](#org3e067e5)\n            -   [Flatten](#orgae92c28)\n    -   [Comand Line Tools](#orgd240084)\n        -   [Template](#orgf379ee3)\n            -   [Crawler](#org7696ae6)\n    -   [More](#org2d9dfe6)\n-   [Packages](#org0ce3219)\n    -   [Normal](#org06b5a3e)\n    -   [Science](#org1fa803f)\n    -   [Crawler](#orgad6dc64)\n    -   [Development](#org855a683)\n-   [Epoligue](#org40ecd96)\n    -   [History](#orgadfe69c)\n        -   [0.2.2 <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-29 Sat&gt;</span></span>](#org5e9403c)\n        -   [0.2.1 <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-22 Sat&gt;</span></span>](#org40ed255)\n        -   [0.1.1 <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-17 Mon&gt;</span></span>](#org3476a9f)\n        -   [0.1.0 <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-16 Sun&gt;</span></span>](#org51a254c)\n\nHere is everything frequently use in python.\n\n\n<a id="orge7c993d"></a>\n\n# Prologue\n\nI often need to configure a new Python development environment.  Whether it is to help others or for\nmyself, it is very troublesome to manage packages with pip.  Besides, there are fascinating and\nimpressive ipython extensions, and every installation of them has to bother Google again.\n\nTherefore, I created this napy.\n\n*This package is still under development, and although is only for myself now, you can use it as you\nlike.*\n\n\n<a id="org34ce89a"></a>\n\n# Introduction\n\nNapy includes some packages that I frequently use in python, such as `requests`, for crawlers; `sympy`\nfor mathematics.  Also, napy has some ipython extensions I write.  A template Napy also has that I\noften use (of course, it\'s still straightforward now).  Hope you like it.\n\n*Due to the `.dir-local.el` contains `(org-html-klipsify-src . nil)`, it is warning that it is not safe.*\n\n\n<a id="org50b2bae"></a>\n\n# Usage\n\n\n<a id="org6834eee"></a>\n\n## Tools (Libs)\n\n\n<a id="org3e067e5"></a>\n\n### Utility\n\n\n<a id="orgae92c28"></a>\n\n#### Flatten\n\nFlatten list of iterable objects.\n\n    from napy.tools import flatten, flatten_str\n\n    list(flatten([1, 2, "ab", [3, "c", [4, ["d"]]]]))\n    # [1, 2, "ab", 3, "c", 4, "d"]\n\n    list(flatten("abc"))\n    # ["a", "b", "c"]\n    # regard "abc" as ["a", "b", "c"]\n\n    list(flatten_str([1, 2, "ab", [3, "c", [4, ["d"]]]]))\n    # or list(flatten([1, 2, "ab", [3, "c", [4, ["d"]]]], True))\n    # [1, 2, "a", "b", 3, "c", 4, "d"]\n\n\n<a id="orgd240084"></a>\n\n## Comand Line Tools\n\n\n<a id="orgf379ee3"></a>\n\n### Template\n\n\n<a id="org7696ae6"></a>\n\n#### Crawler\n\n    $ napy template --help\n    Usage:\n      template [options]\n\n    Options:\n      -c, --category[=CATEGORY]       Category of template\n      -o, --output[=OUTPUT]           Output file (default: "stdout")\n      -y, --yes                       Confirmation\n      -h, --help                      Display this help message\n      -q, --quiet                     Do not output any message\n      -V, --version                   Display this application version\n          --ansi                      Force ANSI output\n          --no-ansi                   Disable ANSI output\n      -n, --no-interaction            Do not ask any interactive question\n      -v|vv|vvv, --verbose[=VERBOSE]  Increase the verbosity of messages: 1 for normal output, 2 for more verbose output and 3 for debug\n\n    Help:\n     Template command line tool.\n\nIt will generate this:\n\n    from requests_html import HtmlSession as s\n    import requests as req\n\n\n    def crawler() -> None:\n        """Crawler."""\n        pass\n\n\n    if __name__ == "__main__":\n        pass\n\n\n<a id="org2d9dfe6"></a>\n\n## More\n\nStill under development.\n\n\n<a id="org0ce3219"></a>\n\n# Packages\n\n\n<a id="org06b5a3e"></a>\n\n## Normal\n\n-   **better\\_exceptions:** Pretty and helpful exceptions, automatically.\n-   **pendulum:** Python datetimes made easy.\n-   **tqdm:** Fast, Extensible Progress Meter.\n\n\n<a id="org1fa803f"></a>\n\n## Science\n\n-   **jupyter :: Jupyter Notebook + IPython:** Jupyter metapackage. Install all the Jupyter components in\n    one go.\n-   **numpy:** NumPy: array processing for numbers, strings, records, and objects\n-   **pandas:** Powerful data structures for data analysis, time series, and statistics\n-   **sympy:** Computer algebra system (CAS) in Python\n\n\n<a id="orgad6dc64"></a>\n\n## Crawler\n\n-   **requests:** Python HTTP for Humans.\n-   **requests\\_html:** HTML Parsing for Humans.\n-   **BeautifulSoup4:** Screen-scraping library\n\n\n<a id="org855a683"></a>\n\n## Development\n\n-   **cleo:** Cleo allows you to create beautiful and testable command-line interfaces.\n\n\n<a id="org40ecd96"></a>\n\n# Epoligue\n\n\n<a id="orgadfe69c"></a>\n\n## History\n\n\n<a id="org5e9403c"></a>\n\n### 0.2.2 <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-29 Sat&gt;</span></span>\n\n-   **Fix:** now flatten will not flat dict any more.\n\n\n<a id="org40ed255"></a>\n\n### 0.2.1 <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-22 Sat&gt;</span></span>\n\nAdd a new tool flatten\n\n\n<a id="org3476a9f"></a>\n\n### 0.1.1 <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-17 Mon&gt;</span></span>\n\nUse README.md instead of README.org\n\n\n<a id="org51a254c"></a>\n\n### 0.1.0 <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-16 Sun&gt;</span></span>\n\nThe beginning of everything\n',
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
