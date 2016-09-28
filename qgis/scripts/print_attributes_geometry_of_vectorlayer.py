#!/usr/bin/env python
# -*- coding: utf-8 -*-
# url:
# http://stackoverflow.com/questions/6289474/working-with-utf-8-encoding-in-python-source

import os
import glob
from PyQt4.QtGui import QColor, QLabel, QPixmap
import random
import sys
from PyQt4.QtGui import *
# url: https://docs.python.org/2/library/random.html
from random import randrange

import platform

# url:
# http://stackoverflow.com/questions/110362/how-can-i-find-the-current-os-in-python
settings = {
    'Linux-3.13.0-24-generic-x86_64-with-LinuxMint-17.3-rosa': {
        'search_dir_images': u'/media/atty/WIN7_INST_DATAS/__DATAS__/__DEV__/OSGEO4W/2016-07-18_LI3DS_Nexus5_Synch_BatU/img',
        'search_pattern_images': u'*.jpg'
    },
    'Windows-7-6.1.7601-SP1': {
        'search_dir_images': u'D:\\__DATAS__\\__DEV__\\OSGEO4W\\2016-07-18_LI3DS_Nexus5_Synch_BatU\\img',
        'search_pattern_images': u'*.jpg',
    }
}
s = settings[platform.platform()]

# urls:
# - http://stackoverflow.com/questions/2701173/most-efficient-way-for-a-lookup-search-in-a-huge-list-python
# - https://docs.python.org/2/library/bisect.html
from bisect import bisect_left


def bi_contains(lst, item):
    """ efficient `item in lst` for sorted lists """
    # if item is larger than the last its not in the list, but the bisect would
    # find `len(lst)` as the index to insert, so check that first. Else, if the
    # item is in the list then it has to be at index bisect_left(lst, item)
    return (item <= lst[-1]) and (lst[bisect_left(lst, item)] == item)


def build_img_dict(id_img, img_dir, tup_qgis_layer_featureid, position):
    return {
        id_img: {
            'path': img_dir,
            'qgis': tup_qgis_layer_featureid,
            'position': position
        }
    }


def get_qgis_from_dict_imgs(id_img):
    return dict_imgs[id_img]['qgis']


def get_layer_from_dict_imgs(id_img):
    return dict_imgs[id_img]['qgis'][0]


def get_featureid_from_dict_imgs(id_img):
    return dict_imgs[id_img]['qgis'][1]


def get_img_filename(id_img):
    return os.path.join(dict_imgs[id_img]['path'], id_img)


def get_random_id(l):
    """
        Renvoie un id aleatoire de la liste passee en parametre.
    """
    return random.randint(0, len(l))


def load_pixmap_to_label(img_filename, label=QLabel()):
    pixmap_img = QPixmap(img_filename)
    label.setPixmap(pixmap_img)
    return label


def init_label_with_img(id_img, label=None):
    img_filename = get_img_filename(id_img)
    # if os.path.exists(img_filename):
    try:
        label = load_pixmap_to_label(img_filename)
    except Exception as e:
        # url:
        # http://stackoverflow.com/questions/1278705/python-when-i-catch-an-exception-how-do-i-get-the-type-file-and-line-number
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
    #
    return label


def get_vector_layers_with_fields_v0(layers, list_fields):
    list_layers_found = []
    for layer in layers:
        # url:
        # http://gis.stackexchange.com/questions/76364/how-to-get-field-names-in-pyqgis-2-0
        fields_names = map(QgsField.name, layer.pendingFields())
        if all([field in fields_names for field in list_fields]):
            list_layers_found.append(layer)
    return list_layers_found


def get_vector_layers_with_fields_v1a(layers, list_fields):
    list_layers_found = []
    for layer in layers:
        fields_names = map(QgsField.name, layer.pendingFields())
        list_layers_found.append(
            (layer, all([field in fields_names for field in list_fields])))
    #

    def _func_tup(_tup):
        return tup[1]
    return filter(_func_tup, list_layers_found)


def get_vector_layers_with_fields_v1b(layers, list_fields):
    list_layers_found = []
    for layer in layers:
        fields_names = map(QgsField.name, layer.pendingFields())
        list_layers_found.append(
            (layer, all([field in fields_names for field in list_fields])))
    return filter(lambda tup: tup[1], list_layers_found)


def get_vector_layers_with_fields_v2a(layers, list_fields):
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


def get_random_key(d):
    """
        Renvoie une clee aleatoire du dictionnaire 'd'
    """
    list_keys = dict_imgs.keys()
    return list_keys[get_random_id(list_keys)]


def create_label_with_random_img(dict_imgs, label=QLabel()):
    # tup_qgis = (None, None)
    label = None
    try:
        id_img = get_random_key(dict_imgs)
        dict_img = dict_imgs[id_img]

        # -----
        # Notes
        # -----
        # Il faut se rappeler que les informations fournies par QGIS ne sont pas statiques
        # au cours de l'execution du plugin (les liens peuvent etre effaces/supprimes, changes, etc ...)
        # Il faudrait retester la validite des informations a chaque
        # utilisation (ou ne plus stocker et effectuer des requetes a la volee)
        # layer_selected, featureid_selected = get_qgis_from_dict_imgs(id_img)
        # tup_qgis = layer_selected, featureid_selected = dict_img['qgis']
        #
        label = init_label_with_img(id_img, label)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

    # return label, tup_qgis, id_img
    return label, id_img


def show_random_img_in_label(dict_imgs):
    # label, tup_qgis = create_label_with_random_img(dict_imgs)
    # label.show()
    # return tup_qgis
    label, id_img = create_label_with_random_img(dict_imgs)
    label.show()
    return id_img


