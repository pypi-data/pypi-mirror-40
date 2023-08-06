# PYroMat changelog

## Version 1.1: 
Original Release, including ideal gas data

## Version 1.2: 
- Add the 'steam' substance and its class, if97.
- Added new functionality to reg.__baseclass__._vectorize()
- Corrected inconsistent capitalization p/P usage across classes.  Lower case p 
    is now used for pressure in all classes.  This may cause reverse 
    compatibility issues between 1.1 and 1.2 if your code calls out P in its 
    arguments.
- Corrected a bug in psolve() caused by the same inconsistency
- Changed the "def_T" configuration parameter to 300. Some species' data are not
    defined below 300, so the default of 298.15 caused an error.
- Corrected all IG pressure references to be 1 bar instead of 1 atm to be 
    consistent with the source JANAF reference data.
- Replaced def_P with def_p to be consistent with the lower case pressure 
    definition.

## Version 1.3:
- Ported to GIT
- Changed package name from pyro to pyromat to avoid collision with existing 
    (https://pythonhosted.org/Pyro4/)
- Edited inline documentation to reflect changes
- Cleaned up some code in the data module (functionality should not change)
- Eliminated the input error class and reverted to the parameter error
- Changed the method for detecting the installation directory 
    utility.load_config()
- Eliminated a bug that caused the IGTAB class _lookup() method to fail in 
    Python3

## Version 1.4:
- Added the solve module
- Obsoleted the psolve() function
- Added inverse relations T_h() and T_s() to all classes
- Added inverse relations p_h() and p_s() to the ideal gas classes
- Changed the namespace handling so that registry class definitions behave like
    normal files.
- Added methods for calculating the inverse polynomials to the IF-97 class

## Version 2.0.1
This is the first version that deliberately breaks reverse compatibility.  Every time reverse compatibility is not preserved, the major version number will increase.

- Provides a uniform array handling behavior for all classes
    - All methods now accept arrays or array-like objects of any dimension
    - All methods attempt reduce their returns to scalars if possible
    - All methods return values that obey Numpy broadcasting rules
    - Some methods will return a Python float and others return a Numpy array scalar depending on implementation
- Provides a new configuration class, for in-line configuration
    - config[] is now a dictionary-like object and NOT a dictionary.
    - config[] enforces its own rules about type etc.
    - config scripts still behave identically.
- Provides a new unit conversion module, "units"
    - config["unit_XXX"] now configures global unit defaults for unit XXX.
    - Added unit conversion routines
    - in-line documentation for all property methods reports the config unit parameters on which they depend.
- Modifies the info() function to print a table of supported properties
- Adds Tlim() and plim() to IF-97 (steam)
- Migrates specific heat ratio method k() to gam() in preparation for k() to become thermal conductivity

## Version 2.0.4
The version increments between 2.0.1 and 2.0.4 were primarily spent correcting issues with the python package index and documentation.
- Corrected a bug that prevented `info()` from displaying in Python 3.

## Version 2.0.5
- Corrected a bug preventing T_s() in the if97 (steam) class from returning quality correctly.

## Version 2.0.6
- Corrected a bug that caused hsd() in the if97 (steam) class to crash
- Corrected a bug in the configuration object that prevented a parameter summary from displaying correctly in Python 3.

## Version 2.0.7
- Added the mp1 multi-phase class
- Migrated steam away from if97 to the mp1 class
- Added CO2 and R134a (C2H2F4) to the multiphase data
- Added ig2 class incorporating the NASA polynomial
- Added hundreds of new ideal gas data including a better ig.H2O data set

## Version 2.0.8
- Corrected unit conversion in mp1 density output

## Version 2.0.9
- Skipped due to an error uploading to the Python package index

## Version 2.0.10
- Temperature units in T_s, T_h, and T in the mp1 class were not being converted: fixed.

## Version 2.0.11
- Corrected a bug in units.matter(); inplace directives were not being honored in certain cases, causing odd errors in T_s and T_h()

## Version 2.0.12
- Corrected data error in CO2 that caused errors near the saturation curve
- Added support for specifying T,p, and x simultaneously; p is ignored unless x<0
- Added the aps module with support for calculating the performance of thermodynamic cycles
