#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
#
from tool_log import logger, init_logger
from tool_ori import dump_ori_fileobject_to_array, \
    export_meanposition_from_arrori,    \
    write_affine_transformation_from_arrori,        \
    write_shp_idpositions_from_arrori,  \
    write_shp_viewdir_from_arrori,  \
    write_dict_oris


# urls:
# - https://pypi.python.org/pypi/pyshp
# - http://pygis.blogspot.fr/2012/10/pyshp-attribute-types-and-point-files.html
# - http://gis.stackexchange.com/questions/85448/python-how-to-create-a-polygon-shapefile-from-a-list-of-x-y-coordinates

# TODO: doc -> ecrire la doc. (reellement) pour les methodes/fonctions
# TODO: doc -> generer la doc par sphinx (ou doxygen)
# TODO: exceptions -> relever plus d'exceptions et les gerer
# TODO: exceptions -> creer des exceptions customs pour ce projet/script


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
                        (default: nom du fichier transmis par le paramètre ori (sans extension))""")

    # option: noms des champs pour l'export shapefile

    # option: export des directions de vue
    # url: http://stackoverflow.com/questions/8259001/python-argparse-command-line-flags-without-arguments
    parser.add_argument("-v", "--viewdir", action='store_true',
                        help="flag pour exporter les directions de vue. (default: %(default)s)")

    # option: longueur des projections des directions de vue
    parser.add_argument("-vl", "--viewdir_length_proj", type=float, default=1.0,
                        help="longueur des projections des directions de vue. (default: %(default)s)")

    # option:
    parser.add_argument("-m", "--mean_position", action='store_true',
                        help="flag pour exporter la position mean des points de vue. (default: %(default)s)")
    #
    parser.add_argument("--mean_position_export", nargs='?', type=str,
                        help="""nom du fichier (sans extension) pour l'export de la mean position\
                                (default: nom du fichier transmis par le parametre ori (sans extension)\
                                 avec suffixe '_meanposition.txt')""")
    # option:
    parser.add_argument("--affine_transformation", action='store_true',
                        help="flag pour exporter les transformations affines (position + rotation) issues des ORIs. \
                        (default: %(default)s)")
    #
    parser.add_argument("--affine_transformation_export", nargs='?', type=str,
                        help="""nom du fichier (sans extension) pour l'export des transformations affines. \
                                    (default: nom du fichier transmis par le parametre ori (sans extension)\
                                     avec suffixe '_affinetransfo.txt')""")

    #
    parser.add_argument("--dict_ori", action='store_true',
                        help="flag pour exporter un dictionnaire d'ORIS. (default: %(default)s)")
    parser.add_argument("--dict_ori_export", nargs='?', type=str,
                        help="""nom du fichier (sans extension) pour l'export du dictionnaire des ORIs\
                                (default: nom du fichier transmis par le parametre ori (sans extension)\
                                 avec suffixe '_dict.txt')""")

    args = parser.parse_args()

    name_ori = args.ori[:-4]

    if args.shapefile is None:
        args.shapefile = name_ori
    if args.mean_position_export is None:
        args.mean_position_export = name_ori + '_meanposition.txt'
    if args.affine_transformation_export is None:
        args.affine_transformation_export = name_ori + '_affinetransfo.txt'
    if args.dict_ori_export is None:
        args.dict_ori_export = name_ori + '_dict.txt'

    return args


def print_args(args):
    """

    :param args:
    :return:
    """
    logger.info("- filename ExportOri: %s", args.ori)
    # print("- prefix for export: ", args.prefix_for_export)
    logger.info("- pivot: %s", args.pivot)
    logger.info("- shapefile: %s", args.shapefile)
    logger.info("- export view dir: %s", args.viewdir)
    if args.viewdir:
        logger.info("-- export view dir - length proj: %s", args.viewdir_length_proj)
    logger.info("- export mean position: %s", args.mean_position)
    if args.mean_position:
        logger.info("-- export mean position export: %s", args.mean_position_export)
    logger.info("- export affine transformation: %s", args.affine_transformation)
    if args.affine_transformation:
        logger.info("-- export affine transformation filename: %s", args.affine_transformation_export)
    logger.info("- export dictionnaire ORIs: %s", args.dict_ori)
    if args.dict_ori:
        logger.info("-- export dictionnaire ORIs filename: %s", args.dict_ori_export)


def main():
    """

    :param argv:
    :return:
    """
    init_logger()

    args = parse_arguments()
    print_args(args)

    # url: http://stackoverflow.com/questions/713794/catching-an-exception-while-using-a-python-with-statement
    try:
        with open(args.ori, 'r') as fo_exportori:
            arr_oris = dump_ori_fileobject_to_array(fo_exportori, args.pivot[0], args.pivot[1], args.pivot[2])
            if arr_oris:
                if args.mean_position:
                    export_meanposition_from_arrori(args.mean_position_export, arr_oris)
                if args.affine_transformation:
                    write_affine_transformation_from_arrori(args.affine_transformation_export, arr_oris)
                #
                write_shp_idpositions_from_arrori(arr_oris, args.shapefile)
                if args.viewdir:
                    write_shp_viewdir_from_arrori(
                        args.shapefile + "_view_dir",
                        arr_oris,
                        args.viewdir_length_proj
                    )
                #
                if args.dict_ori:
                    write_dict_oris(args.dict_ori_export, arr_oris)
    except IOError as err:
        logger.error('Exception: %s', err)


if __name__ == "__main__":
    main()
