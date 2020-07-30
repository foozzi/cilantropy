"""
.. module:: main
   :platform: Unix, Windows
   :synopsis: Main Cilantropy entry-point.

:mod:`main` -- main Cilantropy entry-point
==================================================================
"""

import requests
    
from docutils.core import publish_parts
import pkg_resources as _pkg_resources

from flask import Flask
from flask import render_template
from flask import url_for
from flask import jsonify
from flask import abort
from flask import json

from . import metadata
from .helpers import Crumb
from .helpers import get_pkg_res
from .helpers import get_shared_data
from .helpers import get_pypi_releases
from .helpers import get_sys_info
from .helpers import create_paste_template
from .helpers import DIST_PYPI_CACHE
from .helpers import is_venv
from .helpers import check_pypi_stable_version
from .helpers import get_description_from_remote

from .settings import __version__
from .settings import __author__
from .settings import __author_url__
from .settings import TEKNIK_PASTE_API

from .dist_worker import Updater


app = Flask(__name__)


@app.route('/pypi/upgrade/<dist_name>')
def pypi_upgrade(dist_name):
    """ Upgrade package and return installation-log
    to web interface.

    :param dist_name: distribution name
    :rtype: text
    :return installation-log text
    """
    pkg_res = get_pkg_res()
    try:
        pkg_dist_version = pkg_res.get_distribution(dist_name).version
    except _pkg_resources.DistributionNotFound:
        abort(404)

    updater = Updater(dist_name)    
    res, status_code = updater.upgrade()

    if not status_code:
        DIST_PYPI_CACHE.remove(dist_name.lower())

    return render_template('pypi_upgrade.html', result=res.strip(), 
        status_code=status_code)

@app.route('/pypi/check_update/<dist_name>')
def check_pypi_update(dist_name):
    """ Just check for updates and return a json
    with the attribute "has_update".

    :param dist_name: distribution name
    :rtype: json
    :return: json with the attribute "has_update"
    """
    pkg_res = get_pkg_res()
    try:
        pkg_dist_version = pkg_res.get_distribution(dist_name).version
    except _pkg_resources.DistributionNotFound:
        abort(404)

    pypi_last_version = check_pypi_stable_version(dist_name)

    if pypi_last_version:
        current_version = pkg_res.parse_version(pkg_dist_version)

        if str(pypi_last_version) > str(current_version):
            DIST_PYPI_CACHE.add(dist_name.lower())
            return jsonify({"has_update": 1})

    try:
        DIST_PYPI_CACHE.remove(dist_name.lower())
    except KeyError:
        pass

    return jsonify({"has_update": 0})


@app.route('/pypi/releases/<dist_name>')
def releases(dist_name):
    """ This is the /pypi/releases/<dist_name> entry point, it is the interface
    between Cilantropy and the PyPI RPC service when checking for updates.

    :param dist_name: the package name (distribution name).
    """
    pkg_res = get_pkg_res()    

    data = {}
    try:
        pkg_dist_version = pkg_res.get_distribution(dist_name).version
    except _pkg_resources.DistributionNotFound:
        abort(404)

    pypi_rel = get_pypi_releases(dist_name)
    pypi_last_version = check_pypi_stable_version(dist_name)

    data["dist_name"] = dist_name
    data["pypi_info"] = pypi_rel
    data["current_version"] = pkg_dist_version
    data['is_venv'] = is_venv()

    if pypi_rel:
        current_version = pkg_res.parse_version(pkg_dist_version)
        if pypi_last_version:
            last_version = str(pkg_dist_version).lower() != str(pypi_rel[0]).lower()
            data["last_is_great"] = str(pypi_last_version) > str(current_version)
        else: 
            last_version = True
            data["last_is_great"] = False
        
        data["last_version_differ"] = last_version

        if data["last_is_great"]:
            DIST_PYPI_CACHE.add(dist_name.lower())
        else:
            try:
                DIST_PYPI_CACHE.remove(dist_name.lower())
            except KeyError:
                pass

    return render_template('pypi_update.html', **data)


@app.route('/')
def index():
    """ The main Flask entry-point (/) for the Cilantropy server. """
    data = {'breadpath': [Crumb('Main')]}

    data.update(get_shared_data())
    data['menu_home'] = 'active'    
    data['system_information'] = get_sys_info()

    return render_template('system_information.html', **data)


@app.route('/console_scripts')
def console_scripts():
    """ Entry point for the global console scripts """
    data = {}
    data.update(get_shared_data())
    data['menu_console_scripts'] = 'active'
    data['breadpath'] = [Crumb('Console Scripts')]

    entry_console = get_pkg_res().iter_entry_points('console_scripts')
    data['scripts'] = entry_console

    return render_template('console_scripts.html', **data)


@app.route('/about')
def about():
    """ The About entry-point (/about) for the Cilantropy server. """

    data = {}
    data.update(get_shared_data())
    data['menu_about'] = 'active'

    data['breadpath'] = [Crumb('About')]
    data['version'] = __version__
    data['author'] = __author__
    data['author_url'] = __author_url__

    return render_template('about.html', **data)


@app.route('/paste_pkgs')
def paste_pkg():
    """ Entry-point for publish a Cilantropy list of installed packages """

    template_data = create_paste_template()

    res = requests.post(TEKNIK_PASTE_API, data={"code": template_data})
    if 'result' in res.json():
        return jsonify({'result': res.json()['result']['url'], 'error': False})
    else:
        return jsonify({'result': None, 'error': True})


@app.route('/distribution/<dist_name>')
def distribution(dist_name=None):
    """ The Distribution entry-point (/distribution/<dist_name>)
    for the Cilantropy server.

    :param dist_name: the package name
    """
    try:
        pkg_dist = get_pkg_res().get_distribution(dist_name)
    except _pkg_resources.DistributionNotFound:
        abort(404)

    data = {}
    data.update(get_shared_data())

    data['dist'] = pkg_dist
    data['breadpath'] = [Crumb('Main', url_for('index')),
                         Crumb('Package'), Crumb(pkg_dist.project_name)]

    settings_overrides = {
        'raw_enabled': 0,  # no raw HTML code
        'file_insertion_enabled': 0,  # no file/URL access
        'halt_level': 2,  # at warnings or errors, raise an exception
        'report_level': 5,  # never report problems with the reST code
    }

    try:
        pkg_metadata = pkg_dist.get_metadata(metadata.METADATA_NAME[0])
    except FileNotFoundError:
        pkg_metadata = pkg_dist.get_metadata(metadata.METADATA_NAME[1])
    except FileNotFoundError:
        pass

    parsed, key_known = metadata.parse_metadata(pkg_metadata)
    distinfo = metadata.metadata_to_dict(parsed, key_known)    

    parts = None
    """ get description from pep-0426 """
    if distinfo['metadata-version'] == '2.0':    
        distinfo['description'] = pkg_dist.get_metadata(metadata.DESCRIPTION_2_0[0])    
        try:
            parts = publish_parts(source=distinfo['description'],
                          writer_name='html',
                          settings_overrides=settings_overrides)
        except:
            pass

    try:
        parts = publish_parts(source=distinfo['description'],
                              writer_name='html',
                              settings_overrides=settings_overrides)
    except:
        pass

    data['distinfo'] = distinfo
    data['entry_map'] = pkg_dist.get_entry_map()
    data['location'] = '{}/{}'.format(pkg_dist.location, dist_name)
    data['pypi_update_cache'] = DIST_PYPI_CACHE
    data['is_venv'] = is_venv()

    if parts is not None:
        data['description_render'] = parts['body']

    return render_template('distribution.html', **data)


