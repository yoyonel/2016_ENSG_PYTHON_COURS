#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tool_log import logger
import sys
from PyQt4.QtGui import QColor
import os


def select_feature_on_layer(
        _tup_layer_featureid_selected,
        _map_canvas,
        _selection_qcolor=QColor("blue")):
    """

    :param _layer_selected:
    :param _featureid_selected:
    :param _map_canvas:
    :param _selection_qcolor:
    :return:
    """
    # test d'interaction avec QGIS (mapcanvas, layer, selection)
    _map_canvas.setSelectionColor(_selection_qcolor)
    # urls:
    # - http://gis.stackexchange.com/questions/131158/how-to-select-features-using-an-expression-with-pyqgis
    # - http://gis.stackexchange.com/questions/136861/how-to-get-a-layer-by-name-in-pyqgis
    try:
        _layer_selected, _featureid_selected = _tup_layer_featureid_selected
        _layer_selected.setSelectedFeatures([_featureid_selected])
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error("{}, {}, {}".format(exc_type, fname, exc_tb.tb_lineno))
    else:
        logger.info("Feature selected: {}".format(_featureid_selected))