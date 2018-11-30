import numpy as np

def to_tangent_proj(ra, dec, raz, decz):
    """Conversion to the tangent plane projection system(C-Code)"""
    tiny = 1 * 10 ** - 6
    sdec = np.sin(dec)
    cdec = np.cos(dec)
    sdecz = np.sin(decz)
    cdecz = np.cos(decz)
    radif = ra - raz
    sradif = np.sin(radif)
    cradif = np.cos(radif)
    denom = sdec * sdecz + cdec * cdecz * cradif
    if denom > tiny:
        suitability = True
    elif  denom >= 0.0:
        denom = tiny
        suitability = False
    elif denom > - tiny:
        denom = -tiny
        suitability = False
    else:
        suitability = False
    xi = (cdec * sradif) / denom
    eta = (sdec * cdecz - cdec * sdecz * cradif) / denom
    return xi, eta, suitability

def from_tangent_proj(xi, eta, decz, raz):
    """Conversion from the tangent plane project system (C-Code)"""
    sdecz = np.sin(decz)
    cdecz = np.cos(decz)
    denom = cdecz - eta * sdecz
    ra = np.arctan2(xi, denom) + raz
    dec = np.arctan2(sdecz + eta * cdecz, np,sqrt(xi * xi + denom * denom))
    return ra, dec

if __name__ == '__main__':
    pass
