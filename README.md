# Cilantropy

[![Build Status](https://travis-ci.com/foozzi/cilantropy.svg?branch=master)](https://travis-ci.com/foozzi/cilantropy) [![Build Status](https://img.shields.io/docker/cloud/build/fz11/cilantropy)](https://hub.docker.com/r/fz11/cilantropy) 
[![Downloads](https://img.shields.io/pypi/dm/cilantropy)](https://pypi.org/project/cilantropy/) 
[![License](https://img.shields.io/pypi/l/cilantropy)](https://github.com/foozzi/cilantropy/blob/master/LICENSE) 
[![Version Pypi](https://img.shields.io/pypi/v/cilantropy)](https://pypi.org/project/cilantropy/)

Cilantropy is a Python Package Manager interface created to provide an "easy-to-use" visual and also
a command-line interface for Pythonistas. Today we have many nice distribution utilities like pip,
distribute, etc, but we don't have a nice visual approach to inspect current installed packages,
show projects metadata, check for PyPI updates, etc. 

## Demo
[Demo Cilantropy](https://cilantropy.cc/demo/)


## Screenshots

### Screenshot: The home

![The home](https://imgur.com/7dOJWWA.jpg)

### Screenshot: Installed package information

![Installed package information](https://imgur.com/r691yh3.jpg)

### Screenshot: Check PyPI for updates available

![Updates](https://imgur.com/fSI22th.jpg)

![Updates](https://imgur.com/GO5cEcB.jpg)

![Updates](https://imgur.com/zpe2xon.jpg)

### 'plp' (Python List Packages) console utility

[![asciicast](https://asciinema.org/a/cKVaIhb6jOUw5PZMiD2Z2VgF1.svg)](https://asciinema.org/a/cKVaIhb6jOUw5PZMiD2Z2VgF1)

## How to Install

Installing using pip:

    $ pip install cilantropy

Upgrading using pip:

    $ pip install --upgrade cilantropy

### Docker

Repository @ [DockerHub](https://hub.docker.com/r/fz11/cilantropy)

Docker Compose excerpt

```yaml
# Docker Compose excerpt
services:
  nginx-ui:
    image: fz11/cilantropy:latest
    ports:
      - 8080:8080
    volumes:
      - nginx:/etc/nginx
```

### uWSGI
```bash
uwsgi --http 0.0.0.0:5000 --wsgi-file wsgi.py --callable app --processes 1 --threads 8
```

### Installing as a systemd service

If you're running Linux with [systemd](http://www.freedesktop.org/wiki/Software/systemd)
(before edit path and other configs in `contrib/systemd/cilantropy.service`)
installed, you can register Cilantropy as a service by copying `cilantropy.service`
(both in `contrib/systemd`) to `/etc/systemd/system`.

All standard systemd service management commands (e.g. `systemctl enable` and `systemctl start`) apply.

### uWSGI + Nginx

[Manual](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04-ru)

#### Service management

```shell
$ sudo start cilantropy
$ sudo stop cilantropy
$ sudo status cilantropy
```
or
```shell
$ sudo service cilantropy start
$ sudo service cilantropy stop
$ sudo service cilantropy status
```

## Android (Termux)

You can use Cilantropy on your android device with Termux:
![termux](https://i.imgur.com/QMBsvCJ.jpg%5B =200x) ![termux2](https://imgur.com/wNjGwNY.jpg =200x) ![termux3](https://imgur.com/LGad31u.jpg =200x) ![termux4](https://imgur.com/4e5JONy.jpg =200x) ![android](https://imgur.com/kkQKXrG.jpg =200x)

## Authentication

[BasicAuth with nginx](https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-http-basic-authentication/)

In general, this app does not come with authentication. However, it is easy to setup basic auth to restrict unwanted access.
Here is how this can be done when using nginx.

### Configure the auth file

1. Verify that `apache2-utils` (Debian, Ubuntu) or `httpd-tools` (RHEL/CentOS/Oracle Linux) is installed
2. Run the htpasswd utility to create a new user and set a passwort.
    - Make sure, that the directory exists
    - Remove the `-c` flag, if you have created a user before, since it creates the inital user/passwort file
    - `sudo htpasswd -c /etc/apache2/.htpasswd user1`

## Using Cilantropy

You only need to call the script (the -w option will automatically open your browser):

    $ cilantropy -w

## Using plp
  
    $ plp --help
    Cilantropy - Python List Packages (PLP)

    Usage:
      plp list [--compact] [<filter>]
      plp show <project_name>
      plp check <project_name>
      plp scripts [<filter>]
      plp paste [list your packages to pastebin service]

      plp (-h | --help)
      plp --version

    Options:
      --compact     Compact list format
      -h --help     Show this screen.
      --version     Show version.

## Setting a development environment
-------------------------------------------------------------------------------

Developers can setup a development environment using the "develop" command
from setuptools:

    $ git clone git@github.com:foozzi/cilantropy.git && cd cilantropy
    $ pip install flit --user
    $ flit install
    $ cilantropy

## Requirements

Cilantropy uses the following external projects:

[Flask](https://github.com/mitsuhiko/flask)

> A microframework based on Werkzeug, Jinja2 and good intentions

[Bootstrap 4](https://getbootstrap.com/)

> HTML, CSS, and JS toolkit from Bootstrap

[Jinja2](https://github.com/mitsuhiko/jinja2) (Flask requirement)

>The Jinja2 template engine

[Werkzeug](https://github.com/mitsuhiko/werkzeug) (Flask requirement)

> A flexible WSGI implementation and toolkit

[docopt](http://docopt.org/) (used by plp)

> Command-line interface description language

[colorama](https://pypi.python.org/pypi/colorama) (used by plp)

> Cross-platform colored terminal text.

[docutils](http://docutils.sourceforge.net/)

> Docutils is an open-source text processing system for processing plaintext documentation
> into useful formats, such as HTML or LaTeX.

[flit](https://pypi.python.org/pypi/flit) (for build and install package)

> Flit is a simple way to put Python packages and modules on PyPI.

## Compatibility

Cilantropy is compatible with:

  - Python 3

## Supported browsers

Cilantropy is compatible with:

  - Firefox
  - Google Chrome
  - Internet Explorer 9/10
  - Safari

## Reporting bug

Open an issue in Github with the traceback. To get the traceback, you'll 
have to run Cilantropy in debugging mode:

    $ cilantropy -drvi

## License

    Copyright (c) 2020, Tkachenko Igor All rights reserved.

	Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

	1) Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

	2) Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

	3) All advertising materials mentioning features or use of this software must display the following acknowledgement:

	"This product includes software developed by the University of California, Berkeley and its contributors."

	4) Neither the name of the foozzi nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

	THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. 

## Contributors

  See the [Contributors](https://github.com/foozzi/cilantropy/contributors).
  
## Links

[Project Site - Github](https://github.com/foozzi/cilantropy)
