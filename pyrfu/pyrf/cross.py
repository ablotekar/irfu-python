import xarray as xr
import numpy as np

from .resample import resample
from .ts_vec_xyz import ts_vec_xyz


def cross(inp1=None,inp2=None):
	"""
	Computes cross product of two fields z = xxy

	Parameters :
		- inp1 : DataArray
			Time series of the first field x

		- inp2 : DataArray
			Time series of the second field y

	Returns :
		- out : DataArray
			Time series of the cross product inp1xinp2

	Example :
		>>> Tint = ["2019-09-14T07:54:00.000","2019-09-14T08:11:00.000"]
		>>> gseB = mms.get_data("B_gse_fgm_srvy_l2",Tint,1)
		>>> gseE = mms.get_data("E_gse_edp_fast_l2",Tint,1)
		>>> Bmag = pyrf.norm(gseB)
		>>> gseExB = pyrf.cross(gseE,gseB)/Bmag**2

	"""

	if not isinstance(inp1,xr.DataArray):
		raise TypeError("Inputs must be DataArrays")

	if not isinstance(inp2,xr.DataArray):
		raise TypeError("Inputs must be DataArrays")
		
	if len(inp1) != len(inp2):
		inp2 = resample(inp2,inp1)
		
	outdata = np.cross(inp1.data,inp2.data,axis=1)

	out = ts_vec_xyz(inp1.time.data,outdata)
	
	return out


