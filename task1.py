from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt

hdulist = fits.open("Astro/Fits_Data/mosaic.fits")

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

# FIND BRIGHT SPOTS:
img_data = hdulist[0].data

#print("Length of image data:" + str(len(img_data[:, 0])))
#print("Length of image data:" + str(len(img_data[0, :])))

rows, cols = len(img_data), len(img_data[0, :])
mask = np.zeros((rows, cols))
masked_img_data = img_data + mask

'''
# Very inefficient - could probs just use argmax for numpy and acheieve the same thing in O1 time... so maybe just do that... Instead of On**2

for bright in range(0, 100):
    brightest=0
    brightest_coords=[0,0]
    for row in range(10, rows):
        for col in range(0, cols):
            if (masked_img_data[row, col] > brightest):
                brightest = masked_img_data[row, col]
                brightest_coords = [row, col]
    
    print(str(brightest) + "||||" + str(brightest_coords))
    mask[brightest_coords[0], brightest_coords[1]] = mask[brightest_coords[0], brightest_coords[1]] + brightest
    masked_img_data = masked_img_data - mask
'''

# Produces the top 100 most intense points in the img
for count in range(10000):
    row, col = np.unravel_index(np.argmax(masked_img_data), masked_img_data.shape)
    print(str(masked_img_data[row, col]) + " |||| (" + str(col) + "," + str(row) + ")")
    mask[row, col] = mask[row, col] + masked_img_data[row, col]
    masked_img_data = masked_img_data - mask




# CLAUDE HERE:

# Astro/view_fits.py turns mosaic.fits into the black and white PNG. To remake it:
#   cd Astro && python view_fits.py --save Fits_Data/mosaic.png
# PNG row 0 is the top of the image but FITS row 0 is the bottom, so flip it to line up with the mask.
overlay = plt.imread("Astro/Fits_Data/mosaic.png")[::-1].copy()

# Draw a red dot on every pixel in the mask. Bigger than 1 px so they still show when zoomed out.
dot_radius = 3
for row, col in zip(*np.nonzero(mask)):
    overlay[max(row - dot_radius, 0):row + dot_radius + 1,
            max(col - dot_radius, 0):col + dot_radius + 1, :3] = [1, 0, 0]

plt.imsave("Astro/Fits_Data/mosaic_masked.png", overlay, origin="lower")
print("Saved Astro/Fits_Data/mosaic_masked.png")
