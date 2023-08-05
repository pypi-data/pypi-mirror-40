# Table of Contents

-   [Prologue](#orge7c993d)
-   [Introduction](#org34ce89a)
-   [Usage](#org50b2bae)
    -   [Tools (Libs)](#org6834eee)
        -   [Utility](#org3e067e5)
            -   [Flatten](#orgae92c28)
    -   [Comand Line Tools](#orgd240084)
        -   [Template](#orgf379ee3)
            -   [Crawler](#org7696ae6)
    -   [More](#org2d9dfe6)
-   [Packages](#org0ce3219)
    -   [Normal](#org06b5a3e)
    -   [Science](#org1fa803f)
    -   [Crawler](#orgad6dc64)
    -   [Development](#org855a683)
-   [Epoligue](#org40ecd96)
    -   [History](#orgadfe69c)
        -   [0.2.2 <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-29 Sat&gt;</span></span>](#org5e9403c)
        -   [0.2.1 <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-22 Sat&gt;</span></span>](#org40ed255)
        -   [0.1.1 <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-17 Mon&gt;</span></span>](#org3476a9f)
        -   [0.1.0 <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-16 Sun&gt;</span></span>](#org51a254c)

Here is everything frequently use in python.


<a id="orge7c993d"></a>

# Prologue

I often need to configure a new Python development environment.  Whether it is to help others or for
myself, it is very troublesome to manage packages with pip.  Besides, there are fascinating and
impressive ipython extensions, and every installation of them has to bother Google again.

Therefore, I created this napy.

*This package is still under development, and although is only for myself now, you can use it as you
like.*


<a id="org34ce89a"></a>

# Introduction

Napy includes some packages that I frequently use in python, such as `requests`, for crawlers; `sympy`
for mathematics.  Also, napy has some ipython extensions I write.  A template Napy also has that I
often use (of course, it's still straightforward now).  Hope you like it.

*Due to the `.dir-local.el` contains `(org-html-klipsify-src . nil)`, it is warning that it is not safe.*


<a id="org50b2bae"></a>

# Usage


<a id="org6834eee"></a>

## Tools (Libs)


<a id="org3e067e5"></a>

### Utility


<a id="orgae92c28"></a>

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


<a id="orgd240084"></a>

## Comand Line Tools


<a id="orgf379ee3"></a>

### Template


<a id="org7696ae6"></a>

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


<a id="org2d9dfe6"></a>

## More

Still under development.


<a id="org0ce3219"></a>

# Packages


<a id="org06b5a3e"></a>

## Normal

-   **better\_exceptions:** Pretty and helpful exceptions, automatically.
-   **pendulum:** Python datetimes made easy.
-   **tqdm:** Fast, Extensible Progress Meter.


<a id="org1fa803f"></a>

## Science

-   **jupyter :: Jupyter Notebook + IPython:** Jupyter metapackage. Install all the Jupyter components in
    one go.
-   **numpy:** NumPy: array processing for numbers, strings, records, and objects
-   **pandas:** Powerful data structures for data analysis, time series, and statistics
-   **sympy:** Computer algebra system (CAS) in Python


<a id="orgad6dc64"></a>

## Crawler

-   **requests:** Python HTTP for Humans.
-   **requests\_html:** HTML Parsing for Humans.
-   **BeautifulSoup4:** Screen-scraping library


<a id="org855a683"></a>

## Development

-   **cleo:** Cleo allows you to create beautiful and testable command-line interfaces.


<a id="org40ecd96"></a>

# Epoligue


<a id="orgadfe69c"></a>

## History


<a id="org5e9403c"></a>

### 0.2.2 <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-29 Sat&gt;</span></span>

-   **Fix:** now flatten will not flat dict any more.


<a id="org40ed255"></a>

### 0.2.1 <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-22 Sat&gt;</span></span>

Add a new tool flatten


<a id="org3476a9f"></a>

### 0.1.1 <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-17 Mon&gt;</span></span>

Use README.md instead of README.org


<a id="org51a254c"></a>

### 0.1.0 <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-16 Sun&gt;</span></span>

The beginning of everything
