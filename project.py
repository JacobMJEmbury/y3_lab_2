#### POSSIBLE IDEA FOR PROJECT:
###############################

# Could you not map a continuous f(x,y) onto the image (like a spline) and then determine the rate of change for any of the contours where the star is?
# -> Effectively could you not solve for the local and global maximums of this function to then solve for the functions themselves?
# -> You then convolve with a smoothing function like a guassian for each of these functions to get rid of pixel-by-pixel artifacts
# -> You then can find a regular functional profile for these galaxies - and classify much better...
# -> Use this method not for the whole plane (would be inefficient) - you just do this calc for the pixels around the point - it can then determine and differentiate between a single pixel and a full galaxy...
