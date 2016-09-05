# coding=utf-8
__author__ = 'YoYo'

import unittest
from app.OriExport_to_shapefile import write_viewdir_shp_from_arr_ori
from app.OriExport_to_shapefile import write_OPK_to_shp_file
from app.OriExport_to_shapefile import extract_center_dict_ori
from os.path import exists
from os import mkdir
from shutil import rmtree
import shapefile
import numpy as np


class Test_OriExport_to_shapefile(unittest.TestCase):
    def setUp(self):
        """

        :return:
        """
        # setting for export
        prefix_for_export = "export/"
        self.test_shapefile = prefix_for_export + "Test_OriExport_to_shapefile.shp"
        # clear the export directory
        # urls:
        # - http://stackoverflow.com/questions/273192/how-to-check-if-a-directory-exists-and-create-it-if-necessary
        # - https://docs.python.org/3/library/shutil.html#shutil.rmtree
        rmtree(prefix_for_export)
        mkdir(prefix_for_export)

    def test_write_OPK_to_shp_file(self):
        """

        :return:
        """
        arr_oris = [{'altitude': 53.534337, 'id': 'IMG_1468832894.185000000.jpg', 'easting': 657739.197431,
                          'pitch': -172.350586, 'heading': -75.622522, 'roll': -40.654833, 'northing': 6860690.284637}]

        # on export le shapefile à partir des données pour le tests
        write_OPK_to_shp_file(arr_oris,
                              self.test_shapefile,
                              b_export_view_dir=False)
        # on tests si la methode a exporté les fichiers
        # url: http://stackoverflow.com/questions/82831/how-to-check-whether-a-file-exists-using-python
        self.assertTrue(exists(self.test_shapefile))

        # lecture d'un shapefile
        r = shapefile.Reader(self.test_shapefile)
        # géométries
        shapes = r.shapes()
        # 1 point défini dans le shapefile
        self.assertEqual(len(shapes), 1)
        # on tests le type de la shape stockée
        # url: http://www.esri.com/library/whitepapers/pdfs/shapefile.pdf
        # type == 1 => Shape type=Point
        self.assertEqual(shapes[0].shapeType, 1)
        # on utilise extract_center_dict_ori (qui est doctestée)
        self.assertTrue(np.isclose(shapes[0].points[0], extract_center_dict_ori(arr_oris[0])[:2]).all())

    def test_write_viewdir_shp_from_arr_ori(self):
        """

        :return:
        """
        # url: http://support.pcigeomatics.com/hc/en-us/articles/203483349-Heading-Pitch-Roll-vs-Omega-Phi-Kappa
        arr_oris = [
            {
                'id': 'IMG_1468832894.185000000.jpg',
                'northing': 6860690.284637,
                'easting': 657739.197431,
                'altitude': 53.534337,
                'pitch': -90.0,
                'heading': 0.0,
                'roll': 0.0
            }]

        write_viewdir_shp_from_arr_ori(arr_oris,
                                       self.test_shapefile,
                                       viewdir_length_proj=10.0)

        # on tests si la methode a exporté les fichiers
        self.assertTrue(exists(self.test_shapefile))

        # lecture d'un shapefile
        r = shapefile.Reader(self.test_shapefile)
        # géométries
        shapes = r.shapes()
        # 1 point défini dans le shapefile
        self.assertEqual(len(shapes), 1)
        # on tests le type de la shape stockée
        # 13 PolyLineZ
        self.assertEqual(shapes[0].shapeType, 13)

        # On tests les points contenus dans le shapefile
        # point 1: centre de l'ori
        point1_expected = extract_center_dict_ori(arr_oris[0])[:2]
        self.assertTrue(np.isclose(shapes[0].points[0], point1_expected).all())
        # point 2: centre de l'ori + projection (longueur=10) dans la direction de vue
        point2_expected = np.add(extract_center_dict_ori(arr_oris[0])[:2], [10.0, 0.0])
        self.assertTrue(np.isclose(shapes[0].points[1], point2_expected).all())
        #
        # print("shapes[0].points[0]:  ", shapes[0].points[0])
        # print("shapes[0].points[1]:  ", shapes[0].points[1])

        # TODO: tester chacune des orientations (pitch, heading, roll)


if __name__ == '__main__':
    unittest.main()