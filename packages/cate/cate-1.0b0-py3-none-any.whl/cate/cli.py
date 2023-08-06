# -*- coding: utf-8 -*-

"""
Logic to handle the Command Line Interface (CLI).
"""

import argparse as _argparse
import json as _json
import logging as _logging
import logging.config as _logging_config
import os as _os
import textwrap as _textwrap

from . import main as _main
from . import __name__ as _pkgname  # name of the main package (i.e., the app)
from . import __version__


logger = _logging.getLogger(__name__)  # pylint: disable=invalid-name


# XXX: SCALE_BOUNDS constant tuple introduces a strong coupling between this
# module and the drawing module: consider defining the constant tuple in the
# drawing module and importing it.
SCALE_BOUNDS = (0.5, 3.0)


def _bounded_float(inf, sup):
    """
    Create a suitable callable for `argparse.add_argument` `type=` argument.

    The returned callable converts the string into a float, and checks the
    converted value falls within [inf, sup] (inclusive set).
    """
    def _type(string):
        value = float(string)
        if inf <= value and value <= sup:
            return value
        else:
            msg = '{} does not fall within [{}, {}].'.format(value, inf, sup)
            raise _argparse.ArgumentTypeError(msg)
    return _type


def _create_parser():
    parser = _argparse.ArgumentParser(
        prog=_pkgname,
        formatter_class=_argparse.RawDescriptionHelpFormatter,
        description='Draw the templates of chaotic attractors.',
        epilog=_textwrap.dedent(
            f'''
            To read a matrix from a file whose name starts with a '-' for example
            '-foo.json', use one of these commands:
              {_pkgname} -- -foo.json

              {_pkgname} ./-foo.json
            '''
        ),
    )
    parser.add_argument(
        '--version',
        action='version',
        version='{} {}'.format(_pkgname, __version__),
    )
    parser.add_argument(
        '-s', '--scale',
        default=1.0,
        type=_bounded_float(*SCALE_BOUNDS),
        help='Alter scale of the template.' \
            ' The scale value must reside between {} and {}.'.format(*SCALE_BOUNDS),
    )
    parser.add_argument(
        '-t', '--complete-flow',
        action='store_true',
        help='Add semicircles depicting the complete flow of the attractor.',
    )
    parser.add_argument(
        '-c', '--no-color',
        action='store_false',
        help='Do not color the template.',
        dest='color',
    )
    parser.add_argument(
        '-o', '--output',
        default='template.svg',
        help='Set the output filename to OUTPUT.' \
            ' Default output filename is \'template.svg\'.' \
            ' Use \'-\' to output the matrix to stdout.',
    )
    parser.add_argument(
        'matrix',
        help='Filename to read the matrix from.' \
            ' The matrix must be encoded as a JSON array of arrays.' \
            ' Use \'-\' to read the matrix from stdin.',
    )
    return parser


def _setup_logging():
    """
    Configure the logging.

    The default logging behavior can be tweaked through the environment
    variable `CATE_LOG_CFG`.
    To modify the configuration of the logging, the environment variable
    `CATE_LOG_CFG` has to point to a JSON file that is a valid configuration
    dictionary.  Do not modify the logging configuration unless you know what
    you are doing!

    See https://docs.python.org/3/library/logging.config.html for more details
    on the configuration of the logging module.
    """
    log_cfg_filename = _os.getenv('CATE_LOG_CFG')
    if log_cfg_filename is not None and _os.path.isfile(log_cfg_filename):
        with open(log_cfg_filename, mode='rt') as log_cfg_fd:
            log_cfg = _json.load(log_cfg_fd)
        _logging_config.dictConfig(log_cfg)
    else:
        _logging.basicConfig(
            # levelname is padded with spaces to the length of the longest levelname
            format='[{levelname:^8}] {message}',
            style='{',
            level=_logging.INFO,
        )


def cli():
    """Entry point for the Command Line Interface (CLI)."""
    _setup_logging()
    parser = _create_parser()
    options = vars(parser.parse_args())  # read argparse.Namespace as a dict
    logger.debug(f'parsed arguments: {options}')
    infile = options.pop('matrix')  # extract positional argument from options
    _main.run(infile, **options)
