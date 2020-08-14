"""
.. module:: helpers
   :platform: Unix, Windows
   :synopsis: Cilantropy helpers entry-point.

:mod:`helpers` -- Cilantropy helpers entry-point
==================================================================
"""

try:
    reload
except NameError:
    from importlib import reload

import os
import sys
import json
import platform
import pkg_resources as _pkg_resources
from pip._vendor.packaging.version import parse
import xmlrpc.client

from jinja2 import Template

import requests

from colorama import Fore
from colorama import Style


# Entry-point for check stable version packages
URL_PATTERN_INFO_DIST = "https://pypi.python.org/pypi/{package}/json"
URL_PATTERN_INFO_DIST_VERSION = "https://pypi.org/pypi/{package}/{version}/json"
PASTE_PKG_TEMPLATE = "paste_pkg_template.html"

# This is a cache with flags to show if a distribution
# has an update available
DIST_PYPI_CACHE = set()

PYPI_XMLRPC = "http://pypi.python.org/pypi"


class Crumb(object):
    """ Represents each level on the bootstrap breadcrumb. """

    def __init__(self, title, href="#"):
        """Instatiates a new breadcrum level.

        :param title: the title
        :param href: the link
        """
        self.title = title
        self.href = href


def get_pkg_res():
    reload(_pkg_resources)
    return _pkg_resources


def get_shared_data():
    """Returns a new dictionary with the shared-data between different
    Cilantropy views (ie. a lista of distribution packages).

    :rtype: dict
    :return: the dictionary with the shared data.
    """
    shared_data = {
        "pypi_update_cache": DIST_PYPI_CACHE,
        "distributions": [d for d in get_pkg_res().working_set],
    }

    return shared_data


def get_pypi_proxy():
    """Returns a RPC ServerProxy object pointing to the PyPI RPC
    URL.

    :rtype: xmlrpclib.ServerProxy
    :return: the RPC ServerProxy to PyPI repository.
    """
    return xmlrpc.client.ServerProxy(PYPI_XMLRPC)


def get_pypi_releases(dist_name):
    """Return the releases available at PyPI repository and sort them using
    the pkg_resources.parse_version, the lastest version is on the 0 index.

    :param dist_name: the distribution name
    :rtype: list
    :return: a list with the releases available at PyPI
    """
    pypi = get_pypi_proxy()

    show_hidden = True
    ret = pypi.package_releases(dist_name, show_hidden)

    if not ret:
        ret = pypi.package_releases(dist_name.capitalize(), show_hidden)

    ret.sort(key=lambda v: _pkg_resources.parse_version(v), reverse=True)

    return ret


def get_description_from_remote(dist_name, version):
    """Just returned description from remote
    repository pypi

    :param: dist_name: the disctribution name
    :param: version: the disctribution version
    :rtype: string
    :return: disctribution desctiption text
    """
    req = requests.get(
        URL_PATTERN_INFO_DIST_VERSION.format(package=dist_name, version=version)
    )

    if req.status_code == requests.codes.ok:
        try:
            return req.json()["info"]["description"]
        except:
            return None
    else:
        return None


def check_pypi_stable_version(dist_name):
    """Return last stable version package from pypi.org

    :param dist_name: the distribution name
    :rtype: string
    :return lastest stable version string (like 1.1.0)
    """
    req = requests.get(URL_PATTERN_INFO_DIST.format(package=dist_name))
    version = parse("0")
    if req.status_code == requests.codes.ok:
        j = json.loads(req.text)
        releases = j.get("releases", [])
        for release in releases:
            ver = parse(release)
            if not ver.is_prerelease:
                version = max(version, ver)
    else:
        return False

    return version


