#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tool_log import logger
import os
import glob
#
import platform

# local settings
# url:
# http://stackoverflow.com/questions/110362/how-can-i-find-the-current-os-in-python
# ps: c'est surement pas assez discriminant de n'utiliser que l'information de platform
# peut etre effecuter une fusion avec l'hostname, ip, ou autrechose
# ps2: a noter qu'on passe maintenant avec un submodule pour les données,
# du coup on a peut etre un acces relatif au path des ressources/datas.
# ps3: faudrait séparer les parties du path (ROOT + relatif PATH)
dict_settings = {
    'Linux-3.13.0-24-generic-x86_64-with-LinuxMint-17.3-rosa': {
        'search_dir_images': u'/media/atty/WIN7_INST_DATAS/__DATAS__/__DEV__/OSGEO4W/2016-07-18_LI3DS_Nexus5_Synch_BatU/img',
        'search_pattern_images': u'*.jpg'
    },
    'Windows-7-6.1.7601-SP1': {
        'search_dir_images': u'D:\\__DATAS__\\__DEV__\\OSGEO4W\\2016-07-18_LI3DS_Nexus5_Synch_BatU\\img',
        'search_pattern_images': u'*.jpg',
    },
    'Linux-3.19.0-32-generic-x86_64-with-LinuxMint-17.3-rosa': {
        'search_dir_images': u'/home/latty/link_dir/2016_ENSG_PYTHON_COURS/data-2016-07-18_LI3DS_Nexus5_Synch_BatU/img',
        'search_pattern_images': u'*.jpg',
    }
}
settings = dict_settings[platform.platform()]


def search_images(search_dir_images, search_pattern_images=u'*.jpg'):
    """

    :param search_dir_images:
    :param search_pattern_images:
    :return:
    """
    search_path_for_img = ""
    try:
        # search images files
        search_path_for_img = os.path.join(
            search_dir_images, search_pattern_images)
        [l_img_dirs, l_img_basename] = zip(
            *[os.path.split(filename_img)
              for filename_img in glob.glob(search_path_for_img)
              ]
        )
    except:
        logger.warning("No images found in: {}".format(search_path_for_img))
    else:
        logger.info("{} images found in: {}".format(len(l_img_dirs), search_path_for_img))
        return l_img_dirs, l_img_basename


def build_list_imgs_dir_basename(
        search_dir_images=settings['search_dir_images'],
        search_pattern_images=settings['search_pattern_images']
):
    """

    :param search_dir_images:
    :param search_pattern_images:
    :return:
    """
    list_img_dirs, list_img_basename = search_images(
        search_dir_images=search_dir_images,
        search_pattern_images=search_pattern_images,
    )

    # il faut etre sure que les listes sont triees si on souhaite
    # utiliser les outils de recherche dichotomique (bisect_left, bi_contain, etc ...)
    list_img_dirs = list(list_img_dirs)
    list_img_dirs.sort()
    list_img_basename = list(list_img_basename)
    list_img_basename.sort()

    return list_img_dirs, list_img_basename
