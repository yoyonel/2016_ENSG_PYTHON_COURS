#!/usr/bin/env python
# -*- coding: utf-8 -*-
import shapefile
import argparse
import sys
import numpy as np
from math import *

# for doctest
import numpy

# for doctest
# url: http://python-future.org/compatible_idioms.html
try:
    # from StringIO import StringIO
    import StringIO
except ImportError:
    from io import StringIO  # for handling unicode strings

try:
    # from transformations import euler_matrix
    import transformations
except ImportError:
    import sys
    import os

    PACKAGE_PARENT = '..'
    SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
    sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
    import transformations

import logging

from logging.handlers import RotatingFileHandler

# urls:
# - https://pypi.python.org/pypi/pyshp
# - http://pygis.blogspot.fr/2012/10/pyshp-attribute-types-and-point-files.html
# - http://gis.stackexchange.com/questions/85448/python-how-to-create-a-polygon-shapefile-from-a-list-of-x-y-coordinates


# TODO: Versionner le projet [URGENT]
#
# TODO: doc -> ecrire la doc. (reellement) pour les methodes/fonctions
# TODO: doc -> generer la doc par sphinx (ou doxygen)
# TODO: exceptions -> relever plus d'exceptions et les gerer
# TODO: exceptions -> creer des exceptions customs pour ce projet/script


# création de l'objet logger qui va nous servir à écrire dans les logs
logger = logging.getLogger()


def _parse_tabline_from_orifile(tab, x0=0, y0=0, z0=0):
    """

    :param tab:
    :param x0:
    :param y0:
    :param z0:
    :return:

    >>> _parse_tabline_from_orifile(['IMG_1468832894.185000000.jpg', '-75.622522', '-40.654833', '-172.350586', \
                                    '657739.197431', '6860690.284637', '53.534337'])
    {'altitude': 53.534337, 'id': 'IMG_1468832894.185000000.jpg', 'easting': 657739.197431, 'pitch': -172.350586, 'heading': -75.622522, 'roll': -40.654833, 'northing': 6860690.284637}
    """
    md = dict()

    # Identifiant
    md["id"] = tab[0]  # nom du fichier image
    # Orientation
    md["heading"] = float(tab[1])
    md["roll"] = float(tab[2])
    md["pitch"] = float(tab[3])
    # Position
    md["easting"] = float(tab[4]) + x0
    md["northing"] = float(tab[5]) + y0
    md["altitude"] = float(tab[6]) + z0

    return md


def _convert_line_to_tab_from_orifile(line):
    """

    :param line:
    :return:

    >>> _convert_line_to_tab_from_orifile('''IMG_1468832894.185000000.jpg -75.622522 -40.654833 -172.350586 \
                                            657739.197431 6860690.284637 53.534337''')
    ['IMG_1468832894.185000000.jpg', '-75.622522', '-40.654833', '-172.350586', '657739.197431', '6860690.284637', '53.534337']
    """
    return line.split()


def export_ori_fileobject_to_OmegaPhiKhapa(fo_oriexport, x0=0, y0=0, z0=0):
    """

    :param fo_oriexport:
    :param x0:
    :param y0:
    :param z0:
    :return:

    url: https://docs.python.org/2/library/stringio.html
    >>> output = StringIO.StringIO('''IMG_1468832894.185000000.jpg -75.622522 -40.654833 -172.350586 \
                                    657739.197431 6860690.284637 53.534337''')
    >>> export_ori_fileobject_to_OmegaPhiKhapa(output)
    [{'altitude': 53.534337, 'id': 'IMG_1468832894.185000000.jpg', 'easting': 657739.197431, 'pitch': -172.350586, 'heading': -75.622522, 'roll': -40.654833, 'northing': 6860690.284637}]
    >>> output.close()
    """
    try:
        return [_parse_tabline_from_orifile(_convert_line_to_tab_from_orifile(line), x0, y0, z0) for line in
                fo_oriexport]
    except Exception as err:
        logger.error("Exception: " % err)
        return []


