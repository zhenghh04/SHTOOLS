import numpy as _np


def cross_spectrum(clm1, clm2, normalization='4pi', degrees=None, lmax=None,
                   convention='power', unit='per_l', base=10.):
    """
    Return the cross-spectrum of the spherical harmonic coefficients as a
    function of spherical harmonic degree.

    Usage
    -----
    array = cross_spectrum(clm1, clm2, [normalization, degrees, lmax,
                                        convention, unit, base])

    Returns
    -------
    array : ndarray, shape (len(degrees))
        1-D ndarray of the spectrum.

    Parameters
    ----------
    clm1 : ndarray, shape (2, lmax + 1, lmax + 1)
        ndarray containing the first set of spherical harmonic coefficients.
    clm2 : ndarray, shape (2, lmax + 1, lmax + 1)
        ndarray containing the second set of spherical harmonic coefficients.
    normalization : str, optional, default = '4pi'
        '4pi', 'ortho' or 'schmidt' for geodesy 4pi normalized,
        orthonormalized, or Schmidt semi-normalized coefficients, respectively.
    lmax : int, optional, default = len(clm[0,:,0]) - 1.
        Maximum spherical harmonic degree to output.
    degrees : ndarray, optional, default = numpy.arange(lmax+1)
        Array containing the spherical harmonic degrees where the spectrum
        is computed.
    convention : str, optional, default = 'power'
        The type of spectrum to return: 'power' for power spectrum, 'energy'
        for energy spectrum, and 'l2norm' for the l2 norm spectrum.
    unit : str, optional, default = 'per_l'
        If 'per_l', return the total contribution to the spectrum for each
        spherical harmonic degree l. If 'per_lm', return the average
        contribution to the spectrum for each coefficient at spherical
        harmonic degree l. If 'per_dlogl', return the spectrum per log
        interval dlog_a(l).
    base : float, optional, default = 10.
        The logarithm base when calculating the 'per_dlogl' spectrum.

    Description
    -----------
    This function returns either the cross-power spectrum, cross-energy
    spectrum, or l2-cross-norm spectrum. Total cross-power is defined as the
    integral of the clm1 times the conjugate of clm2 over all space, divided
    by the area the functions span. If the mean of the functions is zero,
    this is equivalent to the covariance of the two functions. The total
    cross-energy is the integral of clm1 times the conjugate of clm2 over all
    space and is 4pi times the total power. The l2-cross-norm is the
    sum of clm1 times the conjugate of clm2 over all angular orders as a
    function of spherical harmonic degree.

    The output spectrum can be expresed using one of three units. 'per_l'
    returns the contribution to the total spectrum from all angular orders
    at degree l. 'per_lm' returns the average contribution to the total
    spectrum from a single coefficient at degree l. The 'per_lm' spectrum
    is equal to the 'per_l' spectrum divided by (2l+1). 'per_dlogl' returns
    the contribution to the total spectrum from all angular orders over an
    infinitessimal logarithmic degree band. The contrubution in the band
    dlog_a(l) is spectrum(l, 'per_dlogl')*dlog_a(l), where a is the base,
    and where spectrum(l, 'per_dlogl) is equal to
    spectrum(l, 'per_l')*l*log(a).
    """
    if lmax is None:
        lmax = len(clm1[0, :, 0]) - 1

    if (degrees is None):
        degrees = _np.arange(lmax+1)

    if _np.iscomplexobj(clm1) is not _np.iscomplexobj(clm2):
        raise ValueError('clm1 and clm2 must both be either real or ' +
                         'complex. \nclm1 is complex : {:s}\n'
                         .format(repr(_np.iscomplexobj(clm1))) +
                         'clm2 is complex : {:s}'
                         .format(repr(_np.iscomplexobj(clm2))))

    ndegrees = len(degrees)
    if _np.iscomplexobj(clm1):
        array = _np.empty(ndegrees, dtype='complex')
    else:
        array = _np.empty(ndegrees)

    # First compute l2norm, and then convert to the required normalization
    if _np.iscomplexobj(clm1):
        for i, l in enumerate(degrees):
            array[i] = (clm1[0, l, 0:l + 1] *
                        clm2[0, l, 0:l + 1].conjugate()).sum() + \
                       (clm1[1, l, 1:l + 1] *
                        clm2[1, l, 1:l + 1].conjugate()).sum()
    else:
        for i, l in enumerate(degrees):
            array[i] = (clm1[0, l, 0:l + 1] * clm2[0, l, 0:l + 1]).sum() \
                       + (clm1[1, l, 1:l + 1] * clm2[1, l, 1:l + 1]).sum()

    if convention.lower() == 'l2norm':
        pass
    elif convention.lower() in ('power', 'energy'):
        if normalization == '4pi':
            pass
        elif normalization == 'schmidt':
            array /= (2.0 * degrees + 1.0)
        elif normalization == 'ortho':
            array /= (4.0 * _np.pi)
        else:
            raise ValueError(
                "normalization must be '4pi', 'ortho', or 'schmidt'. " +
                "Input value was {:s}".format(repr(normalization)))
    else:
        raise ValueError(
            "convention must be 'power', 'energy', or 'l2norm'. " +
            "Input value was {:s}".format(repr(convention)))

    if convention.lower() == 'energy':
        array *= 4.0 * _np.pi

    if unit.lower() == 'per_l':
        pass
    elif unit.lower() == 'per_lm':
        array /= (2.0 * degrees + 1.0)
    elif unit.lower() == 'per_dlogl':
        array *= degrees * _np.log(base)
    else:
        raise ValueError(
            "unit must be 'per_l', 'per_lm', or 'per_dlogl'." +
            "Input value was {:s}".format(repr(unit)))

    return array
