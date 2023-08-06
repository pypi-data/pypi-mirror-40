#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LombardPress print.

Usage:
  lbp_print (tex|pdf) [options] --local <file>...
  lbp_print (tex|pdf) [options] --scta <id>...
  lbp_print recipe <recipe> [options]

Pull LBP-compliant files from SCTA repositories or use local, convert them into
tex or pdf.

Arguments:
  <file>                   File location of one or more objects to be processed.
  <id>                     SCTA id of one or more objects to be processed.

Multiple arguments are separated with whitespace.

Commands:
  tex                      Convert the xml to a tex-file.
  pdf                      Convert the xml to a tex-file and compile it into a
                           pdf.
  recipe <recipe>          Follow recipe in config file in <recipe>.

Options:
  --scta                   Flag. When present, the <id> should be an expression
                           id of the SCTA database.
  --local                  Flag. When present, process local file indicated
                           by <file> argument.
  --xslt <file>            Use a custom xslt file in place of the default
                           supplied templates.
  --output, -o <dir>       Put results in the specified directory. If nothing is
                           set, it will output to current working dir.
  --cache-dir <dir>        The directory where cached files should be stored.
  --xslt-parameters <str>  Command line parameters that will be
                           passed to the XSLT script. Unfortunately, this only
                           works with one parameter at the moment.
                           Example: --xslt-parameters "key=value"
  --config-file <file>     Location of a config file in json format.
                           [default: ~/.lbp_print.json]
  --no-cache               Skip the cache check.
  --no-samewords           Do not add sameword annotations to the output.
  -V, --verbosity <level>  Set verbosity. Possibilities: silent, info, debug
                           [default: info].
  -v, --version            Show version and exit.
  -h, --help               Show this help message and exit.
"""

import logging
import os
import json

from docopt import docopt

from lbp_print import config
from lbp_print.core import LocalTranscription, RemoteTranscription, Tex
from lbp_print.__about__ import __version__

def load_config(filename):
    """Load and read in configuration from local config file.

    :return Dictionary of the configuration."""
    try:
        with open(filename, mode='r') as f:
            conf = json.loads(f.read())
        return conf
    except json.decoder.JSONDecodeError as e:
        logging.error(f"The config file {f.name} is incorrectly formatted.\n"
                      f"JSON decoding gave the following error: {e}")
        raise
    except FileNotFoundError:
        logging.warning(f'The config file {filename} was not found. Default settings will be used.')
        return {}

def expand_in_dict(key, dict):
    """Expand os user name in dict key."""
    if key in dict:
        if isinstance(dict[key], list):
            return [os.path.abspath(os.path.expanduser(item)) for item in dict[key]]
        elif isinstance(dict[key], str):
            return os.path.abspath(os.path.expanduser(dict[key]))

def setup_arguments(cl_args):
    """Register command line and config file configuration and update values in `Config` object
    in the global variable `config`.
    """
    # Expand user dir for config file.
    cl_args['--config-file'] = os.path.expanduser(cl_args['--config-file'])

    # Read config file or recipe
    if cl_args['<recipe>']:
        ini_args = load_config(cl_args['<recipe>'])
        logging.debug(f'Recipe loaded with these values. {ini_args}')
    else:
        ini_args = load_config(cl_args['--config-file'])
        logging.debug(f'Config file loaded with these values. {ini_args}')

    # Merge configurations, giving command line arguments priority over config file arguments
    args = {**cl_args, **ini_args}

    # Set the output dir to current working dir, if it's not set yet
    if not '--output' in args:
        args['--output'] = os.getcwd()


    # Expand user commands in file arguments.
    for key in ['<file>', '<recipe>', '--output', '--xslt', '--config-file', '--cache-dir']:
        if key in args:
            args[key] = expand_in_dict(key, args)

    if args['--cache-dir']:
        config.cache_dir = args['--cache-dir']

    return args

def main():

    logging.basicConfig(format="%(levelname)s: %(message)s")

    args = setup_arguments(docopt(__doc__, version=__version__))

    # Setup logging according to configuration
    logging.getLogger().setLevel(args['--verbosity'].upper())
    logging.debug('Logging initialized at debug level.')

    # Initialize the object
    transcriptions = []
    if args['--scta']:
        for num, exp in enumerate(args['<id>'], 1):
            logging.info(f'Initializing {exp}. [{num}/{len(args["<id>"])}]')
            transcriptions.append(RemoteTranscription(exp, custom_xslt=args['--xslt']))
    elif args['--local']:
        for num, exp in enumerate(args['<file>'], 1):
            logging.info(f'Initializing {exp}. [{num}/{len(args["<file>"])}]')
            transcriptions.append(LocalTranscription(exp, custom_xslt=args['--xslt']))

    if args["pdf"]:
        output_format = 'pdf'
    elif args['tex']:
        output_format = 'tex'
    else:
        output_format = None

    for num, item in enumerate(transcriptions, 1):
        # Determine xslt script file (either provided or selected based on the xml transcription)
        logging.info('-------')
        logging.info(f'Processing {item.input}. [{num}/{len(transcriptions)}]')

        if args['--xslt']:
            item.xslt = item.select_xlst_script(args['--xslt'])

        if args['--no-cache']:
            caching = False
        else:
            caching = True

        if args['--no-samewords']:
            samewords = False
        else:
            samewords = True

        output_file = Tex(item,
                          output_format=output_format,
                          output_dir=args['--output'],
                          xslt_parameters=args['--xslt-parameters'],
                          caching=caching,
                          annotate_samewords=samewords).process()

        logging.info('Results returned sucessfully.\n '
                     'The output file is located at %s' % os.path.abspath(output_file))