def get_pypi_search(spec, operator="or"):
    """Search the package database using the indicated search spec

    The spec may include any of the keywords described in the above list
    (except 'stable_version' and 'classifiers'), for example: {'description': 'spam'}
    will search description fields. Within the spec, a field's value can be a string
    or a list of strings (the values within the list are combined with an OR), for
    example: {'name': ['foo', 'bar']}. Valid keys for the spec dict are listed here.

    name
    version
    author
    author_email
    maintainer
    maintainer_email
    home_page
    license
    summary
    description
    keywords
    platform
    download_url

    Arguments for different fields are combined using either "and" (the default) or "or".
    Example: search({'name': 'foo', 'description': 'bar'}, 'or'). The results are
    returned as a list of dicts {'name': package name, 'version': package release version,
    'summary': package release summary}
    browse(classifiers)
    """
    pypi = get_pypi_proxy()
    ret = pypi.search(spec, operator)
    ret.sort(key=lambda v: v["_pypi_ordering"], reverse=True)
    return ret


def get_sys_info():
    """ Collect main system and python info """

    sys_info = {
        "Python Platform": sys.platform,
        "Python Version": sys.version,
        "Python Prefix": sys.prefix,
        "Machine Type": platform.machine(),
        "Platform": platform.platform(),
        "Processor": platform.processor(),
    }

    try:
        sys_info["Python Implementation"] = platform.python_implementation()
    except:
        pass

    sys_info["System"] = platform.system()
    sys_info["System Arch"] = platform.architecture()

    return sys_info


def create_paste_template():
    """ Create template with system info and packages list """

    sys_info = get_sys_info()

    with open(
        os.path.join(
            os.path.dirname(__file__), "templates/{}".format(PASTE_PKG_TEMPLATE)
        ),
        "r",
    ) as file:
        template = Template(file.read())

        template_data = template.render(
            packages=get_shared_data(),
            python_platform=sys_info["Python Platform"],
            python_version=sys_info["Python Version"],
            python_prefix=sys_info["Python Prefix"],
            python_implementation=sys_info["Python Implementation"],
        )

        return template_data


# helper functions for 'plp'


def ellipsize(msg, max_size=80):
    """This function will ellipsize the string.

    :param msg: Text to ellipsize.
    :param max_size: The maximum size before ellipsizing,
                                    default is 80.
    :return: The ellipsized string if len > max_size, otherwise
                     the original string.
    """
    if len(msg) >= max_size:
        return "%s (...)" % msg[0 : max_size - 6]
    else:
        return msg


def parse_dict(mdata, key, ellip=False):
    """This function will read the field from the dict and
    if not present will return the string 'Not Specified'

    :param mdata: the distribution info dict
    :param key: the key of the dict
    :ellip: if it will ellipsize
    :return: the string message or 'Not Specified' if empty
    """
    try:
        data = mdata[key]
        if ellip:
            return ellipsize(data)
        else:
            return data
    except KeyError:
        return "Not Specified"


def get_kv_colored(key, value):
    text = Fore.WHITE + Style.BRIGHT + "  %s: " % key.capitalize()
    text += Fore.WHITE + Style.NORMAL + value
    return text


def get_field_formatted(mdata, key):
    """This function will get the formatted and colored
    key data from the dictionary.

    :param mdata: distribution dict
    :param key: the key of the dict
    :return: the formatted and colored string
    """

    def recursive_dict(d, depth=2, final=""):
        final_str = final
        for k, v in sorted(d.items(), key=lambda x: x[0]):
            if isinstance(v, dict):
                if depth == 2:
                    final_str += Fore.BLUE + Style.BRIGHT
                else:
                    final_str += Fore.WHITE + Style.NORMAL

                final_str += "  " * depth + str(k) + "\n"
                final_str += recursive_dict(v, depth + 1, final)
            else:
                final_str = +"  " * depth + str(k) + " " + str(v) + "\n"
        return final_str

    field = parse_dict(mdata, key.lower())

    if isinstance(field, list):
        field = ", ".join(field)

    if isinstance(field, dict):
        field = "\n\n" + recursive_dict(field)

    text = get_kv_colored(key, field)
    return text


# helper functions for dist_worker


def is_venv():
    """Just check is cilantropy in vitrual environment

    :rtype boolean
    :return True if Cilantropy now in virtual envitonment
    or False if not
    """
    return hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    )
