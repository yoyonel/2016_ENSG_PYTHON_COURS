#!/usr/bin/env python
# -*- coding: utf-8 -*-
import shapefile
import argparse
import numpy as np
from math import sin, cos, degrees, radians, atan2

# for doctest
import numpy

# for doctest
# url: http://python-future.org/compatible_idioms.html
try:
    import StringIO
except ImportError:
    from io import StringIO  # for handling unicode strings

import logging
from logging.handlers import RotatingFileHandler

# urls:
# - https://pypi.python.org/pypi/pyshp
# - http://pygis.blogspot.fr/2012/10/pyshp-attribute-types-and-point-files.html
# - http://gis.stackexchange.com/questions/85448/python-how-to-create-a-polygon-shapefile-from-a-list-of-x-y-coordinates

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
    {'yaw': -172.350586, 'altitude': 53.534337, 'roll': -75.622522, 'easting': 657739.197431, 'pitch': -40.654833, 'id': 'IMG_1468832894.185000000.jpg', 'northing': 6860690.284637}
    """
    md = dict()

    # Identifiant
    md["id"] = tab[0]  # nom du fichier image
    # Orientation
    md["roll"] = float(tab[1])
    md["pitch"] = float(tab[2])
    md["yaw"] = float(tab[3])
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


def export_oriexportfileobject_to_oriarray(fo_oriexport, x0=0, y0=0, z0=0):
    """

    :param fo_oriexport:
    :param x0:
    :param y0:
    :param z0:
    :return:

    url: https://docs.python.org/2/library/stringio.html
    >>> output = StringIO.StringIO('''IMG_1468832894.185000000.jpg -75.622522 -40.654833 -172.350586 \
                                    657739.197431 6860690.284637 53.534337''')
    >>> export_oriexportfileobject_to_oriarray(output)
    [{'yaw': -172.350586, 'altitude': 53.534337, 'roll': -75.622522, 'easting': 657739.197431, 'pitch': -40.654833, 'id': 'IMG_1468832894.185000000.jpg', 'northing': 6860690.284637}]
    >>> output.close()
    """
    try:
        return [_parse_tabline_from_orifile(_convert_line_to_tab_from_orifile(line), x0, y0, z0)
                for line in fo_oriexport]
    except Exception as err:
        logger.error("Exception: " % err)
        return []


def build_rotationmatrix_from_micmac(roll, pitch, yaw):
    """

    :param heading:
    :param roll:
    :param pitch:
    :return:

    Doc MicMac: docmicmac-2.pdf
    -----------------------------------------------------
    13.3.4 Exporting external oriention to Omega-Phi-Kapa
    -----------------------------------------------------
    Matrix R gives rotation terms to compute parameters in matrix encoding with respect to Omega-Phi-
    Kappa angles given by the tool OriExport:
        |cos(φ)∗cos(κ)   cos(φ)∗sin(κ)   −sin(φ)                                                |
    R = |cos(ω)∗sin(κ)+sin(ω)∗sin(φ)∗cos(κ)  −cos(ω)∗cos(κ)+sin(ω)∗sin(φ)∗sin(κ) sin(ω)∗cos(φ)  |
        |sin(ω)∗sin(κ)−cos(ω)∗sin(φ)∗cos(κ)  −sin(ω)∗cos(κ)−cos(ω)∗sin(φ)∗sin(κ) −cos(ω)∗cos(φ) |

    - roulis (roll)     ω - omega   - par rapport à l'axe X
    - tangage (pitch)   φ - phi     - par rapport à l'axe Y
    - lacet (yaw)       κ - kappa   - par rapport à l'axe Z

    >>> mat_computed = build_rotationmatrix_from_micmac(roll=radians(-5.819826), pitch=radians(-7.058795), yaw=radians(-12.262634))
    >>> mat_expected = numpy.array( \
            [[   0.969777798578237427, -0.210783330505758815,   0.122887790140630643,   0.        ],    \
            [   -0.199121821850641506, -0.974794184828703614,  -0.100631989382226852,   0.        ],    \
            [   0.141001849092942777,   0.0731210284736428379, -0.987305319416100224,   0.        ],    \
            [   0.,                     0.,                     0.,                     1.        ]])
    >>> numpy.allclose(mat_computed, mat_expected)
    True

    """
    cos_omega = cos(roll)
    sin_omega = sin(roll)
    cos_phi = cos(pitch)
    sin_phi = sin(pitch)
    cos_kappa = cos(yaw)
    sin_kappa = sin(yaw)

    return numpy.array([
        [cos_phi*cos_kappa, cos_phi*sin_kappa, -sin_phi, 0.],
        [cos_omega*sin_kappa+sin_omega*sin_phi*cos_kappa, -cos_omega*cos_kappa+sin_omega*sin_phi*sin_kappa, sin_omega*cos_phi, 0.],
        [sin_omega*sin_kappa-cos_omega*sin_phi*cos_kappa, -sin_omega*cos_kappa-cos_omega*sin_phi*sin_kappa, -cos_omega*cos_phi, 0.],
        [0., 0., 0., 1.]
    ])


def extract_and_convert_rollpitchyaw_from_dictori(dict_ori):
    """

    :param dict_ori:
    :return:

    >>> dict_ori = {'altitude': 53.534337, 'id': 'IMG_1468832894.185000000.jpg', 'easting': 657739.197431, \
                    'pitch': -172.350586, 'yaw': -75.622522, 'roll': -40.654833, 'northing': 6860690.284637}
    >>> extract_and_convert_rollpitchyaw_from_dictori(dict_ori)
    (-0.7095606926984439, -3.0080851934416435, -1.3198619975618473)
    """
    # extract
    roll, pitch, yaw = dict_ori["roll"], dict_ori["pitch"], dict_ori["yaw"]
    # convert (degree -> radian)
    roll = radians(roll)
    pitch = radians(pitch)
    yaw = radians(yaw)
    return roll, pitch, yaw


def extract_center_from_dictori(dict_ori):
    """

    :param dict_ori:
    :return:

    >>> dict_ori = {'id': 'IMG_1468832894.185000000.jpg', \
                    'altitude': 53.534337, 'easting': 657739.197431, 'northing': 6860690.284637, \
                    'pitch': -172.350586, 'yaw': -75.622522, 'roll': -40.654833}
    >>> extract_center_from_dictori(dict_ori)
    [657739.197431, 6860690.284637, 53.534337, 1]
    """
    return [dict_ori["easting"], dict_ori["northing"], dict_ori["altitude"], 1]


def write_shp_viewdir_from_arrori(arr_oris, export_filename, viewdir_length_proj=1.0):
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
    # url: http://gis.stackexchange.com/questions/41742/problems-converting-csv-to-shapefile-using-pyshp
    w.field("ANGLE", "N")

    zaxis = [0, 0, 1, 0]
    yaxis = np.array([0, 1, 0, 0])

    # This time write each line separately
    # with its own dbf record
    for _, ori in enumerate(arr_oris):
        # on extrait le centre de la prise de vue
        center = extract_center_from_dictori(ori)
        # on extrait les informations d'orientation
        roll, pitch, yaw = extract_and_convert_rollpitchyaw_from_dictori(ori)
        # on calcule la matrix de rotation a partir de ces informations d'orientation
        # matrix_rot = build_rotationmatrix_from_euler_(roll, pitch, yaw)
        matrix_rot = build_rotationmatrix_from_micmac(roll, pitch, yaw)
        # url: http://docs.scipy.org/doc/numpy/reference/generated/numpy.multiply.html
        view_vec = np.multiply(zaxis, viewdir_length_proj)
        # on calcule le vecteur de vue
        rot_view_vec = np.dot(matrix_rot, view_vec)
        # on construit la segment de vue
        segment_view = [center, np.add(rot_view_vec, center).tolist()]
        # url: http://stackoverflow.com/questions/21483999/using-atan2-to-find-angle-between-two-vectors
        angle = degrees(atan2(np.cross(rot_view_vec[0:2], yaxis[0:2]), np.dot(yaxis, rot_view_vec)))
        # print segment_view
        w.poly(parts=[segment_view])
        #
        w.record("segment_view", angle)
    # Save
    w.save(export_filename)
    logger.info("Export file: %s", export_filename)


def write_shp_idpositions_from_arrori(
        arr_oris,
        export_filename,
        field_0_name="id",
        field_1_name="position"
):
    """

    :param arr_oris:
    :param export_filename:
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


def parse_arguments():
    """

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


def main():
    """

    :param argv:
    :return:
    """
    init_log()

    args = parse_arguments()
    print_args(args)

    # url: http://stackoverflow.com/questions/713794/catching-an-exception-while-using-a-python-with-statement
    try:
        with open(args.ori, 'r') as fo_exportori:
            arr_oris = export_oriexportfileobject_to_oriarray(fo_exportori, args.pivot[0], args.pivot[1], args.pivot[2])
            if arr_oris:
                write_shp_idpositions_from_arrori(arr_oris, args.shapefile)
                if args.viewdir:
                    write_shp_viewdir_from_arrori(arr_oris, args.shapefile + "_view_dir", args.viewdir_length_proj)
    except IOError as err:
        logger.error('Exception: %s', err)


if __name__ == "__main__":
    main()
