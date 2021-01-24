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

import xarray as xr


def ts_vec_xyz(t, data, attrs=None):
    """Create a time series containing a 1st order tensor.

    Parameters
    ----------
    t : ndarray
        Array of times.

    data : ndarray
        Data corresponding to the time list.

    attrs : dict
        Attributes of the data list.

    Returns
    -------
    out : xarray.DataArray
        1st order tensor time series.

    """

    assert data.ndim == 2 and data.shape[1] == 3

    if len(t) != len(data):
        raise IndexError("Time and data must have the same length")

    flag_attrs = True

    if attrs is None:
        flag_attrs = False

    out = xr.DataArray(data, coords=[t[:], ["x", "y", "z"]], dims=["time", "comp"])

    if flag_attrs:
        out.attrs = attrs

        out.attrs["TENSOR_ORDER"] = 1
    else:
        out.attrs["TENSOR_ORDER"] = 1

    return out
