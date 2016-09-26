import os
import glob
from PyQt4.QtGui import QColor, QLabel, QPixmap
import random, sys

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

def build_img_dict(id_img, img_dir, feature_id, position):
    return {id_img: {'path': img_dir, 'feature_id': feature_id, 'position': position}}

def get_feature_id(id_img):
    return dict_imgs[id_img]['feature_id']

def get_img_filename(id_img):
    return os.path.join(dict_imgs[id_img]['path'], id_img)

def get_random_id(l):
    return random.randint(0, len(l))

def load_pixmap_to_label(img_filename):
    label = QLabel()
    pixmap_img = QPixmap(img_filename)
    label.setPixmap(pixmap_img)
    return label

def init_label_with_img(id_img):
    from PyQt4.QtGui import *
    label = None
    img_filename = get_img_filename(id_img)
    # if os.path.exists(img_filename):
    try:
        label = load_pixmap_to_label(img_filename)
    except Exception as err:
        print("Unexpected error:", err)
    #
    return label

def get_vector_layers_with_fields_0(layers, list_fields):
    list_layers_found = []
    for layer in layers:
        fields_names = map(QgsField.name, layer.pendingFields())
        if all([field in fields_names for field in list_fields]):
            list_layers_found.append(layer)
    return list_layers_found

def get_vector_layers_with_fields_1a(layers, list_fields):
    list_layers_found = []
    for layer in layers:
        fields_names = map(QgsField.name, layer.pendingFields())
        list_layers_found.append((layer, all([field in fields_names for field in list_fields])))
    #
    def _func_tup(_tup):
        return tup[1]
    return filter(_func_tup, list_layers_found)

def get_vector_layers_with_fields_1b(layers, list_fields):
    list_layers_found = []
    for layer in layers:
        fields_names = map(QgsField.name, layer.pendingFields())
        list_layers_found.append((layer, all([field in fields_names for field in list_fields])))
    return filter(lambda tup: tup[1], list_layers_found)

def get_vector_layers_with_fields_2a(layers, list_fields):
    list_layers_with_matching_results = [ (layer, 
                                all([field in map(QgsField.name, layer.pendingFields()) for field in list_fields]))
                                for layer in layers 
                            ]
    return map(lambda tup: tup[0], filter(lambda tup: tup[1], list_layers_with_matching_results))

def get_vector_layers_with_fields_2b(layers, list_fields):
    return map(
                lambda tup: tup[0], 
                filter(
                        lambda tup: tup[1], 
                        [
                            (
                                layer, 
                                all([
                                        field in map(QgsField.name, layer.pendingFields())
                                        for field in list_fields
                                    ]
                                )
                            )
                            for layer in layers
                        ]
                    )
            )

# local settings
DIR_IMG = u'D:\\__DATAS__\\__DEV__\\OSGEO4W\\2016-07-18_LI3DS_Nexus5_Synch_BatU\\img'
PATTERN_IMG = u'*.jpg'

dict_imgs = {}

try:
    # search images files
    search_path_for_img = os.path.join(DIR_IMG, PATTERN_IMG)
    list_img_dirs, list_img_basename = zip(*[os.path.split(filename_img) for filename_img in glob.glob(search_path_for_img)])
except:
    print("No images found in: %s" % search_path_for_img)
else:
    print("%d images found in: %s" % (len(list_img_dirs), search_path_for_img))

    # layers = get_vector_layers_with_attributes(['id', 'position'])
    layers = iface.mapCanvas().layers()

    # for layer in layers:
    #     layerType = layer.type()
    #     if layerType == QgsMapLayer.VectorLayer:
    #         # url: http://gis.stackexchange.com/questions/76364/how-to-get-field-names-in-pyqgis-2-0
    #         field_names = [field.name() for field in layer.pendingFields() ]
    #         if u'id' in field_names and u'position' in field_names:
    layers_compatibles = get_vector_layers_with_fields_2a(layers, [u'id', u'position'])
    for layer in layers_compatibles:
        iter = layer.getFeatures()
        
        for feature in iter:
            # fetch attributes
            attrs = feature.attributes()
            id_img = attrs[0]

            if bi_contains(list_img_basename, id_img):
                #
                id_img_in_list = bisect_left(list_img_basename, id_img)
                dir_path_img = list_img_dirs[id_img_in_list]
                fullpath_to_img = os.path.join(dir_path_img, id_img)
                #
                #print("Fullpath to image: %s" % (fullpath_to_img))

                # retrieve every feature with its geometry and attributes
                # fetch geometry
                geom = feature.geometry()
                qgis_feature_id = feature.id()
                #print "Feature ID %d: " % qgis_feature_id

                # show some information about the feature
                if geom.type() == QGis.Point:
                    position = geom.asPoint()
                    # update dict images
                    dict_imgs.update(build_img_dict(id_img, dir_path_img, qgis_feature_id, position))

    try:
        id_img = list_img_basename[get_random_id(list_img_basename)]
        feature_id_selected = get_feature_id(id_img)
    except Exception as err:
        # print("Can't select feature, because not images was synch with QGIS! ")
        print("Unexpected error:", err)
    else:
        # test d'interaction avec QGIS (mapcanvas, layer, selection)
        iface.mapCanvas().setSelectionColor( QColor("blue") )
        # url: http://gis.stackexchange.com/questions/136861/how-to-get-a-layer-by-name-in-pyqgis
        layer = iface.activeLayer()
        # url: http://gis.stackexchange.com/questions/131158/how-to-select-features-using-an-expression-with-pyqgis
        layer.setSelectedFeatures( [feature_id_selected] )
        print("Feature selected: %d" % (feature_id_selected))
        #
        label = init_label_with_img(id_img)
        try:
            label.show()
        except Exception as err:
            print("Unexpected error:", err)   
finally:
    print("Nb images synch with QGIS: %d" % (len(dict_imgs)))