def build_rotationmatrix_from_euler_(heading, roll, pitch, print_debug=False):
    """

    :param heading:
    :param roll:
    :param pitch:
    :param print_debug:
    
    :return:

    >>> mat_computed = build_rotationmatrix_from_euler_micmac(pitch=0, heading=0, roll=0)
    >>> mat_expected = numpy.array( \
            [[ 1., 0.,  0.,  0.],  \
            [ 0.,  1.,  0.,  0.],   \
            [-0.,  0.,  1.,  0.],   \
            [ 0.,  0.,  0.,  1.]])
    >>> numpy.allclose(mat_computed, mat_expected)
    True

    >>> mat_computed = build_rotationmatrix_from_euler_micmac(pitch=-172.350586, heading=-75.622522, roll=-40.654833)
    >>> mat_expected = numpy.array( \
            [[ 0.90781218, -0.18017385, -0.37870098,  0.        ],  \
            [-0.07492065, -0.95815745,  0.27626291,  0.        ],   \
            [-0.41263052, -0.22242231, -0.88332575,  0.        ],   \
            [ 0.        ,  0.        ,  0.        ,  1.        ]])
    >>> numpy.allclose(mat_computed, mat_expected)
    True
    """
    # urls:
    # - https://github.com/ros/geometry/blob/hydro-devel/transformations/src/transformations/transformations.py
    # - http://answers.ros.org/question/69754/quaternion-transformations-in-python/
    # - https://github.com/iTowns/itowns/blob/master/src/Ori.js
    # construction recuperee depuis itowns (Mathieu B.):
    #   // With quaternion  //set rotation.order to "YXZ", which is equivalent to "heading, pitch, and roll"
    #   var q = new THREE.Quaternion().setFromEuler(new THREE.Euler(-pitch,heading,-roll,'YXZ'),true);

    #
    # quaternion = transformations.quaternion_from_euler(-pitch, heading, -roll, axes='syxz')
    # matrix_rot = transformations.quaternion_matrix(quaternion)
    #
    # version concatenee de la construction de matrice de rotation
    # a partir d'informations d'orientation (euler)
    matrix_rot = transformations.euler_matrix(-pitch, heading, -roll, axes='syxz')

    if print_debug:
        logger.info("ROS - matrix_rot (from Quaternion)\n%s", matrix_rot)

    return matrix_rot


def extract_and_convert_heading_roll_pitch_from_dict_ori(dict_ori):
    """

    :param dict_ori:
    :return:

    >>> dict_ori = {'altitude': 53.534337, 'id': 'IMG_1468832894.185000000.jpg', 'easting': 657739.197431, \
                    'pitch': -172.350586, 'heading': -75.622522, 'roll': -40.654833, 'northing': 6860690.284637}
    >>> extract_and_convert_heading_roll_pitch_from_dict_ori(dict_ori)
    (-1.3198619975618473, -0.7095606926984439, -3.0080851934416435)
    """
    # extract
    heading, roll, pitch = dict_ori["heading"], dict_ori["roll"], dict_ori["pitch"]
    # convert (degree -> radian)
    heading = radians(heading)
    roll = radians(roll)
    pitch = radians(pitch)
    # yaw = heading
    return heading, roll, pitch


def extract_center_dict_ori(dict_ori):
    """

    :param dict_ori:
    :return:

    >>> dict_ori = {'id': 'IMG_1468832894.185000000.jpg', \
                    'altitude': 53.534337, 'easting': 657739.197431, 'northing': 6860690.284637, \
                    'pitch': -172.350586, 'heading': -75.622522, 'roll': -40.654833}
    >>> extract_center_dict_ori(dict_ori)
    [657739.197431, 6860690.284637, 53.534337, 1]
    """
    return [dict_ori["easting"], dict_ori["northing"], dict_ori["altitude"], 1]


def write_viewdir_shp_from_arr_ori(arr_oris, export_filename, viewdir_length_proj=1.0):
    """

    :param arr_oris:
    :param export_filename:
    :param viewdir_length_proj:
    :return:

    """
    # Create another polylineZ shapefile writer
    w = shapefile.Writer(shapeType=13)
    # Create a field called "Name"
    w.field("NAME")

    zaxis = [0, 0, 1, 0]

    # This time write each line separately
    # with its own dbf record
    for _, ori in enumerate(arr_oris):
        # on extrait le centre de la prise de vue
        center = extract_center_dict_ori(ori)
        # on extrait les informations d'orientation
        heading, roll, pitch = extract_and_convert_heading_roll_pitch_from_dict_ori(ori)
        # on calcule la matrix de rotation a partir de ces informations d'orientation
        matrix_rot = build_rotationmatrix_from_euler_micmac(heading, roll, pitch)
        # url: http://docs.scipy.org/doc/numpy/reference/generated/numpy.multiply.html
        view_vec = np.multiply(zaxis, viewdir_length_proj)
        # on calcule le vecteur de vue
        rot_view_vec = np.dot(matrix_rot, view_vec)
        # on construit la segment de vue
        segment_view = [center, np.add(rot_view_vec, center).tolist()]

        # print segment_view
        w.poly(parts=[segment_view])
        w.record("segment_view")
    # Save
    w.save(export_filename)
    logger.info("Export file: %s", export_filename)


