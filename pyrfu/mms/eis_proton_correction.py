#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 3rd party imports
import numpy as np

__author__ = "Louis Richard"
__email__ = "louisr@irfu.se"
__copyright__ = "Copyright 2020-2021"
__license__ = "MIT"
__version__ = "2.3.7"
__status__ = "Prototype"


def _phxtof_calibration(energy, alpha, beta, gamma):
    r"""Pulse Height x Time Of Flight correction model from EPD Data Product
    Guide"""
    return 1 / (.5 * (1 + alpha * (np.tanh((energy - beta) / gamma) + 1)))


def _extof_calibration(energy, alpha, beta, gamma):
    r"""Energy x Time Of Flight correction model from EPD Data Product Guide"""
    return 1 / (.5 * (1 + alpha * (1 - np.tanh((energy - beta) / gamma) + 1)))


def eis_proton_correction(flux_eis):
    r"""Corrects proton flux values based on FPI/HPCA/EPD-EIS cross
    calibration.

    Parameters
    ----------
    flux_eis : xarray.DataArray
        Omni-directional energy spectrum from EPD-EIS.

    Returns
    -------
    flux_eis_corr : xarray.DataArray
        Cross-calibrated omni-directional energy spectrum from EIS-EPD.

    See Also
    --------
    pyrfu.mms.get_eis_allt, pyrfu.mms.eis_omni

    """

    #  Coefficients from EPD Data Product Guide
    alpha_, beta_, gamma_ = [-.3, 49e-3, 1e-3]

    # Pulse Height x Time Of Flight (PHxTOF) energy correction factor
    energy_phxtof = flux_eis.energy.data[:7]
    phxtof_corr = _phxtof_calibration(energy_phxtof, alpha_, beta_, gamma_)

    # Energy x Time Of Flight (ExTOF) energy correction factor
    energy_extof = flux_eis.energy.data[7:]
    extof_corr = _extof_calibration(energy_extof, alpha_, beta_, gamma_)

    eis_corr = np.hstack([phxtof_corr, extof_corr])

    # Apply correction to omni-directional energy spectrum
    flux_eis_corr = flux_eis.copy()
    flux_eis_corr.data *= eis_corr

    return flux_eis_corr
