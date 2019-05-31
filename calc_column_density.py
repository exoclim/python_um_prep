# Python routine to calculate the column density of a chemical species using an ATMO
# chemistry output file

# Import some modules
import pylab 
import netCDF4 as nc
import numpy as np
import read_atmo_chem as rac
from scipy.interpolate import interp1d

# Reference and surface pressures - in Pa
p_ref = 1e4
p_surf = 1e8

# Function to calculate the column density
def calc_column_density_atmo(sp,abundance,gravity,pressure,abundance_h2,abundance_he):

  # Get abundances of requested molecule, and H2 and He, at p_ref
  fint = interp1d(pressure,abundance)
  amol = fint(p_ref)

  fint = interp1d(pressure,abundance_h2)
  ah2 = fint(p_ref)

  fint = interp1d(pressure,abundance_he)
  ahe = fint(p_ref)

  # Calculate mean molecular weight (assume H2+He dominated)
  mean_mol_weight = ah2*get_molmass('H2') + ahe*get_molmass('He')
  # Calculate column density
  sigma = (p_surf/gravity)*amol*get_molmass(sp)/mean_mol_weight			

  return sigma

# Function to return the molecular mass
def get_molmass(mol):

  if mol=='H2': 
    molmass = 2.01588
  elif mol=='H2O':
    molmass = 18.01528
  elif mol=='NH3':
    molmass = 17.03052
  elif mol=='CH4':
    molmass = 16.0425
  elif mol=='CO':
    molmass = 28.0101
  elif mol=='CO2':
    molmass = 44.0095
  elif mol=='He':
    molmass = 4.0026020
  elif mol=='Na':
    molmass = 22.989769280
  elif mol=='K':
    molmass = 39.09830
  elif mol=='Li':
    molmass = 6.9410
  elif mol=='Cs':
    molmass = 132.90545190
  elif mol=='Rb':
    molmass = 85.46780
  elif mol=='TiO':
    molmass = 63.8664
  elif mol=='VO':
    molmass = 66.94090
  elif mol=='HCN':
    molmass = 27.0253
  else:
    print 'Error: molmass not included: ',mol
    sys.exit()

  return molmass

# Function to return the index of a species in the ATMO chemistry file
def imol(mol,mols):

  index = None

  for i in range(len(mols)):
    if mol==mols[i]:
      index = i

  if index==None:
    print 'Error: molecules not included in ATMO file: ',mol
    sys.exit()

  return index

# Main function
def get_column_density(fname=None,
gravity=None,
species=['H2','He','H2O','CH4','CO','CO2','NH3','Na','K','Li','Rb','Cs','TiO','VO','HCN']):

  # Check required inputs are defined
  if fname==None:
    print 'Error: fname is not defined'
    exit()
  if gravity==None:
    print 'Error: you must define gravity'
    print ' in ms-2'
    exit()

  # Read chemistry file 
  pressure, abundances, names = rac.read_atmo_chem(fname)

  #Get indices of requested species
  species_name = []
  for j in range(len(names[:,0])):
    name = names[j,0]+names[j,1]+names[j,2]+names[j,3]+names[j,4]+names[j,5]+names[j,6]+names[j,7]+names[j,8]+names[j,9]
    species_name.append(name.strip())

  abundance = np.zeros(len(pressure))
  abundance_h2 = abundances[imol('H2',species_name),:]
  abundance_he = abundances[imol('He',species_name),:]

  # Loop over molecules, calculate and print column density
  for sp in species:
    molmass = get_molmass(sp)
    abundance = abundances[imol(sp,species_name),:]
    sigma = calc_column_density_atmo(sp,abundance,gravity,pressure,abundance_h2,abundance_he)
    print sp,' column density: ', sigma
	
