# A python routine to read an ATMO chemistry file 

import netCDF4 as nc

def read_atmo_chem(fname):

  #Read atmo chemistry file
  data = nc.Dataset(fname)

  #Get pressure, abundances and molecule names
  pressure   = data.variables['pressure'][:]*0.1 # Convert to Pa 
  abundances = data.variables['abundances'][:,:]
  names      = data.variables['molname'][:]

  return pressure, abundances, names

def read_atmo_chem_cpmmw(fname):

  #Read atmo chemistry file
  data = nc.Dataset(fname)

  #Get pressure, cp and mean molecular weight
  pressure   = data.variables['pressure'][:]*0.1 # Convert to Pa 
  cp         = data.variables['cp'][:]
  mmw        = data.variables['mean_mol_mass'][:]

  return pressure, cp, mmw

