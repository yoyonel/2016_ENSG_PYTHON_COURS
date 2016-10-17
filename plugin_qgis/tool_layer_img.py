from tool_log import logger
import random
import os
import sys
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QPixmap


def get_qgis_from_dict_imgs(dict_imgs, id_img):
    """

    :param dict_imgs:
    :param id_img:
    :return:
    """
    return dict_imgs[id_img]['plugin_qgis']


def get_layer_from_dict_imgs(dict_imgs, id_img):
    """

    :param dict_imgs:
    :param id_img:
    :return:
    """
    return dict_imgs[id_img]['plugin_qgis'][0]


def get_featureid_from_dict_imgs(dict_imgs, id_img):
    """

    :param dict_imgs:
    :param id_img:
    :return:
    """
    return dict_imgs[id_img]['plugin_qgis'][1]


# def get_img_filename(dict_imgs, id_img):
def get_img_filename(dict_img, id_img):
    """

    :param dict_imgs:
    :param id_img:
    :return:
    """
    # return os.path.join(dict_imgs[id_img]['path'], id_img)
    return os.path.join(dict_img['path'], id_img)


def get_random_id(l):
    """
    Renvoie un id aleatoire de la liste passee en parametre.

    :param l:
    :return:
    """
    return random.randint(0, len(l))


def get_random_key(dict_imgs):
    """
    Renvoie une clee aleatoire du dictionnaire 'd'

    :param dict_imgs:
    :return:
    """
    list_keys = dict_imgs.keys()
    return list_keys[get_random_id(list_keys)]


def load_pixmap_to_label(label, img_filename):
    """

    :param label:
    :param img_filename:
    :return:
    """
    pixmap_img = QPixmap(img_filename)
    label.setPixmap(pixmap_img)


def init_label_with_img(label, dict_img, id_img):
    """

    :param label:
    :param dict_img:
    :param id_img:
    :return:
    """
    img_filename = get_img_filename(dict_img, id_img)

    # if os.path.exists(img_filename):
    try:
        load_pixmap_to_label(label, img_filename)
    except Exception as e:
        # url:
        # http://stackoverflow.com/questions/1278705/python-when-i-catch-an-exception-how-do-i-get-the-type-file-and-line-number
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error("{}, {}, {}".format(exc_type, fname, exc_tb.tb_lineno))


def create_label_with_random_img(dict_imgs):
    """

    :param dict_imgs:
    :return:
    """
    label = QLabel()
    id_img = get_random_key(dict_imgs)
    # -----
    # Notes
    # -----
    # Il faut se rappeler que les informations fournies par QGIS ne sont pas statiques
    # au cours de l'execution du plugin (les liens peuvent etre effaces/supprimes, changes, etc ...)
    # Il faudrait retester la validite des informations a chaque
    # utilisation (ou ne plus stocker et effectuer des requetes a la volee)
    #
    init_label_with_img(label, dict_imgs[id_img], id_img)
    return label, id_img


def set_random_img_in_label(dict_imgs):
    """

    :param dict_imgs:
    :return:
    """
    label, id_img = create_label_with_random_img(dict_imgs)
    logger.info("label: {}".format(label))
    return label, id_img
