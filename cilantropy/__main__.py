from optparse import OptionParser
import logging
from .cilantropy import app
from .settings import __version__, __author__

def run_main():
    """ The main entry-point of Cilantropy. """

    print('Cilantropy %s - Python Package Manager' % (__version__,))
    print('By %s 2020\n' % (__author__,))
    parser = OptionParser()

    parser.add_option('-s', '--host', dest='host',
                    help='The hostname to listen on, ' \
                         'set to \'0.0.0.0\' to have the '
                         'server available externally as well. '
                         'Default is \'127.0.0.1\' (localhost only).',
                    metavar="HOST", default='127.0.0.1')

    parser.add_option('-d', '--debug', action='store_true',
                  help='Start Cilantropy in Debug mode (useful to report bugs).',
                  dest='debug', default=False)

    parser.add_option('-r', '--reloader', action='store_true',
                  help='Uses the reloader.', dest='reloader', default=False)

    parser.add_option('-i', '--interactive', action='store_true',
                  help='Enable the interactive interpreter' \
                       ' for debugging (useful to debug errors).',
                  dest='evalx', default=False)

    parser.add_option('-p', '--port', dest='port',
                    help='The port to listen on. ' \
                         'Default is the port \'5000\'.',
                    metavar="PORT", default='5000')

    parser.add_option('-v', '--verbose', dest='verbose', action='store_true',
                    help='Turn on verbose messages (show HTTP requests).' \
                         ' Default is False.',
                    default=False)

    parser.add_option('-w', '--web-browser', dest='web_browser', action='store_true',
                    help='Open a web browser to show Cilantropy.' \
                         ' Default is False.',
                    default=False)

    (options, args) = parser.parse_args()

    if not options.verbose:
        print(" * Running on http://%s:%s/" % (options.host, options.port))
        werk_log = logging.getLogger('werkzeug')
        werk_log.setLevel(logging.WARNING)

    if options.web_browser:
        import webbrowser
        webbrowser.open('http://%s:%s/' % (options.host, options.port))

    app.run(debug=options.debug, host=options.host, port=int(options.port),
            use_evalex=options.evalx, use_reloader=options.reloader)

if __name__ == '__main__':
    run_main()
