# permissive-slugify

Fork of [un33k/python-slugify](https://github.com/un33k/python-slugify) to fix [issue 68](https://github.com/un33k/python-slugify/issues/68).

<table>
    <tr>
        <td>License</td>
        <td><img src='https://img.shields.io/pypi/l/permissive-slugify.svg'></td>
        <td>Version</td>
        <td><img src='https://img.shields.io/pypi/v/permissive-slugify.svg'></td>
    </tr>
    <tr>
        <td>Travis CI</td>
        <td><img src='https://travis-ci.org/roniemartinez/permissive-slugify.svg?branch=master'></td>
        <td>Coverage</td>
        <td><img src='https://codecov.io/gh/roniemartinez/permissive-slugify/branch/master/graph/badge.svg'></td>
    </tr>
    <tr>
        <td>AppVeyor</td>
        <td><img src='https://ci.appveyor.com/api/projects/status/srpweajn7vq7hq02/branch/master?svg=true'></td>
        <td>Supported versions</td>
        <td><img src='https://img.shields.io/pypi/pyversions/permissive-slugify.svg'></td>
    </tr>
    <tr>
        <td>Wheel</td>
        <td><img src='https://img.shields.io/pypi/wheel/permissive-slugify.svg'></td>
        <td>Implementation</td>
        <td><img src='https://img.shields.io/pypi/implementation/permissive-slugify.svg'></td>
    </tr>
    <tr>
        <td>Status</td>
        <td><img src='https://img.shields.io/pypi/status/permissive-slugify.svg'></td>
        <td>Downloads</td>
        <td><img src='https://img.shields.io/pypi/dm/permissive-slugify.svg'></td>
    </tr>
    <tr>
        <td>Show your support</td>
        <td><a href='https://saythanks.io/to/roniemartinez'><img src='https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg'></a></td>
    </tr>
</table>

## Improvements

- Support for `extras_require` and `cmdclass`
- Refactored
- Deploy from Travis CI
- Added Appveyor Integration
- Uses `pytest`
- Uses CodeCov

## How to install

By default, permissive-slugify uses [Unidecode](https://github.com/avian2/unidecode) as decoder which is GPL-licensed.

```bash
pip install permissive-slugify
```

### Specifying decoder

You can specify which decoder will be used:

- [Unidecode](https://github.com/avian2/unidecode) - *(GPL-licensed)*.

    ```bash
    pip install permissive-slugify[unidecode]
    easy_install permissive-slugify[unidecode]
    ```

- [text-unidecode](https://github.com/kmike/text-unidecode) *(GPL & Perl Artistic)*

    ```bash
    pip install permissive-slugify[text-unidecode]
    easy_install permissive-slugify[text-unidecode]
    ```

## How to use

```python
# -*- coding: utf-8 -*-
from slugify import slugify

txt = "This is a test ---"
slug = slugify(txt)
assert slug == "this-is-a-test"

txt = '影師嗎'
slug = slugify(txt)
assert slug == "ying-shi-ma"

txt = 'C\'est déjà l\'été.'
slug = slugify(txt)
assert slug == "c-est-deja-l-ete"

txt = 'Nín hǎo. Wǒ shì zhōng guó rén'
slug = slugify(txt)
assert slug == "nin-hao-wo-shi-zhong-guo-ren"

txt = 'Компьютер'
slug = slugify(txt)
assert slug == "kompiuter"

txt = 'jaja---lol-méméméoo--a'
slug = slugify(txt, max_length=9)
assert slug == "jaja-lol"

txt = 'jaja---lol-méméméoo--a'
slug = slugify(txt, max_length=15, word_boundary=True)
assert slug == "jaja-lol-a"

txt = 'jaja---lol-méméméoo--a'
slug = slugify(txt, max_length=20, word_boundary=True, separator=".")
assert slug == "jaja.lol.mememeoo.a"

txt = 'one two three four five'
slug = slugify(txt, max_length=13, word_boundary=True, save_order=True)
assert slug == "one-two-three"

txt = 'the quick brown fox jumps over the lazy dog'
slug = slugify(txt, stopwords=['the'])
assert slug == 'quick-brown-fox-jumps-over-lazy-dog'

txt = 'the quick brown fox jumps over the lazy dog in a hurry'
slug = slugify(txt, stopwords=['the', 'in', 'a', 'hurry'])
assert slug == 'quick-brown-fox-jumps-over-lazy-dog'

txt = 'thIs Has a stopword Stopword'
slug = slugify(txt, stopwords=['Stopword'], lowercase=False)
assert slug == 'thIs-Has-a-stopword'

txt = "___This is a test___"
regex_pattern = r'[^-a-z0-9_]+'
slug = slugify(txt, regex_pattern=regex_pattern)
assert slug == "___this-is-a-test___"

txt = "___This is a test___"
regex_pattern = r'[^-a-z0-9_]+'
slug = slugify(txt, separator='_', regex_pattern=regex_pattern)
assert slug != "_this_is_a_test_"

txt = '10 | 20 %'
slug = slugify(txt, replacements=[['|', 'or'], ['%', 'percent']])
assert slug == "10-or-20-percent"

```

## References

- [Add ability to specify "default" extras_require](https://github.com/pypa/setuptools/issues/1139)
- [setup.py not ran on wheels](https://stackoverflow.com/questions/40433168/running-custom-code-with-pip-install-fails#comment75920547_40434969)

## Author

- Original - [Val Neekman](https://github.com/un33k/python-slugify)
- Modified by [Ronie Martinez](mailto:ronmarti18@gmail.com)