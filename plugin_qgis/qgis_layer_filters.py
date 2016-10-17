#!/usr/bin/env python
# -*- coding: utf-8 -*-

from qgis.core import QgsField
from qgis.core import QgsMapLayer
from tool_log import logger


def get_vector_layers_with_fields_v0(layers, list_fields):
    """

    :param layers:
    :param list_fields:
    :return:
    """
    list_layers_found = []
    for layer in layers:
        # url:
        # http://gis.stackexchange.com/questions/76364/how-to-get-field-names-in-pyqgis-2-0
        fields_names = map(QgsField.name, layer.pendingFields())
        if all([field in fields_names for field in list_fields]):
            list_layers_found.append(layer)
    return list_layers_found


def get_vector_layers_with_fields_v1a(layers, list_fields):
    """

    :param layers:
    :param list_fields:
    :return:
    """
    list_layers_found = []
    for layer in layers:
        fields_names = map(QgsField.name, layer.pendingFields())
        list_layers_found.append(
            (layer, all([field in fields_names for field in list_fields])))

    #
    def _func_tup(_tup):
        return _tup[1]

    return filter(_func_tup, list_layers_found)


def get_vector_layers_with_fields_v1b(layers, list_fields):
    """

    :param layers:
    :param list_fields:
    :return:
    """
    list_layers_found = []
    for layer in layers:
        fields_names = map(QgsField.name, layer.pendingFields())
        list_layers_found.append(
            (layer, all([field in fields_names for field in list_fields])))
    return filter(lambda tup: tup[1], list_layers_found)


def get_vector_layers_with_fields_v2a(layers, list_fields):
    """

    :param layers:
    :param list_fields:
    :return:
    """
    list_layers_with_matching_results = \
        [(layer, all([field in map(QgsField.name, layer.pendingFields())
                      for field in list_fields]))
         for layer in layers
         ]
    return map(
        lambda tup: tup[0],
        filter(lambda tup: tup[1], list_layers_with_matching_results)
    )


def get_vector_layers_with_fields_v2b(layers, list_fields):
    """

    :param layers:
    :param list_fields:
    :return:
    """
    return map(
        lambda tup: tup[0],
        filter(
            lambda tup: tup[1],
            [
                (
                    layer,
                    all([
                        field in map(
                            QgsField.name, layer.pendingFields())
                        for field in list_fields
                    ]
                    )
                )
                for layer in layers
            ]
        )
    )


def get_compatibles_layers(layers):
    """

    :param list_layers:
    :return:
    """
    # On recupere tous les layers QGIS disponibles
    # layers = iface.mapCanvas().layers()
    # 1er filtre: on ne s'interesse qu'aux VectorLayers
    # url:
    # http://gis.stackexchange.com/questions/26257/how-can-i-iterate-over-map-layers-in-qgis-python
    layers = filter(lambda layer: layer.type() == QgsMapLayer.VectorLayer, layers)
    # 2nd filtre: on ne s'intéresse qu'aux VectorLayers possedant au moins 2
    # champs: 'id' et 'position'
    layers_compatibles = get_vector_layers_with_fields_v2a(
        layers, [u'id', u'position'])
    # Layers (potentiellement) compatibles
    logger.info("layers_compatibles: {}".format(layers_compatibles))
    return layers_compatibles
