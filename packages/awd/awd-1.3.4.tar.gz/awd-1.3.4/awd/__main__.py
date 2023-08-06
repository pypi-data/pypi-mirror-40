#!/usr/bin/env python3

'''
main module;
'''

import argparse
import argparse_ext
import logging
import logging_ext

from awd.api import get_windows
from awd.api import layout_windows

##  program name;
prog = 'awd'

##  logger;
logger = logging_ext.getLogger(__name__)
handler = logging.StreamHandler()
logger.addHandler(handler)

def parse_args():

    '''
    parse command line arguments;
    '''

    parser = argparse.ArgumentParser(
        prog=prog,
        description='a window director;',
        formatter_class=argparse_ext.HelpFormatter,
        add_help=False,
    )

    parser.add_argument(
        '-h', '--help',
        action='help',
        help='display help message;',
    )
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='debug mode;',
    )
    parser.add_argument(
        '-e', '--exclude',
        action='append',
        default=[],
        metavar='pattern',
        help='excluded window name pattern;',
    )

    layouts = parser.add_argument_group('layouts')

    layouts.add_argument(
        '--cascade',
        action='store_true',
        help='cascade;',
    )
    layouts.add_argument(
        '--horizontal',
        action='store_true',
        help='tile horizontally;',
    )
    layouts.add_argument(
        '--vertical',
        action='store_true',
        help='tile vertically;',
    )
    layouts.add_argument(
        '--left',
        action='store_true',
        help='main window on the left;',
    )
    layouts.add_argument(
        '--right',
        action='store_true',
        help='main window on the right;',
    )
    layouts.add_argument(
        '--top',
        action='store_true',
        help='main window on the top;',
    )
    layouts.add_argument(
        '--bottom',
        action='store_true',
        help='main window on the bottom;',
    )
    layouts.add_argument(
        '--grid',
        action='store_true',
        help='grid;',
    )

    layout_opts = parser.add_argument_group('layout options')

    layout_opts.add_argument(
        '--rows',
        type=int,
        metavar='rows',
        help='number of grid rows;',
    )
    layout_opts.add_argument(
        '--cols',
        type=int,
        metavar='cols',
        help='number of grid cols;',
    )

    args = parser.parse_args()

    ##  check conflicting args;
    mutex = [
        k for k in [
            'cascade', 'horizontal', 'vertical', 'left', 'right', 'top',
            'bottom', 'grid',
        ] if getattr(args, k, None)
    ]
    if len(mutex) > 1:
        raise Exception('confict options: ' + ', '.join(mutex))

    ##  check missing args;
    if args.grid:
        if not args.rows:
            raise Exception('no number of grid rows;')
        if not args.cols:
            raise Exception('no number of grid cols;')

    return args

def main():

    '''
    main function;
    '''

    ##  parse args;
    args = parse_args()

    ##  enable debug mode;
    if args.debug:
        logger.setLevel(logging_ext.DEBUG)

    ##  get layout;
    if args.cascade:
        layout = 'cascade'
    elif args.horizontal:
        layout = 'horizontal'
    elif args.vertical:
        layout = 'vertical'
    elif args.left:
        layout = 'left'
    elif args.right:
        layout = 'right'
    elif args.top:
        layout = 'top'
    elif args.bottom:
        layout = 'bottom'
    elif args.grid:
        layout = 'grid'
    else:
        raise Exception('no window layout;')

    ##  get windows in current desktop;
    windows = get_windows(excludes=args.exclude)
    logger.d(windows)

    ##  layout windows;
    layout_windows(windows, layout, rows=args.rows, cols=args.cols)

if __name__ == '__main__':
    main()

