![ebook_homebrew](https://raw.githubusercontent.com/tubone24/ebook_homebrew/master/doc_src/bookicon.png
 "ebook_homebrew_icon")


# ebook_homebrew

[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![Build Status](https://travis-ci.org/tubone24/ebook_homebrew.svg?branch=master)](https://travis-ci.org/tubone24/ebook_homebrew)
[![codecov](https://codecov.io/gh/tubone24/ebook_homebrew/branch/master/graph/badge.svg)](https://codecov.io/gh/tubone24/ebook_homebrew)
[![Maintainability](https://api.codeclimate.com/v1/badges/a3e2d70a87998a18e225/maintainability)](https://codeclimate.com/github/tubone24/ebook_homebrew/maintainability)

Change file name to only digit name like `001.jpg` and make e-book format files.

##Getting Started

Ebook_homebrew is a python package, so that you can use `setup.py` or `pip` installer.

###Using setup.py

```bash
$ pip install -r requirements.txt
$ python setup.py install
```

###Or using pip installer

Unimplemented

```bash
$ pip install ebook_homebrew
```

## Usage

You can use global command "ebookhomebrew".

Show help.

```bash
$ ebookhomebrew -h
```

Ex) Rename image file to only digit and Create PDF file.

```bash
$ ebookhomebrew auto -s ./tests -d 3,4 -e jpg -f test.pdf
```

### ebookhomebrew command line interface

#### Subcommands

```bash
  Choose subcommands. Usually choose "auto"

  {auto}
    auto      Make only digit file name, convert e-book file such as PDF
```

#### Options

```bash
  -h, --help            show this help message and exit
  -s SRC_DIR, --src_dir SRC_DIR
                        Source directory which put original image files.
  --dst_dir DST_DIR     Destination directory which put e-book file.
  -d N,N, --digit N,N   Serial number digits you remain file name
  -e EXT, --extension EXT
                        Destination directory which put e-book file.
  -f FILENAME, --filename FILENAME
                        Destination directory which put e-book file.
  -m, --manual          Duplicate file name, solving manually.
  -r, --remove          Remove original image file.
  -y, --assume_yes      no verify users.
```

## Testing

### Unit Test

Using pytest, if you want to test.

```bash
pytest
```

If you get coverage report, run coverage and report.

```bash
$ coverage run --source=ebook_homebrew -m pytest
$ coverage report -m
```

Or pytest-cov param for pytest

```bash
$ pytest --cov=ebook_homebrew --cov-report html --cov-report xml
```

### Integration Test

Using pytest, if you want to test with mark "--it"

```bash
pytest --it
```

### With tox

With tox, you can test multiple python version.(only python3.5, 3.6)

```bash
tox
```

### Travis-CI

This repository uses [Travis-CI](https://travis-ci.org/) and be building jobs by push or PR branches.

## Licence

This software is released under the MIT License, see LICENSE.

## API Document

See 

[Sphinxdocument](http://tubone24.github.io/ebook_homebrew/)
# Changelog

## [v1.0.0](https://github.com/tubone24/ebook_homebrew/releases/tag/v1.0.0) (2019-1-14)

First release.
The MIT License (MIT)

Copyright (c) 2019 tubone

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


