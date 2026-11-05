#!/usr/bin/env python3
"""View a FITS image, or export it as a PNG.

    python3 view_fits.py                       # interactive window
    python3 view_fits.py --save out.png        # full-resolution PNG, no window
    python3 view_fits.py --vmin 3380 --vmax 3700

The stretch only affects how the image is displayed. Pixel values shown under
the cursor are the original counts from the file.
"""
import argparse

from astropy.io import fits
from astropy.visualization import AsinhStretch, ImageNormalize
import matplotlib.pyplot as plt
import numpy as np


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("path", nargs="?", default="Fits_Data/mosaic.fits")
    parser.add_argument("--save", metavar="PNG", help="write a PNG and exit")
    parser.add_argument("--vmin", type=float, help="counts shown as black (default: 1st percentile)")
    parser.add_argument("--vmax", type=float, help="counts shown as white (default: 99th percentile)")
    args = parser.parse_args()

    data = fits.getdata(args.path)
    low, high = np.percentile(data, [1, 99])
    vmin = low if args.vmin is None else args.vmin
    vmax = high if args.vmax is None else args.vmax
    norm = ImageNormalize(vmin=vmin, vmax=vmax, stretch=AsinhStretch(0.05), clip=True)
    print(f"{args.path}: {data.shape[1]} x {data.shape[0]} px, display range {vmin:.0f} to {vmax:.0f} counts")

    if args.save:
        # imsave writes one image pixel per PNG pixel, with no axes or resampling.
        plt.imsave(args.save, norm(data), cmap="gray", vmin=0, vmax=1, origin="lower")
        print(f"saved {args.save}")
        return

    fig, ax = plt.subplots(figsize=(7, 10))
    im = ax.imshow(data, cmap="gray", norm=norm, origin="lower", interpolation="nearest")
    ax.set(title=args.path, xlabel="x (px)", ylabel="y (px)")
    fig.colorbar(im, ax=ax, label="counts", shrink=0.8)
    plt.show()


if __name__ == "__main__":
    main()
