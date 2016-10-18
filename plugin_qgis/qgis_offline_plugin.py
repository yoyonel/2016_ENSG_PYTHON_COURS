#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import sys
#
from tool_log import logger, init_logger
from tool_qgis_app import QgisApp
from tool_argparse import parse_arguments, print_args


def main(argv):
    """

    :param argv:
    :return:
    """
    # init logging/logger
    init_logger(logger)
    # Parsing des arguments transmis au script
    args = parse_arguments(argv)
    print_args(args)
    #
    app = QgisApp()
    app.init_qt_canvas()
    app.run(args)

if __name__ == '__main__':
    main(sys.argv)
