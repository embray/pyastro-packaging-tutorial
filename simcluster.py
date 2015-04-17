#!/usr/bin/env python

import argparse  # We added a new import statement for argarse
import sys       # Also import sys for sys.argv

import numpy as np
import astropy.io.fits as fits
from astropy.convolution import Gaussian2DKernel, convolve_fft


def simulated_cluster(n_stars=10000, dimensions=(512, 512)):
    """
    Generates an image simulating a cluster of stars, including
    a Gaussian filter and background noise.

    Parameters
    ----------
    n_stars : `int`
        A positive integer giving the number of visible stars in the image
        (default: 10000).

    dimensions : `tuple`
        A two-tuple of positive integers specifying the dimensions (in pixels)
        of the output image (default: 512x512).

    Returns
    -------
    array : `~numpy.ndarray`
        A 2D Numpy array containing the pixels of the generated image.
    """

    nx, ny = dimensions

    # Create empty image
    image = np.zeros((ny, nx))

    # Generate random positions
    r = np.random.random(n_stars) * nx
    theta = np.random.uniform(0., 2. * np.pi, n_stars)

    # Generate random fluxes
    fluxes = np.random.random(n_stars) ** 2

    # Compute position
    x = nx / 2 + r * np.cos(theta)
    y = ny / 2 + r * np.sin(theta)

    # Add stars to image
    # ==> First for loop and if statement <==
    for idx in range(n_stars):
        if x[idx] >= 0 and x[idx] < nx and y[idx] >= 0 and y[idx] < ny:
            image[y[idx], x[idx]] += fluxes[idx]

    # Convolve with a gaussian
    kernel = Gaussian2DKernel(stddev=1)
    image = convolve_fft(image, kernel)

    # Add noise
    image += np.random.normal(1., 0.001, image.shape)

    return image


def main(argv=None):
    """Main function for the simcluster.py script."""

    # Create an ArgumentParser--a special object that keeps track of all the
    # arguments we want our script to be able to handle, and then implements parsing
    # them from sys.argv
    parser = argparse.ArgumentParser(description="Generates simulated images of clusters")

    # Add an optional argument for # of stars (default=10000)
    parser.add_argument('-s', '--stars', type=int, default=10000,
                        help='the number of stars to generate')

    # Add the x and y arguments
    parser.add_argument('-x', type=int, default=512,
                        help='the x dimension (in pixels) of the image')
    parser.add_argument('-y', type=int, default=512,
                        help='the y dimension (in pixels) of the image')

    # Add an argument to handle the output file.  If we use argparse.FileType it will
    # handle opening a writeable file (and ensuring we can write to it).
    # Note that the argument name 'file' does not beging with a '-' or '--'; this indicates
    # to argparse that it is a *positional* argument
    parser.add_argument('file', type=argparse.FileType('w'),
                        help='the name of the output file')

    args = parser.parse_args(argv)

    image = simulated_cluster(n_stars=args.stars, dimensions=(args.x, args.y))

    # Write to a FITS file
    # For now the file writing is simple enough that we leave it in the main() function; in the future
    # we may want to break this out into its own routine that takes a filename and the image array
    # (and any other relevant options) and handles the writing
    fits.writeto(args.file, image, clobber=True)


if __name__ == '__main__':
    main(sys.argv[1:])