def select_feature_on_layer(
        layer_selected, featureid_selected,
        selection_qcolor=QColor("blue")):
    """
    """
    # test d'interaction avec QGIS (mapcanvas, layer, selection)
    iface.mapCanvas().setSelectionColor(selection_qcolor)
    # urls:
    # - http://gis.stackexchange.com/questions/131158/how-to-select-features-using-an-expression-with-pyqgis
    # - http://gis.stackexchange.com/questions/136861/how-to-get-a-layer-by-name-in-pyqgis
    try:
        layer_selected.setSelectedFeatures([featureid_selected])
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
    else:
        print("Feature selected: %d" % (featureid_selected))


def build_imgs_dict(layers_compatibles):
    dict_imgs = {}
    # Pour chaque layer compatible
    for layer in layers_compatibles:
        # On recupere ces features
        iter = layer.getFeatures()
        # Pour chaque feature
        for feature in iter:
            # fetch attributes
            attrs = feature.attributes()
            # On recupere l'id de l'image (basename)
            id_img = attrs[0]
            # On recherche cette id dans notre base d'images
            # (trouvees/disponibles)
            if bi_contains(list_img_basename, id_img):
                # On recupere l'indice de correspondance de l'image dans notre
                # base
                id_img_in_list = bisect_left(list_img_basename, id_img)
                # On peut extraire son path
                dir_path_img = list_img_dirs[id_img_in_list]
                # fullpath_to_img = os.path.join(dir_path_img, id_img)

                # On recupere l'id de la feature [QGIS side]
                qgis_feature_id = feature.id()
                # print "Feature ID %d: " % qgis_feature_id

                # On recupere des informations geometriques (position du centre d'acquisition de l'image)
                # retrieve every feature with its geometry and attributes
                # fetch geometry
                geom = feature.geometry()
                # show some information about the feature
                position = geom.asPoint() if geom.type() == QGis.Point else QgsPoint(
                    0, 0)

                # On met a jour le dictionnaire des images
                dict_imgs.update(
                    build_img_dict(
                        id_img,
                        dir_path_img,
                        (layer, qgis_feature_id),
                        position
                    )
                )
    return dict_imgs


def search_images(search_dir_images, search_pattern_images=u'*.jpg'):
    list_img_dirs, list_img_basename = [], []
    try:
        # search images files
        search_path_for_img = os.path.join(
            search_dir_images, search_pattern_images)
        list_img_dirs, list_img_basename = zip(
            *[os.path.split(filename_img)
              for filename_img in glob.glob(search_path_for_img)
              ]
        )
    except:
        print("No images found in: %s" % search_path_for_img)
    else:
        print("%d images found in: %s" %
              (len(list_img_dirs), search_path_for_img))
    return list_img_dirs, list_img_basename


def get_qstring_random_color():
    return '%d, %d, %d' % (
        randrange(0, 256), randrange(0, 256), randrange(0, 256))


def configure_layer_renderer(dict_imgs, id_img, field):
    # urls:
    # - https://qgis.org/api/qgsmarkersymbollayerv2_8cpp_source.html
    # - http://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/vector.html#appearance-symbology-of-vector-layers
    # - http://gis.stackexchange.com/questions/175068/apply-symbol-to-each-feature-categorized-symbol
    # - http://gis.stackexchange.com/questions/59682/how-to-set-marker-line-symbol-for-qgsvectorlayer-by-using-python

    # Get the active layer (must be a vector layer)
    # layer = qgis.utils.iface.activeLayer()
    layer, featureid_selected = dict_imgs[id_img]['qgis']

    print("id_img: %s" % id_img)

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

        layer_style['color'] = get_qstring_random_color()
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
        category = QgsRendererCategoryV2(
            unique_value, symbol, str(unique_value))
        # entry for the list of category items
        categories.append(category)

    # create renderer object
    renderer = QgsCategorizedSymbolRendererV2(field, categories)

    # assign the created renderer to the layer
    if renderer is not None:
        layer.setRendererV2(renderer)
    layer.triggerRepaint()


#############
### MAIN ####
#############
if __name__ == '__main__' or __name__ == '__console__':
    # local settings
    list_img_dirs, list_img_basename = search_images(
        # search_dir_images="/media/atty/WIN7_INST_DATAS/__DATAS__/__DEV__/OSGEO4W/2016-07-18_LI3DS_Nexus5_Synch_BatU/img"
        search_dir_images=s['search_dir_images'],
        search_pattern_images=s['search_pattern_images'],
    )

    # On recupere tous les layers QGIS disponibles
    layers = iface.mapCanvas().layers()
    # 1er filtre: on ne s'interesse qu'aux VectorLayers
    # url:
    # http://gis.stackexchange.com/questions/26257/how-can-i-iterate-over-map-layers-in-qgis-python
    layers = filter(
        lambda layer: layer.type() == QgsMapLayer.VectorLayer, layers)
    # 2nd filtre: on ne s'intéresse qu'aux VectorLayers possedant au moins 2
    # champs: 'id' et 'position'
    layers_compatibles = get_vector_layers_with_fields_v2a(
        layers, [u'id', u'position'])
    # Layers (potentiellement) compatibles
    print("layers_compatibles: %s" % (layers_compatibles))
    #
    dict_imgs = build_imgs_dict(layers_compatibles)

    id_img = show_random_img_in_label(dict_imgs)
    layer_selected, feature_selected = dict_imgs[id_img]['qgis']
    select_feature_on_layer(layer_selected, feature_selected)

    print("Nb images synch with QGIS: %d" % (len(dict_imgs)))

    configure_layer_renderer(dict_imgs, id_img, 'id')
else:
    print("__name__: %s" % __name__)
#############
