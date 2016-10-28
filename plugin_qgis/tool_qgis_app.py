#!/usr/bin/env python
# -*- coding: utf-8 -*-

from qgis.core import QgsApplication
#
from qgis.core import QgsMapLayerRegistry, QgsVectorLayer
from qgis.gui import QgsMapCanvas, QgsMapCanvasLayer
from PyQt4.QtGui import QWidget, QColor
from PyQt4.QtCore import QTimer
#
from tool_log import logger
#
import sys
#
from qgis_layer_filters import get_compatibles_layers
from tool_build_img_dict import build_imgs_dict
from tool_layer_img import set_random_img_in_label
from qgis_layer_feature import select_feature_on_layer
from qgis_layer_renderer import configure_layer_renderer, get_qstring_random_color
from tool_search_images import build_list_imgs_dir_basename
import os
#
from tool_layer_img import init_label_with_img, get_random_key
#
from collections import defaultdict

# urls:
# - saghul/pyqt_opencv.py: https://gist.github.com/saghul/1055161


class QgisApp(QWidget):
    def __init__(self):
        """

        """
        #
        # create a new application instance
        self.qgis_app = QgsApplication(sys.argv, True)
        QWidget.__init__(self)

        # Init QGIS for QGIS Application
        self.qgis_app.initQgis()

        # MapCanvas
        self.qgis_canvas = QgsMapCanvas()
        # set color and antialiasing
        self._init_mapcanvas()
        #
        # Timer pour l'animation
        self._timer = QTimer(self)
        # #
        # self._timer.timeout.connect(self.changeId_random)
        self._timer.timeout.connect(self.changeId_inc)
        #
        self.vector_layer = None
        self.label = None
        self.id_img = None
        self.dict_imgs = {}
        self.keys_dict_imgs = []
        # TODO: write a doc/commentaries about this defaultdict (idea, usage, ...)
        self.map_id_color = defaultdict(lambda: get_qstring_random_color())

    def startAnimation(self, period=200):
        """

        :param period:
        :return:
        """
        self._timer.start(period)

    def changeId(self, _id):
        """

        :param _id:
        :return:
        """
        self.id_img = _id

        init_label_with_img(self.label, self.dict_imgs[self.id_img], self.id_img)
        select_feature_on_layer(self.dict_imgs[self.id_img]['plugin_qgis'], self.qgis_canvas)
        configure_layer_renderer(self.dict_imgs, self.id_img, 'id', self.map_id_color)

        logger.debug("Change id: {}".format(self.id_img))

    def changeId_random(self):
        """

        :return:
        """
        self.changeId(get_random_key(self.dict_imgs))

    def changeId_inc(self):
        """

        :return:
        """
        l_keys = self.keys_dict_imgs
        next_id_in_list = (l_keys.index(self.id_img) + 1) % len(l_keys)
        self.changeId(l_keys[next_id_in_list])

    def _init_mapcanvas(self, color=QColor("white"), useAA=True):
        """

        :param color:
        :param useAA:
        :return:
        """
        # create a map canvas widget
        self.qgis_canvas.setCanvasColor(color)
        self.qgis_canvas.enableAntiAliasing(useAA)

    def load_vectorlayer(self, _shp_fullpath=""):
        """

        :param _shp_fullpath:
        :return:
        """
        logger.debug("shp_fullpath: %s" % _shp_fullpath)
        self.vector_layer = QgsVectorLayer(_shp_fullpath, 'MasterMap', 'ogr')

    def add_vectorlayer_to_canvas(self, _vl):
        """

        :param _vl:
        :return:
        """
        # add the layer to the canvnas and zoom to it
        QgsMapLayerRegistry.instance().addMapLayer(_vl)
        self.qgis_canvas.setLayerSet([QgsMapCanvasLayer(_vl)])
        self.qgis_canvas.setExtent(_vl.extent())

    def init_qt_canvas(self):
        """

        :return:
        """
        qt_canvas = self.qgis_canvas
        qt_canvas.setWindowTitle('Render MapCanvas')
        qt_canvas.resize(800, 600)

    def show(self, show_qgis_canvas=True, show_label=True):
        """

        :return:
        """
        if show_qgis_canvas:
            self.qgis_canvas.show()
        if show_label:
            self.label.show()

    def run(self, args):
        """

        :param args:
        :return:
        """
        self.load_vectorlayer(os.path.join(args.shp_path, args.shp_basename))
        vector_layer = self.vector_layer

        if vector_layer.isValid():
            self.add_vectorlayer_to_canvas(vector_layer)
            #
            layers_compatibles = get_compatibles_layers([vector_layer])
            #
            list_img_dirs, list_img_basename = build_list_imgs_dir_basename(
                search_dir_images=args.imgs_path,
                search_pattern_images=args.imgs_pattern_ext
            )
            #
            dict_imgs = self.dict_imgs = build_imgs_dict(layers_compatibles, list_img_dirs, list_img_basename)
            self.keys_dict_imgs = dict_imgs.keys()
            self.keys_dict_imgs.sort()
            logger.debug("dict_imgs: {}".format(len(dict_imgs)))
            #
            if dict_imgs:
                self.label, self.id_img = set_random_img_in_label(dict_imgs)
                logger.debug("id_img: {}".format(self.id_img))
                #
                select_feature_on_layer(dict_imgs[self.id_img]['plugin_qgis'], self.qgis_canvas)
                #
                configure_layer_renderer(dict_imgs, self.id_img, 'id', self.map_id_color)
                #
                self.show()
                #
                self.startAnimation(100)
                #
                sys.exit(self.qgis_app.exec_())
