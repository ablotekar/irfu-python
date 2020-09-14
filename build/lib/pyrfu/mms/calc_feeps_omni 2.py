#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
calc_feeps_omni.py

@author : Louis RICHARD
"""

import numpy as np
import xarray as xr
import warnings

from .feeps_split_integral_ch import feeps_split_integral_ch
from .feeps_remove_sun import feeps_remove_sun


def calc_feeps_omni(inp_dset):
	"""
	Computes the omni-directional FEEPS spectrograms from a Dataset that contains the spectrograms of all eyes.

	Parameters:
		inp_dset : Dataset
			Dataset with energy spectrum of every eyes

	Returns:
		out : DataArray
			OMNI energy spectrum from the input

	"""

	var = inp_dset.attrs

	if var["dtype"] == "electron":
		energies = np.array(
			[33.2, 51.90, 70.6, 89.4, 107.1, 125.2, 146.5, 171.3, 200.2, 234.0, 273.4, 319.4, 373.2, 436.0, 509.2])
	else:
		energies = np.array(
			[57.9, 76.8, 95.4, 114.1, 133.0, 153.7, 177.6, 205.1, 236.7, 273.2, 315.4, 363.8, 419.7, 484.2, 558.6])

	# set unique energy bins per spacecraft; from DLT on 31 Jan 2017
	ecorr = {"e": [14.0, -1.0, -3.0, -3.0], "i": [0.0, 0.0, 0.0, 0.0]}
	gfact = {"e": [1.0, 1.0, 1.0, 1.0], "i": [0.84, 1.0, 1.0, 1.0]}

	energies += ecorr[var["dtype"][0]][var["mmsId"]-1]

	# percent error around energy bin center to accept data for averaging; 
	# anything outside of energies[i] +/- en_chk*energies[i] will be changed 
	# to NAN and not averaged   
	en_chk = 0.10

	"""
	top_sensors = eyes['top']
	bot_sensors = eyes['bottom']
	"""

	inp_dset_clean, inp_dset_500kev = feeps_split_integral_ch(inp_dset)

	inp_dset_clean_sun_removed = feeps_remove_sun(inp_dset_clean)

	eye_list = list(inp_dset_clean_sun_removed.keys())
	tmp_data = inp_dset_clean_sun_removed[eye_list[0]]

	d_all_eyes = np.empty((tmp_data.shape[0], tmp_data.shape[1], len(inp_dset_clean_sun_removed)))
	d_all_eyes[:] = np.nan

	for i, k in enumerate(eye_list):
		d_all_eyes[..., i] = inp_dset_clean_sun_removed[k].data

		try:
			diff_en_ch = inp_dset_clean_sun_removed[k].coords["Differential_energy_channels"].data
			ie = np.where(np.abs(energies - diff_en_ch) > en_chk * energies)
			
			if ie[0].size != 0:
				d_all_eyes[:, ie[0], i] = np.nan

		except Warning:
			print('NaN in energy table encountered; sensor T{}'.format(k))

	with warnings.catch_warnings():
		warnings.simplefilter("ignore", category=RuntimeWarning)
		flux_omni = np.nanmean(d_all_eyes, axis=2)

	flux_omni *= gfact[var["dtype"][0]][var["mmsId"]-1]

	t, attrs = [inp_dset_clean_sun_removed.time, inp_dset_clean_sun_removed[eye_list[0]].attrs]

	out = xr.DataArray(flux_omni, coords=[t, energies], dims=["time", "energy"], attrs=attrs)

	return out
