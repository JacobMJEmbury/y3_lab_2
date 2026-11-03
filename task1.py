from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt

hdulist = fits.open("/Users/jacobembury/Downloads/Astro/Fits_Data/mosaic.fits")

# Get the header data (MAGZPT - this is the only thing we really need - instramental zero point)
print(hdulist[0].header)

# Get the data itself
print(hdulist[0].data)

# Flattern the data so we are just printing the pixel values
flatterned_data = np.ndarray.flatten(hdulist[0].data)

# Plot a histogram with 1000 bins... 
plt.hist(flatterned_data, bins=1000, range=(3000,4000))
plt.show()

# We see a gaussian about 3418 - longer tailed on the RHS (higher pixel values)
# HOWEVER: at 3422 we see a very large bin - that is superposed ontop of the gaussian shape...

# The peak of the guassian represents the average background counts of the image
# The spread of the guassian represents the average noise of the image
# The longer tail on the right is actually the astronomical objects we want to see - higher intensity objects

# Probably need to be at least 3sig to get outside of the range of random noise from the background
