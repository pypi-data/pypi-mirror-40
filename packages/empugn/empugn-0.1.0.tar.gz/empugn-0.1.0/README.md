# Empugn – Generate HTML or XML from YAML or JSON

More an experiment than a serious attempt at making a HTML template engine. But if you're going to use it, you may find it works well together with [Emrichen](https://github.com/con2/emrichen).

An Empugn template looks like this:

```yaml
html:
  - head:
      - title: Empugn example
      - link:
          rel: stylesheet
          href: foo.css
      - script: |
          alert('Hello, World');
  - body:
      - h1: Sole text child may be specified as-is
      - p:
          - "Separating links by "
          - a:
              href: https://google.com
              target: _blank
              children: space
          - " may require quoting"
```

Or with Emrichen:

```yaml
!Defaults
title: Empugn example with Emrichen
greeting: Hello, Emrichen
---
html:
  - head:
      - title: !Var title
      - link:
          rel: stylesheet
          href: foo.css
      - script: !Format "alert({greeting!r});"
  - body:
      - h1: !Var title
```

## Installation

Python 3.5+ required. Python 2 is not and will not be supported.

Optional dependencies:

* YAML support requires [PyYAML](https://pypi.org/project/PyYAML/)
* Emrichen support requires… well… [Emrichen](https://pypi.org/project/emrichen/)

The recommended way to instal Empugn is

    pip install empugn[emrichen]

Plain `empugn` gives you JSON support only. For Empugn with YAML support but no Emrichen, use `empugn[yaml]`.

## CLI

```
usage: empugn [-h] [--template-format {yaml,json}] [--output-file OUTPUT_FILE]
              [--indent INDENT] [--use-emrichen] [--var-file VAR_FILE]
              [--define VAR=VALUE] [--include-env]
              [template_file]

Generate HTML or XML from YAML or JSON

positional arguments:
  template_file         The YAML or JSON template to process. If unspecified,
                        the template is read from stdin.

optional arguments:
  -h, --help            show this help message and exit
  --template-format {yaml,json}
                        Template format. If unspecified, attempted to be
                        autodetected from the input filename (but defaults to
                        YAML).
  --output-file OUTPUT_FILE, -o OUTPUT_FILE
                        Output file. If unspecified, the HTML/XML output is
                        written into stdout.
  --indent INDENT, -i INDENT
                        Indent output. If integer, this many spaces will be
                        used. If string, will be used literally. To disable
                        indentation, pass in the empty string.
  --use-emrichen, -r    Use Emrichen to process tags, making Empugn a full
                        featured HTML template engine. Emrichen must be
                        installed.
  --var-file VAR_FILE, -f VAR_FILE
                        (Implies --use-emrichen) A YAML file containing an
                        object whose top-level keys will be defined as
                        variables. May be specified multiple times.
  --define VAR=VALUE, -D VAR=VALUE
                        (Implies --use-emrichen) Defines a single variable.
                        May be specified multiple times.
  --include-env, -e     (Implies --use-emrichen) Expose process environment
                        variables to the template.
```

## Python API

Simple usage:

```python
from empugn import empugn

# In goes parsed JSON/YAML, out comes string
empugn({'html': []})  # -> '<html></html>'
```

Usage with Emrichen:

```python
from empugn import empugn
from emrichen import Context, Template

template_yaml = '…'
template = Template.parse(template)  # or Template(…)
context = Context({'var': 'value'})
data, = Template.enrich(context)
empugn(data)
```

## Why is it called Empugn?

The name Empugn is a play on Emrichen, [Pug](https://pugjs.org/) and _impugn_.

## License

    The MIT License (MIT)

    Copyright © 2018–2019 Santtu Pajukanta
    Copyright © 2018–2019 Aarni Koskela

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
