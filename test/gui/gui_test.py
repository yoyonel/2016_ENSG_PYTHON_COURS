# coding=utf-8
__author__ = 'YoYo'

import unittest

import os
import sys
#
osgeo4w_root = r'D:\__DATAS__\__DEV__\OSGEO4W\OSGeo4W64'

# os.environ['PATH'] = '{}/bin{}{}'.format(osgeo4w_root, os.pathsep, os.environ['PATH'])
# sys.path.insert(0, '{}/apps/qgis/python'.format(osgeo4w_root))
# sys.path.insert(1, '{}/apps/python27/lib/site-packages'.format(osgeo4w_root))
# sys.path.insert(2, 'C:/Users/Abdias/.qgis2/python/plugins')

# import PyQGIS
from qgis.core import QgsApplication, QgsVectorLayer, QgsMapLayerRegistry, QgsProviderRegistry
from qgis.gui import QgsMapCanvas, QgsMapCanvasLayer
#
# import Qt
from PyQt4 import QtCore, QtGui, QtTest
from PyQt4.QtCore import Qt

#
# import plugin_test

# disable debug messages
os.environ['QGIS_DEBUG'] = '-1'
#
shapefile_path = 'D:\__DATAS__\__DEV__\OSGEO4W\__COURS__\2016_ENSG_PYTHON_COURS\export\qgis_project.shp'


def setUpModule():
    """

    """
    # load qgis providers
    # QgsApplication.setPrefixPath('{}/apps/qgis'.format(osgeo4w_root), True)
    QgsApplication([], False).initQgis()

    if len(QgsProviderRegistry.instance().providerList()) == 0:
        raise RuntimeError('No data providers available.')


# dummy instance to replace qgis.utils.iface
class QgisInterfaceDummy(object):
    """

    """
    def __getattr__(self, name):
        """

        :param name:
        :return:
        """
        # return an function that accepts any arguments and does nothing
        def dummy(*args, **kwargs):
            return None
        return dummy


class Test_GUI(unittest.TestCase):
    def setUp(self):
        """

        """
        # create a new application instance
        self.app = app = QtGui.QApplication(sys.argv)

        # create a map canvas widget
        self.canvas = canvas = QgsMapCanvas()
        canvas.setCanvasColor(QtGui.QColor('white'))
        canvas.enableAntiAliasing(True)

        # load a shapefile
        layer = QgsVectorLayer(shapefile_path, 'MasterMap', 'ogr')

        # add the layer to the canvas and zoom to it
        QgsMapLayerRegistry.instance().addMapLayer(layer)
        canvas.setLayerSet([QgsMapCanvasLayer(layer)])
        canvas.setExtent(layer.extent())

    def test_gui(self):
        """

        """
        pass

