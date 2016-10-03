#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from qgis.core import QgsApplication
import sys
#
from tool_log import logger, init_logger
from tool_qgis_app import QgisApp
from tool_search_images import list_img_basename
from qgis_layer_filters import get_compatibles_layers
from tool_build_img_dict import build_imgs_dict
from tool_layer_img import show_random_img_in_label


def main():
    QgsApplication([], False).initQgis()

    # init logging/logger
    init_logger(logger)

    app = QgisApp()
    app.init_qt_canvas()
    vector_layer = app.load_vectorlayer("/home/latty/link_dir/2016_ENSG_PYTHON_COURS/export/OriExport_Ori-RTL-Init.shp")
    if vector_layer.isValid():
        app.add_vectorlayer_to_canvas(vector_layer)
        app.show()
        #
        layers_compatibles = get_compatibles_layers([vector_layer])
        #
        dict_imgs = build_imgs_dict(layers_compatibles, list_img_basename)
        logger.info("dict_imgs: {}".format(len(dict_imgs)))
        #
        label, id_img = show_random_img_in_label(dict_imgs)
        logger.info("id_img: {}".format(id_img))
        label.show()

    sys.exit(app.qt_app.exec_())


if __name__ == '__main__':
    main()
