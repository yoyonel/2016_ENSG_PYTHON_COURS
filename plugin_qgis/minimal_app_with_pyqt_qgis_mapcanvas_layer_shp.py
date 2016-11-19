# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 11:23:45 2016

@author: latty
"""

import sys
#
from qgis.core import QgsMapLayerRegistry, QgsVectorLayer, QgsApplication
from qgis.gui import QgsMapCanvas, QgsMapCanvasLayer
#
from PyQt4.QtGui import QWidget, QColor
# from PyQt4.QtGui import QApplication
# from PyQt4.QtCore import QTimer


class QgisApp(QWidget):
    def __init__(self):
        #
        self.qgs_app = QgsApplication([], True)
        self.qgs_app.initQgis()
        QWidget.__init__(self)
        #
        self.qgis_canvas = QgsMapCanvas()
        self.qgis_canvas.setCanvasColor(QColor('white'))
        self.qgis_canvas.enableAntiAliasing(True)
        
    def run(self):
        #
        _shp_fullpath = "/home/latty/link_dir/2016_ENSG_PYTHON_COURS/export/Nexus5/OriExport_Ori-RTL-Init.shp"
        vector_layer = QgsVectorLayer(_shp_fullpath, 'MasterMap', 'ogr')
        QgsMapLayerRegistry.instance().addMapLayer(vector_layer)
        self.qgis_canvas.setLayerSet([QgsMapCanvasLayer(vector_layer)])
        self.qgis_canvas.setExtent(vector_layer.extent())
        #
        self.qgis_canvas.show()
        sys.exit(self.qgs_app.exec_())
    

qgis_app = QgisApp()
qgis_app.run()