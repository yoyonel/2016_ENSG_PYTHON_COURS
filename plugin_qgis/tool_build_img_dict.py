#
# urls:
# - http://stackoverflow.com/questions/2701173/most-efficient-way-for-a-lookup-search-in-a-huge-list-python
# - https://docs.python.org/2/library/bisect.html
from bisect import bisect_left
from tool_search_images import list_img_dirs
from qgis.core import QgsPoint, QGis


def bi_contains(lst, item):
    """ efficient `item in lst` for sorted lists """
    # if item is larger than the last its not in the list, but the bisect would
    # find `len(lst)` as the index to insert, so check that first. Else, if the
    # item is in the list then it has to be at index bisect_left(lst, item)
    return (item <= lst[-1]) and (lst[bisect_left(lst, item)] == item)


def bi_contains_2(lst, item):
    """ efficient `~ lst.index(item)` for sorted lists """
    # if item is larger than the last its not in the list, but the bisect would
    # find `len(lst)` as the index to insert, so check that first. Else, if the
    # item is in the list then it has to be at index bisect_left(lst, item)
    found = False
    id_item = 0
    if item <= lst[-1]:
        id_item = bisect_left(lst, item)
        found = (lst[id_item] == item)
    return found, id_item


def build_img_dict(id_img, img_dir, tup_qgis_layer_featureid, position):
    """

    :param id_img:
    :param img_dir:
    :param tup_qgis_layer_featureid:
    :param position:
    :return:
    """
    return {
        id_img: {
            'path': img_dir,
            'plugin_qgis': tup_qgis_layer_featureid,
            'position': position
        }
    }


def build_imgs_dict_0(layers_compatibles, list_img_basename):
    """

    :param layers_compatibles:
    :param list_img_basename:
    :return:
    """
    dict_imgs = {}
    # Pour chaque layer compatible
    for layer in layers_compatibles:
        # Pour chaque feature
        for feature in layer.getFeatures():
            # fetch attributes
            attrs = feature.attributes()
            # On recupere l'id de l'image (basename)
            id_img = attrs[0]

            # On recherche cette id dans notre base d'images
            # (trouvees/disponibles)v
            if id_img in list_img_basename:

                # On recupere l'indice de correspondance de l'image dans notre
                # base
                id_img_in_list = list_img_basename.index(id_img)

                # On peut extraire son path
                dir_path_img = list_img_dirs[id_img_in_list]

                # On recupere l'id de la feature [QGIS side]
                qgis_feature_id = feature.id()

                # On recupere des informations geometriques (position du centre d'acquisition de l'image)
                # retrieve every feature with its geometry and attributes
                # fetch geometry
                geom = feature.geometry()
                # show some information about the feature
                position = geom.asPoint() if geom.type() == QGis.Point else QgsPoint(0, 0)

                # On met a jour le dictionnaire des images
                dict_imgs.update(
                    build_img_dict(id_img, dir_path_img, (layer, qgis_feature_id), position)
                )
    return dict_imgs


def build_imgs_dict_1(layers_compatibles, list_img_basename):
    """

    :param layers_compatibles:
    :param list_img_basename:
    :return:
    """
    dict_imgs = {}
    # Pour chaque layer compatible
    for layer in layers_compatibles:
        # Pour chaque feature
        for feature in layer.getFeatures():
            # fetch attributes
            attrs = feature.attributes()
            # On recupere l'id de l'image (basename)
            id_img = attrs[0]

            # On recherche cette id dans notre base d'images
            # (trouvees/disponibles)v
            if bi_contains(list_img_basename, id_img):
                # On recupere l'indice de correspondance de l'image dans notre
                # base
                id_img_in_list = bisect_left(list_img_basename, id_img)

                # On peut extraire son path
                dir_path_img = list_img_dirs[id_img_in_list]

                # On recupere l'id de la feature [QGIS side]
                qgis_feature_id = feature.id()

                # On recupere des informations geometriques (position du centre d'acquisition de l'image)
                # retrieve every feature with its geometry and attributes
                # fetch geometry
                geom = feature.geometry()
                # show some information about the feature
                position = geom.asPoint() if geom.type() == QGis.Point else QgsPoint(0, 0)

                # On met a jour le dictionnaire des images
                dict_imgs.update(
                    build_img_dict(id_img, dir_path_img, (layer, qgis_feature_id), position)
                )
    return dict_imgs


def build_imgs_dict_2(layers_compatibles, list_img_basename):
    """

    :param layers_compatibles:
    :param list_img_basename:
    :return:
    """
    dict_imgs = {}
    # Pour chaque layer compatible
    for layer in layers_compatibles:
        # Pour chaque feature
        for feature in layer.getFeatures():
            # fetch attributes
            attrs = feature.attributes()
            # On recupere l'id de l'image (basename)
            id_img = attrs[0]

            # On recherche cette id dans notre base d'images
            # (trouvees/disponibles)v
            bc_found_img, bc_id_img = bi_contains_2(list_img_basename, id_img)
            if bc_found_img:
                # On recupere l'indice de correspondance de l'image dans notre
                # base
                id_img_in_list = bc_id_img

                # On peut extraire son path
                dir_path_img = list_img_dirs[id_img_in_list]

                # On recupere l'id de la feature [QGIS side]
                qgis_feature_id = feature.id()

                # On recupere des informations geometriques (position du centre d'acquisition de l'image)
                # retrieve every feature with its geometry and attributes
                # fetch geometry
                geom = feature.geometry()
                # show some information about the feature
                position = geom.asPoint() if geom.type() == QGis.Point else QgsPoint(0, 0)

                # On met a jour le dictionnaire des images
                dict_imgs.update(
                    build_img_dict(id_img, dir_path_img, (layer, qgis_feature_id), position)
                )
    return dict_imgs

build_imgs_dict = build_imgs_dict_2
