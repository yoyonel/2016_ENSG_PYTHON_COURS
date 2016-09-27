import os
import glob
from PyQt4.QtGui import QColor, QLabel, QPixmap
import random
import sys
from PyQt4.QtGui import *

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
    except Exception as err:
        print("Unexpected error:", err)
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
    try:
        id_img = get_random_key(dict_imgs)
        dict_img = dict_imgs[id_img]

        # -----
        # Notes
        # -----
        # Il faut se rappeler que les informations fournies par QGIS ne sont pas statiques au cours de l'execution du plugin (les liens peuvent etre effaces/supprimes, changes, etc ...)
        # Il faudrait retester la validite des informations a chaque
        # utilisation (ou ne plus stocker et effectuer des requetes a la volee)
        # layer_selected, featureid_selected = get_qgis_from_dict_imgs(id_img)
        tup_qgis = layer_selected, featureid_selected = dict_img['qgis']
        #
        label = init_label_with_img(id_img, label)
    except Exception as err:
        print("Unexpected error:", err)

    return label, tup_qgis


def show_random_img_in_label(dict_imgs):
    label, tup_qgis = create_label_with_random_img(dict_imgs)
    label.show()
    return tup_qgis


def select_feature_on_layer(layer_selected, featureid_selected, selection_qcolor=QColor("blue")):
    # test d'interaction avec QGIS (mapcanvas, layer, selection)
    iface.mapCanvas().setSelectionColor(selection_qcolor)
    # urls:
    # - http://gis.stackexchange.com/questions/131158/how-to-select-features-using-an-expression-with-pyqgis
    # - http://gis.stackexchange.com/questions/136861/how-to-get-a-layer-by-name-in-pyqgis
    layer_selected.setSelectedFeatures([featureid_selected])
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
                fullpath_to_img = os.path.join(dir_path_img, id_img)

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


def search_images(
    search_dir_images=u'D:\\__DATAS__\\__DEV__\\OSGEO4W\\2016-07-18_LI3DS_Nexus5_Synch_BatU\\img',
    search_pattern_images=u'*.jpg'
):
    """
    """
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


#############
### MAIN ####
#############
if __name__ == '__main__' or __name__ == '__console__':
    # local settings
    list_img_dirs, list_img_basename = search_images()

    # On recupere tous les layers QGIS disponibles
    layers = iface.mapCanvas().layers()
    # On les filtre avec nos criteres de recherche
    layers_compatibles = get_vector_layers_with_fields_v2a(
        layers, [u'id', u'position'])

    dict_imgs = build_imgs_dict(layers_compatibles)

    layer_selected, feature_selected = show_random_img_in_label(dict_imgs)
    select_feature_on_layer(layer_selected, feature_selected)

    print("Nb images synch with QGIS: %d" % (len(dict_imgs)))
else:
    print("__name__: %s" % __name__)
#############
