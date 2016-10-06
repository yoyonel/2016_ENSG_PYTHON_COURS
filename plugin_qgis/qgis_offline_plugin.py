#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from qgis.core import QgsApplication
import sys
#
from tool_log import logger, init_logger
from tool_qgis_app import QgisApp
from qgis_layer_filters import get_compatibles_layers
from tool_build_img_dict import build_imgs_dict
from tool_layer_img import show_random_img_in_label
from qgis_layer_feature import select_feature_on_layer
from qgis_layer_renderer import configure_layer_renderer
from tool_argparse import parse_arguments, print_args

import os


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
    QgsApplication([], False).initQgis()

    #
    app = QgisApp()

    app.init_qt_canvas()

    shp_fullpath = os.path.join(args.shp_path, args.shp_basename)
    logger.debug("shp_fullpath: %s" % shp_fullpath)
    vector_layer = app.load_vectorlayer(shp_fullpath)

    if vector_layer.isValid():
        app.add_vectorlayer_to_canvas(vector_layer)
        #
        layers_compatibles = get_compatibles_layers([vector_layer])
        #
        list_img_dirs, list_img_basename = build_list_imgs_dir_basename(
            search_dir_images=args.imgs_path,
            search_pattern_images=args.imgs_pattern_ext
        )
        #
        dict_imgs = build_imgs_dict(layers_compatibles, list_img_dirs, list_img_basename)
        logger.debug("dict_imgs: {}".format(len(dict_imgs)))
        #
        if dict_imgs:
            label, id_img = show_random_img_in_label(dict_imgs)
            logger.debug("id_img: {}".format(id_img))
            #
            select_feature_on_layer(dict_imgs[id_img]['plugin_qgis'], app.qgis_canvas)
            #
            configure_layer_renderer(dict_imgs, id_img, 'id')
            #
            app.show()
            label.show()
            #
            sys.exit(app.qt_app.exec_())

if __name__ == '__main__':
    main(sys.argv)
