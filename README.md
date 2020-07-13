# Cilantropy

[![Build Status](https://travis-ci.com/foozzi/cilantropy.svg?branch=master)](https://travis-ci.com/foozzi/cilantropy) [![Build Status](https://img.shields.io/docker/cloud/build/fz11/cilantropy)](https://hub.docker.com/r/fz11/cilantropy) 


Cilantropy is a Python Package Manager interface created to provide an "easy-to-use" visual and also
a command-line interface for Pythonistas. Today we have many nice distribution utilities like pip,
distribute, etc, but we don't have a nice visual approach to inspect current installed packages,
show projects metadata, check for PyPI updates, etc. 

## Screenshots

### Screenshot: The home

![The home](https://user-images.githubusercontent.com/1178208/87153409-1892ba80-c2c0-11ea-9a48-be7f2e5ed34d.png)

### Screenshot: Installed package information

![Installed package information](https://user-images.githubusercontent.com/1178208/87153582-614a7380-c2c0-11ea-944e-73b3c8f2c21c.png)

### Screenshot: Check PyPI for updates available

![Updates](https://user-images.githubusercontent.com/1178208/87153686-8939d700-c2c0-11ea-8aee-42e650086e38.png)

![Updates](https://user-images.githubusercontent.com/1178208/87153749-a078c480-c2c0-11ea-9865-1f04bd132581.png)

![Updates](https://user-images.githubusercontent.com/1178208/87153797-b71f1b80-c2c0-11ea-94d6-488335e867a6.png)

### 'plp' (Python List Packages) console utility

[![asciicast](https://asciinema.org/a/RqK3NwgKPzVvrjmfmaUtpMKno.svg)](https://asciinema.org/a/RqK3NwgKPzVvrjmfmaUtpMKno)

## How to Install

Installing using pip:

    $ pip install cilantropy

Upgrading using pip:

    $ pip install --upgrade cilantropy

or using easy install:

Installing using easy_install:

    $ easy_install cilantropy

Upgrading using easy_install:

    $ easy_install -U cilantropy

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
uwsgi --http 0.0.0.0:8080 --wsgi-file wsgi.py --callable app --processes 1 --threads 8
```

### Installing as a systemd service

If you're running Linux with [systemd](http://www.freedesktop.org/wiki/Software/systemd)
installed, you can register Cilantropy as a service by copying `cilantropy.service`
and `cilantropy` (both in `contrib/systemd`) to `/etc/systemd/system` and
`/etc/conf.d`, respectively.

All standard systemd service management commands (e.g. `systemctl enable` and `systemctl start`) apply.

### Installing as an Upstart service

On Linux systems having [Upstart](http://upstart.ubuntu.com/) you can set up Cilantropy as a service easily as follow.

- copy `contrib/upstart/cilantropy.conf` to `/etc/init/`
- make a symbolic link for it in `/etc/init.d/`:

    ```shell
    $ ln -s /etc/init/cilantropy.conf /etc/init.d/cilantropy
    ```
- copy `contrib/upstart/cilantropy` to `/etc/default/`

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

#### Service customization

You can customize the host and port the cilantropy service will be listening on by editing the file `/etc/default/cilantropy`.

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

    $ python setup.py develop
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
