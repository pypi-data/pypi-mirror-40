# Table of Contents

-   [Prologue](#org76774da)
-   [Introduction](#org96a0d13)
-   [Usage](#org08dde91)
    -   [Tools (Libs)](#org32fac2d)
        -   [Utility](#org2f3eb3e)
            -   [Flatten](#orgd29860a)
    -   [Comand Line Tools](#org219e84d)
        -   [Template](#orgb5b1237)
            -   [Crawler](#orgafe8f23)
    -   [More](#orga4b15d9)
-   [Packages](#orga721f60)
    -   [Normal](#org4b4510a)
    -   [Science](#org4034141)
    -   [Crawler](#orgc3f72b5)
    -   [Development](#org5b345b8)
-   [Epoligue](#org2f16717)
    -   [History](#org111d8b7)
        -   [0.2.1 <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-22 Sat&gt;</span></span>](#org00f2e11)
        -   [0.1.1 <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-17 Mon&gt;</span></span>](#org0808725)
        -   [0.1.0 <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-16 Sun&gt;</span></span>](#orgade8c74)

Here is everything frequently use in python.


<a id="org76774da"></a>

# Prologue

I often need to configure a new Python development environment.  Whether it is to help others or for
myself, it is very troublesome to manage packages with pip.  Besides, there are fascinating and
impressive ipython extensions, and every installation of them has to bother Google again.

Therefore, I created this napy.

*This package is still under development, and although is only for myself now, you can use it as you
like.*


<a id="org96a0d13"></a>

# Introduction

Napy includes some packages that I frequently use in python, such as `requests`, for crawlers; `sympy`
for mathematics.  Also, napy has some ipython extensions I write.  A template Napy also has that I
often use (of course, it's still straightforward now).  Hope you like it.

*Due to the `.dir-local.el` contains `(org-html-klipsify-src . nil)`, it is warning that it is not safe.*


<a id="org08dde91"></a>

# Usage


<a id="org32fac2d"></a>

## Tools (Libs)


<a id="org2f3eb3e"></a>

### Utility


<a id="orgd29860a"></a>

#### Flatten

Flatten list of iterable objects.

    from napy.tools import flatten, flatten_str

    list(flatten([1, 2, "ab", [3, "c", [4, ["d"]]]]))
    # [1, 2, "ab", 3, "c", 4, "d"]

    list(flatten("abc"))
    # ["a", "b", "c"]
    # regard "abc" as ["a", "b", "c"]

    list(flatten_str([1, 2, "ab", [3, "c", [4, ["d"]]]]))
    # or list(flatten([1, 2, "ab", [3, "c", [4, ["d"]]]], True))
    # [1, 2, "a", "b", 3, "c", 4, "d"]


<a id="org219e84d"></a>

## Comand Line Tools


<a id="orgb5b1237"></a>

### Template


<a id="orgafe8f23"></a>

#### Crawler

    $ napy template --help
    Usage:
      template [options]

    Options:
      -c, --category[=CATEGORY]       Category of template
      -o, --output[=OUTPUT]           Output file (default: "stdout")
      -y, --yes                       Confirmation
      -h, --help                      Display this help message
      -q, --quiet                     Do not output any message
      -V, --version                   Display this application version
          --ansi                      Force ANSI output
          --no-ansi                   Disable ANSI output
      -n, --no-interaction            Do not ask any interactive question
      -v|vv|vvv, --verbose[=VERBOSE]  Increase the verbosity of messages: 1 for normal output, 2 for more verbose output and 3 for debug

    Help:
     Template command line tool.

It will generate this:

    from requests_html import HtmlSession as s
    import requests as req


    def crawler() -> None:
        """Crawler."""
        pass


    if __name__ == "__main__":
        pass


<a id="orga4b15d9"></a>

## More

Still under development.


<a id="orga721f60"></a>

# Packages


<a id="org4b4510a"></a>

## Normal

-   **better\_exceptions:** Pretty and helpful exceptions, automatically.
-   **pendulum:** Python datetimes made easy.
-   **tqdm:** Fast, Extensible Progress Meter.


<a id="org4034141"></a>

## Science

-   **jupyter :: Jupyter Notebook + IPython:** Jupyter metapackage. Install all the Jupyter components in
    one go.
-   **numpy:** NumPy: array processing for numbers, strings, records, and objects
-   **pandas:** Powerful data structures for data analysis, time series, and statistics
-   **sympy:** Computer algebra system (CAS) in Python


<a id="orgc3f72b5"></a>

## Crawler

-   **requests:** Python HTTP for Humans.
-   **requests\_html:** HTML Parsing for Humans.
-   **BeautifulSoup4:** Screen-scraping library


<a id="org5b345b8"></a>

## Development

-   **cleo:** Cleo allows you to create beautiful and testable command-line interfaces.


<a id="org2f16717"></a>

# Epoligue


<a id="org111d8b7"></a>

## History


<a id="org00f2e11"></a>

### 0.2.1 <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-22 Sat&gt;</span></span>

Add a new tool flatten


<a id="org0808725"></a>

### 0.1.1 <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-17 Mon&gt;</span></span>

Use README.md instead of README.org


<a id="orgade8c74"></a>

### 0.1.0 <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-16 Sun&gt;</span></span>

The beginning of everything
