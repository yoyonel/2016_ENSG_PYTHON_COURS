#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tool_log import logger
from qgis.core import QgsSymbolV2, QgsSimpleMarkerSymbolLayerV2, QgsRendererCategoryV2, QgsCategorizedSymbolRendererV2
from random import randrange


def get_qstring_random_color():
    """

    :return:
    """
    return '%d, %d, %d' % (
        randrange(0, 256), randrange(0, 256), randrange(0, 256))


def configure_layer_renderer(dict_imgs, id_img, field, map_id_colors):
    """

    :param dict_imgs:
    :param id_img:
    :param field:
    :param map_id_colors:
    :return:
    """
    # urls:
    # - https://qgis.org/api/qgsmarkersymbollayerv2_8cpp_source.html
    # - http://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/vector.html#appearance-symbology-of-vector-layers
    # - http://gis.stackexchange.com/questions/175068/apply-symbol-to-each-feature-categorized-symbol
    # - http://gis.stackexchange.com/questions/59682/how-to-set-marker-line-symbol-for-qgsvectorlayer-by-using-python

    # Get the active layer (must be a vector layer)
    # layer = plugin_qgis.utils.iface.activeLayer()
    layer, featureid_selected = dict_imgs[id_img]['plugin_qgis']

    logger.info("configure_layer_renderer - id_img: {}".format(id_img))

    # get unique values
    fni = layer.fieldNameIndex(field)
    unique_values = layer.dataProvider().uniqueValues(fni)

    # define categories
    categories = []

    layer_styles = (
        # 'unselected'
        {
            'outline_color': '0, 0, 0',
            'size': '2',
            'name': 'circle'
        },
        # 'selected'
        {
            'outline_color': '255, 0, 0',
            'size': '15',
            'name': 'regular_star'
        }
    )
    #
    layer_style = {}

    for unique_value in unique_values:
        # initialize the default symbol for this geometry type
        symbol = QgsSymbolV2.defaultSymbol(layer.geometryType())

        # configure a symbol layer
        # layer_style = {}
        # layer_style['color'] = '%d, %d, %d' % (randrange(0,256), randrange(0,256), randrange(0,256))
        # layer_style['outline'] = '#000000'
        # symbol_layer = QgsSimpleFillSymbolLayerV2.create(layer_style)
        #
        # configure a symbol layer
        # simple_marker = QgsSimpleMarkerSymbolLayerV2()
        # simple_marker.setAngle(0)
        # simple_marker.setColor(
        #     QColor(randrange(0, 256), randrange(0, 256), randrange(0, 256)))
        # if id_img == unique_value:
        #     simple_marker.setShape(QgsSimpleMarkerSymbolLayerBase.Star)
        #     simple_marker.setSize(15)
        # else:
        #     simple_marker.setShape(QgsSimpleMarkerSymbolLayerBase.Circle)
        #     # simple_marker.setColor(QColor('red'))
        #     simple_marker.setSize(5)
        # simple_marker.setOutlineColor(QColor(0, 0, 0))

        # lecture/ecriture sur map_id_colors car defaultdict:
        # - si la clé existe (déjà) on utilise la valeur,
        # - si non, on génère une couleur aléatoire car la default value est sur une lambda expression utilisant
        #   get_qstring_random_color. Dans ce cas, le defaultdict 'map_id_colors' est mise à jour avec cet nouvelle
        #   pair (clée, value).
        unique_value_color = layer_style['color'] = map_id_colors[unique_value]
        layer_style.update(layer_styles[int(id_img == unique_value)])

        #
        simple_marker = QgsSimpleMarkerSymbolLayerV2.create(layer_style)
        #

        # replace default symbol layer with the configured one
        # if symbol_layer is not None:
        #     symbol.changeSymbolLayer(0, symbol_layer)
        if simple_marker is not None:
            symbol.changeSymbolLayer(0, simple_marker)

        # create renderer object
        category = QgsRendererCategoryV2(unique_value, symbol, str(unique_value))

        # entry for the list of category items
        categories.append(category)

    # create renderer object
    renderer = QgsCategorizedSymbolRendererV2(field, categories)

    # assign the created renderer to the layer
    if renderer is not None:
        layer.setRendererV2(renderer)
    layer.triggerRepaint()


def update_layer_renderer(dict_imgs, id_img, field, last_id_img, tup_categories_map):
    """
    Ne fonctionne pas ! :-/

    :param dict_imgs:
    :param id_img:
    :param field:
    :param last_id_img:
    :param tup_categories_map:
    :return:
    """
    layer, featureid_selected = dict_imgs[id_img]['plugin_qgis']
    _, last_featureid_selected = dict_imgs[last_id_img]['plugin_qgis']
    logger.info("id_img: {}".format(id_img))
    logger.info("last_id_img: {}".format(last_id_img))

    categories, map_idimg_idcat = tup_categories_map
    #
    logger.info("map_idimg_idcat[last_id_img]: %d" % map_idimg_idcat[last_id_img])
    logger.info("map_idimg_idcat[id_img]: %d" % map_idimg_idcat[id_img])
    # last_category = categories[map_idimg_idcat[last_id_img]]
    # category = categories[map_idimg_idcat[id_img]]
    # category.swap(last_category)
    # categories[map_idimg_idcat[id_img]] = category
    categories[map_idimg_idcat[last_id_img]] = categories[map_idimg_idcat[id_img]]

    # create renderer object
    renderer = QgsCategorizedSymbolRendererV2(field, categories)

    # assign the created renderer to the layer
    if renderer is not None:
        layer.setRendererV2(renderer)
    layer.triggerRepaint()

    return categories
