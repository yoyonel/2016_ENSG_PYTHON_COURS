#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import sin, cos, radians
import numpy as np


def build_rotationmatrix_from_micmac(roll, pitch, yaw):
    """

    :param roll:
    :param pitch:
    :param yaw:
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

    >>> mat_computed = build_rotationmatrix_from_micmac(roll=radians(-5.819826), \
    pitch=radians(-7.058795), yaw=radians(-12.262634))
    >>> mat_expected = np.array( \
            [[   0.969777798578237427, -0.210783330505758815,   0.122887790140630643,   0.        ],    \
            [   -0.199121821850641506, -0.974794184828703614,  -0.100631989382226852,   0.        ],    \
            [   0.141001849092942777,   0.0731210284736428379, -0.987305319416100224,   0.        ],    \
            [   0.,                     0.,                     0.,                     1.        ]])
    >>> np.allclose(mat_computed, mat_expected)
    True

    """
    # o: Omega, p: Phi, k: Kappa
    cos_o = cos(roll)
    sin_o = sin(roll)
    cos_p = cos(pitch)
    sin_p = sin(pitch)
    cos_k = cos(yaw)
    sin_k = sin(yaw)
    #
    return np.array([
        [cos_p*cos_k, cos_p*sin_k, -sin_p, 0.],
        [cos_o*sin_k+sin_o*sin_p*cos_k, -cos_o*cos_k+sin_o*sin_p*sin_k, sin_o*cos_p, 0.],
        [sin_o*sin_k-cos_o*sin_p*cos_k, -sin_o*cos_k-cos_o*sin_p*sin_k, -cos_o*cos_p, 0.],
        [0., 0., 0., 1.]
    ])
