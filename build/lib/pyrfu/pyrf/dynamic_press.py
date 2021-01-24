#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# MIT License
#
# Copyright (c) 2020 Louis Richard
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so.

import numpy as np

from astropy import constants


def dynamic_press(n, v, s="i"):
    """Computes dynamic pressure.

    Parameters
    ----------
    n : xarray.DataArray
        Time series of the number density of the specie.

    v : xarray.DataArray
        Time series of the bulk velocity of the specie.

    s : str {"i", "e"}, optional
        Specie. default "i".

    Returns
    -------
    p_dyn : xarray.DataArray
        Time series of the dynamic pressure of the specie.

    Examples
    --------
    >>> from pyrfu import mms, pyrf

    Time interval

    >>> tint = ["2019-09-14T07:54:00.000", "2019-09-14T08:11:00.000"]

    Spacecraft index

    >>> mms_id = 1

    Load ion bulk velocity and remove spintone

    >>> v_xyz_i = mms.get_data("Vi_gse_fpi_fast_l2", tint, mms_id)
    >>> st_xyz_i = mms.get_data("STi_gse_fpi_fast_l2", tint, mms_id)
    >>> v_xyz_i = v_xyz_i - st_xyz_i

    Ion number density

    >>> n_i = mms.get_data("Ni_fpi_fast_l2", tint, mms_id)

    Compute dynamic pressure

    >>> p = pyrf.dynamic_press(n_i, v_xyz_i, s="i")

    """

    if s == "i":
        m = constants.m_p.value
    elif s == "e":
        m = constants.m_e.value
    else:
        raise ValueError("Unknown specie")

    p_dyn = n * m * np.linalg.norm(v, axis=0) ** 2

    return p_dyn
