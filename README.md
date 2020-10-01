

# pyRFU

pyRFU is a software based on the IRFU-MATLAB library to work with space data, particularly the Magnetospheric MultiScale (MMS) mission. 


# Instalation
pyRFU supports Windows, macOS and Linux. 

## Requirements
pyRFU uses packages not included in python3. To get started, install the required packages using :

```python
pip install -r requirements.txt
```

## From TestPyPi
pyRFU uses TestPyPI a separate instance of the Python Package index to not affect the real index. To get started, install the pyrfu package using TestPyPI:

```python
pip install --index-url https://test.pypi.org/project/ --no-deps pyrfu 
```


# Usage
To import generic space plasma physics functions
```python
from pyrfu import pyrf
```

To import functions specific to MMS mission
```python
from pyrfu import mms
```

To import plotting functions
```python
from pyrfu import plot as pltrf
```

# Configuration

Configuration settings are set in the CONFIG hash table in the mms_config.py file.

# Credits 
This software was developped by Louis RICHARD (louisr@irfu.se) based on the IRFU-MATLAB library.

# Acknowledgement
Please use the following to acknowledge use of pyrfu in your publications:
Data analysis was performed using the pyrfu analysis package available at https://github.com/louis-richard/irfu-python

# Additional Information

MMS Science Data Center: https://lasp.colorado.edu/mms/sdc/public/

MMS Datasets: https://lasp.colorado.edu/mms/sdc/public/datasets/

MMS - Goddard Space Flight Center: http://mms.gsfc.nasa.gov/
