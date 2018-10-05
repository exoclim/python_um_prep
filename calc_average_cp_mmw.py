# Python routine to calculate the average mean molecular weight and heat capacity 
# from an ATMO chemistry output file 
# NOTE: the chemistry file needs to contain the heat capacity!!

# Import some modules
import pylab
import read_atmo_chem as rac

def calc_straight_avg(fname):

  # Read atmo chemistry file to get pressure, cp and mean molecular weight
  pressure, cp, mmw = rac.read_atmo_chem_cpmmw(fname)

  # Get number of levels
  nlev = pressure.size

  # Compute straight average
  avg_cp  = sum(cp)/nlev
  avg_mmw = sum(mmw)/nlev

  # Print results to screen
  print 'Column average quantities (straight average):'
  print '  Specific Heat Capacity: ',avg_cp*1E-7*1E3, 'J/kg/K'
  print '  Molar Heat Capacity: ',avg_cp*1E-7*avg_mmw,      'J/mol/K'
  print '  Mean Molecular Weight: ',avg_mmw     ,'g/mol'
  print '  Specific Gas Constant: ',8.3144598/avg_mmw*1E3, 'J/kg/K'




