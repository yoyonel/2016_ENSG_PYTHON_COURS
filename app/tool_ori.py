#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tool_log import logger
# for doctest
# url: http://python-future.org/compatible_idioms.html
try:
    import StringIO
except ImportError:
    from io import StringIO  # for handling unicode strings
#
import shapefile
import numpy as np
from math import degrees, radians, atan2
#
from tool_micmac import build_rotationmatrix_from_micmac


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
                for line in fo_oriexport
                ]
    except Exception as err:
        logger.error("Exception: " % err)
        return []


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


def export_meanposition_from_arrori(mean_position_export, arr_oris):
    """
    Calcul la position moyenne des positions de prise de vue.
    Ca revient à calculer le barycentre des positions de la trajectoire (issue du fichier ORI).

    :param mean_position_export:
    :param arr_oris:
    :return:
    """
    # On extrait les arrays des coordonnées (x, y, z) du tableau des oris
    # ps: pas super optimal, car on décompacte (un fichier OriExport) pour compacter (en liste de dict Ori)
    # pour ensuite décompacter à nouveau en listes/array de vector 1D sur chaque dimension (x, y, z) ...
    x = np.array([ori['easting'] for ori in arr_oris])
    y = np.array([ori['northing'] for ori in arr_oris])
    z = np.array([ori['altitude'] for ori in arr_oris])
    # On construit la chaine de caractere representant notre position mediane
    mean_position = [x.mean(), y.mean(), z.mean()]
    str_mean_position = "{}".format(mean_position)
    # petit log pour la forme
    logger.info("mean position: %s", str_mean_position)
    # On ecrit cette position dans un fichier d'export (mean_position_export)
    try:
        with open(mean_position_export, 'w') as fo_exportmeanposition:
            fo_exportmeanposition.write(str_mean_position)
        logger.info("Export file: %s", mean_position_export)
    except IOError as err:
        logger.error('Exception: %s', err)
    # on retourne la mean position
    return mean_position