def write_OPK_to_shp_file(
        arr_oris,
        export_filename,
        b_export_view_dir=False,
        viewdir_length_proj=1.0,
        field_0_name="id",
        field_1_name="position"
):
    """

    :param arr_oris:
    :param export_filename:
    :param b_export_view_dir:
    :param viewdir_length_proj:
    :param field_0_name: len(field_0_name) < 11
    :type field_1_name: len(field_1_name) < 11
    :return:
    """
    #
    w = shapefile.Writer(shapefile.POINT)
    #
    w.field(field_0_name)
    w.field(field_1_name, 'C', '40')
    #
    for _, ori in enumerate(arr_oris):
        w.point(ori["easting"], ori["northing"], ori["altitude"])
        w.record(ori["id"], 'Point')
    #
    logger.info("Export file: %s", export_filename)
    w.save(export_filename)

    if b_export_view_dir:
        write_viewdir_shp_from_arr_ori(arr_oris, export_filename + "_view_dir", viewdir_length_proj)


def parse_arguments(_):
    """

    :param _:
    :return:
    """
    parser = argparse.ArgumentParser()

    # nom du fichier entree a traiter
    parser.add_argument("ori", help="nom du fichier ORI (ExportOri) a utiliser")

    # option: pivot de translation
    # urls:
    # - https://docs.python.org/3/library/argparse.html#metavar
    # - https://docs.python.org/3/library/argparse.html#nargs
    parser.add_argument("-p", "--pivot", nargs=3, type=float,
                        default=[0, 0, 0],
                        help="position (x, y, z) du pivot (default: %(default)s)", metavar=('x', 'y', 'z'))

    # option: nom du fichier shapefile d'export
    # urls:
    # - http://stackoverflow.com/questions/25486400/how-do-i-set-an-argparse-arguments-default-value-to-a-positional-arguments-val
    # - http://stackoverflow.com/questions/2058925/how-can-i-break-up-this-long-line-in-python
    parser.add_argument("-s", "--shapefile", nargs='?', type=str,
                        help="""nom du fichier shapefile (sans extension) d'export \
                        (default: nom du fichier transmis par le parametre ori (sans extension))""")

    # option: prefix pour les exports
    #
    # parser.add_argument("--path_for_export", type=str,
    #                     default="/export/",
    #                     help="""path pour les exports \
    #                     (default: %(default)s)""")

    # option: noms des champs pour l'export shapefile

    # option: export des directions de vue
    # url: http://stackoverflow.com/questions/8259001/python-argparse-command-line-flags-without-arguments
    parser.add_argument("-v", "--viewdir", action='store_true',
                        help="flag pour exporter les directions de vue. (default: %(default)s)")

    # option: longueur des projections des directions de vue
    parser.add_argument("-vl", "--viewdir_length_proj", type=float, default=1.0,
                        help="longueur des projections des directions de vue. (default: %(default)s)")

    args = parser.parse_args()

    if args.shapefile is None:
        args.shapefile = args.ori[:-4]

    # # add the prefix for export filenames
    # args.shapefile = args.path_for_export + args.shapefile

    return args


def print_args(args):
    """

    :param args:
    :return:
    """
    print("- filename ExportOri: ", args.ori)
    # print("- prefix for export: ", args.prefix_for_export)
    print("- pivot: ", args.pivot)
    print("- shapefile: ", args.shapefile)
    print("- export view dir: ", args.viewdir)
    print("- export view dir - length proj: ", args.viewdir_length_proj)


def init_log():
    """

    :return:
    """
    # on met le niveau du logger à DEBUG, comme ça il écrit tout
    logger.setLevel(logging.INFO)

    # création d'un formateur qui va ajouter le temps, le niveau
    # de chaque message quand on écrira un message dans le log
    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
    # création d'un handler qui va rediriger une écriture du log vers
    # un fichier en mode 'append', avec 1 backup et une taille max de 1Mo
    file_handler = RotatingFileHandler('activity.log', 'a', 1000000, 1)
    # on lui met le niveau sur DEBUG, on lui dit qu'il doit utiliser le formateur
    # créé précédement et on ajoute ce handler au logger
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # création d'un second handler qui va rediriger chaque écriture de log
    # sur la console
    steam_handler = logging.StreamHandler()
    steam_handler.setLevel(logging.DEBUG)
    logger.addHandler(steam_handler)


def main(argv):
    """

    :param argv:
    :return:
    """
    init_log()

    args = parse_arguments(argv)
    print_args(args)

    # url: http://stackoverflow.com/questions/713794/catching-an-exception-while-using-a-python-with-statement
    try:
        with open(args.ori, 'r') as fo_exportori:
            arr_oris = export_ori_fileobject_to_OmegaPhiKhapa(fo_exportori, args.pivot[0], args.pivot[1], args.pivot[2])
            if arr_oris:
                write_OPK_to_shp_file(arr_oris, args.shapefile, args.viewdir, args.viewdir_length_proj)
    except IOError as err:
        logger.error('Exception: %s', err)


if __name__ == "__main__":
    main(sys.argv[1:])
