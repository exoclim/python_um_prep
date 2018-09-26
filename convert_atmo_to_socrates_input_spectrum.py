# Python script to convert an ATMO format irradiation file to
# a text file in the correct format to be read by  socrates routines 

#Import some modules
import netCDF4 as nc

def write_um_spec(fname=None,
fname_out=None,
star_name=None,
source=None):

  # Check all required inputs are defined
  if fname==None:
    print 'Error: fname is not defined'
    exit()
  if fname_out==None:
    print 'Error: fname_out is not defined'
    exit()
  if star_name==None:
    print 'Error: star_name is not defined'
    exit()
  if source==None:
    print 'Error: source is not defined'
    print 'e.g. "Phoenix BT-Settl"'
    exit() 

  # Read in input ATMO spectrum
  data = nc.Dataset(fname,'r')
  # Wavenumber
  nu = data.variables['nu'][:]
  # Spectral irradiance
  hnu = data.variables['hnu'][:]

  # Convert nu to wavelength (m)
  wl = 1./nu
  wl = wl*1e-2

  # Convert spectral irradiance to per wavelength
  hnu = hnu*nu**2.

  # Invert arrays
  hnu = hnu[::-1]
  wl  = wl[::-1]

  # Write to text file
  f = open(fname_out,'w')
  f.write(source+' spectrum for '+star_name+'\n')
  f.write('  Wavelength     Irradiance\n')
  f.write('       (m)        (erg/s/cm/star)\n')
  f.write('*BEGIN_DATA\n')
  for l in range(len(nu)):
    wl_str = str.format("{0:" ">12.6e}",wl[l])
    hnu_str = str.format("{0:" ">12.6e}",hnu[l])
    f.write('     ' + wl_str + '     ' + hnu_str + '\n')

  f.write('*END')
  f.close()


