# url: http://stackoverflow.com/questions/36318440/python-nosetests-import-file-path-with-multiple-modules-files
try:
    from app.OriExport_to_shapefile import write_shp_viewdir_from_arrori
    from app.OriExport_to_shapefile import write_shp_idpositions_from_arrori, extract_center_from_dictori
except:
    import sys
    sys.path.append("../app")
    from OriExport_to_shapefile import write_shp_viewdir_from_arrori
    from OriExport_to_shapefile import write_shp_idpositions_from_arrori, extract_center_from_dictori
#
import unittest
from os.path import exists
from os import mkdir
from shutil import rmtree
import shapefile
import numpy as np

# coding=utf-8
__author__ = 'YoYo'


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
        # rmtree(prefix_for_export)
        # mkdir(prefix_for_export)
        try:
            rmtree(prefix_for_export)
            mkdir(prefix_for_export)
        except OSError:
            pass

    def _raise_assert_on_np_is_close_all(self, np0, np1):
        """
        Helper pour les tests
        ---------------------
        Utilise Numpy pour determiner si deux entites (numpy) sont proches.
        Leve une exception si ce n'est pas le cas.
        :param np0:
        :param np1:
        :return:
        """

        return self.assertTrue(np.isclose(np0, np1).all())

    def test_write_OPK_to_shp_file(self):
        """
        Test
        ----
        Test la methode 'app.write_OPK_to_shp_file' qui
        ecrit dans un shapefile les positions des centres optiques calculees depuis un array d'ORIs.
        """
        arr_oris = [{'altitude': 53.534337, 'id': 'IMG_1468832894.185000000.jpg', 'easting': 657739.197431,
                     'pitch': -172.350586, 'heading': -75.622522, 'roll': -40.654833, 'northing': 6860690.284637}]

        # on export le shapefile a partir des donnees pour le tests
        write_shp_idpositions_from_arrori(arr_oris, self.test_shapefile)
        # on tests si la methode a exporte les fichiers
        # url: http://stackoverflow.com/questions/82831/how-to-check-whether-a-file-exists-using-python
        self.assertTrue(exists(self.test_shapefile))

        # lecture d'un shapefile
        r = shapefile.Reader(self.test_shapefile)
        # geometries
        shapes = r.shapes()
        # extraction de la listes des points
        list_points = shapes[0].points
        # 1 point definit dans le shapefile
        self.assertEqual(len(shapes), 1)
        # on tests le type de la shape stockee
        # url: http://www.esri.com/library/whitepapers/pdfs/shapefile.pdf
        # type == 1 => Shape type=Point
        self.assertEqual(shapes[0].shapeType, 1)
        # on utilise extract_center_dict_ori (qui est doctestee)
        self._raise_assert_on_np_is_close_all(list_points[0], extract_center_from_dictori(arr_oris[0])[:2])

    def test_write_viewdir_shp_from_arr_ori(self):
        """
        Test
        ----
        Test la methode 'app.write_viewdir_shp_from_arr_ori' qui
        ecrit dans un shapefile des directions de vues calculees depuis un array d'ORIs.
        """
        # TODO: tester chacune des orientations (pitch, heading, roll)
        # url: http://support.pcigeomatics.com/hc/en-us/articles/203483349-Heading-Pitch-Roll-vs-Omega-Phi-Kappa
        arr_oris = [
            {
                'id': 'IMG_1468832894.185000000.jpg',
                'northing': 6860690.284637,
                'easting': 657739.197431,
                'altitude': 53.534337,
                'pitch': -90.0,
                'yaw': 0.0,
                'roll': 0.0
            }]

        write_shp_viewdir_from_arrori(arr_oris,
                                      self.test_shapefile,
                                      viewdir_length_proj=10.0)

        # on tests si la methode a exporte les fichiers
        self.assertTrue(exists(self.test_shapefile))

        # lecture d'un shapefile
        r = shapefile.Reader(self.test_shapefile)
        # geometries
        shapes = r.shapes()
        # extraction de la listes des points
        list_points = shapes[0].points
        # 1 point defini dans le shapefile
        self.assertEqual(len(shapes), 1)
        # on tests le type de la shape stockee
        # 13 PolyLineZ
        self.assertEqual(shapes[0].shapeType, 13)

        # On tests les points contenus dans le shapefile
        # point 1: centre de l'ori
        point1_expected = extract_center_from_dictori(arr_oris[0])[:2]
        self._raise_assert_on_np_is_close_all(list_points[0], point1_expected)
        # point 2: centre de l'ori + projection (longueur=10) dans la direction de vue
        point2_expected = np.add(extract_center_from_dictori(arr_oris[0])[:2], [10.0, 0.0])
        self._raise_assert_on_np_is_close_all(list_points[1], point2_expected)


if __name__ == '__main__':
    unittest.main()
