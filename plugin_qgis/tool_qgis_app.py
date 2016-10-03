#!/usr/bin/env python
# -*- coding: utf-8 -*-

from qgis.core import QgsMapLayerRegistry, QgsVectorLayer
from qgis.gui import QgsMapCanvas, QgsMapCanvasLayer
from PyQt4 import QtGui
#
import sys


class QgisApp(object):
    def __init__(self):
        """

        """
        # create a new application instance
        self.qt_app = QtGui.QApplication(sys.argv)
        # MapCanvas
        self.qgis_canvas = canvas = QgsMapCanvas()
        canvas.enableAntiAliasing(True)
        #
        self._init_mapcanvas()

    def _init_mapcanvas(self):
        """

        :return:
        """
        # create a map canvas widget
        self.qgis_canvas.setCanvasColor(QtGui.QColor('white'))
        self.qgis_canvas.enableAntiAliasing(True)

    def load_vectorlayer(self, _shp_filename=""):
        """

        :param _shp_filename:
        :return:
        """
        return QgsVectorLayer(_shp_filename, 'MasterMap', 'ogr')

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

    def show(self):
        """

        :return:
        """
        self.qgis_canvas.show()