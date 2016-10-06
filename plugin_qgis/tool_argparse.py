import argparse
from tool_log import logger


def parse_arguments(_):
    """

    :param _:
    :return:
    """
    parser = argparse.ArgumentParser()

    #
    parser.add_argument("shp_path", type=str, help="Path vers le shapefile")
    parser.add_argument("imgs_path", type=str, help="Path vers les images")
    #
    parser.add_argument("-s", "--shp_basename", type=str,
                        default="OriExport_Ori-RTL-Init.shp",
                        help="Basename du shapefile (default: %(default)s)")
    parser.add_argument("-i", "--imgs_pattern_ext", type=str,
                        default="*.jpg",
                        help="Pattern des extensions pour les images (default: %(default)s)")

    args = parser.parse_args()

    return args


def print_args(args):
    """

    :param args:
    :return:
    """
    logger.info("- shapefile path: {}".format(args.shp_path))
    logger.info("- images path: %s" % args.imgs_path)
    logger.info("- shapefile basename: %s" % args.shp_basename)
    logger.info("- images extensions pattern: %s" % args.imgs_pattern_ext)
