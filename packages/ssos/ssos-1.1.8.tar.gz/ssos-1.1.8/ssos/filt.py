'''
    Python implementations of filter functions to detect SSOs in SExtractor and SCAMP catalogs.

    Part of the SSO recovery pipeline.
'''

import collections

import numpy as np
import pandas as pd
from statsmodels import robust
from scipy import stats
from scipy.optimize import curve_fit


def detections(sources, settings):
    '''
        Remove sources based on number of detections

        input
        ------
        sources - pandas dataframe, table of source data
        detections - list, containing integers responding to number of detections

        return
        ------
        sources - pandas dataframe, sources data without the sources filtered in this step
    '''
    measurements = collections.Counter(sources['SOURCE_NUMBER'])
    sources_to_remove = {key for key, value in measurements.items()
                         if value in settings['DETECTIONS']}

    sources = sources[~sources['SOURCE_NUMBER'].isin(sources_to_remove)]
    return sources


def proper_motion(sources, settings):
    '''
    Remove sources based on the proper motion range and signal-to-noise

    input
    ------
    sources - pandas dataframe, SCAMP full catalog
    settings - dictionary, settings parameter:value pairs

    return
    ------
    sources - pandas dataframe, sources data without the sources filtered in this step
    '''

    pm_low = settings['PM_LOW']
    pm_up = settings['PM_UP']
    SN = settings['PM_SNR']

    # Filter sources for proper motion range
    sources = sources[(sources.PM > pm_low) & (sources.PM < pm_up)]

    # Filter by proper motion SN
    sources = sources[sources.PM / sources.PMERR > SN]
    return sources


def pixel(sources, settings):
    '''
    Remove sources based on pixel coordinates

    input
    ------
    sources - pandas dataframe, SCAMP full catalog
    settings - dictionary, contains the specified filter parameters

    return
    ------
    sources - pandas dataframe, sources data without the sources filtered in this step
    '''

    delta_pixel = settings['DELTA_PIXEL']

    # For all sources, check if the largest XWIN_IMAGE !and! YWIN_IMAGE differences
    # are smaller than delta_pixel.
    for source_number, group in sources.copy().groupby('SOURCE_NUMBER'):

        x_img = group['XWIN_IMAGE']
        y_img = group['YWIN_IMAGE']

        if x_img.max() - x_img.min() < delta_pixel:
            if y_img.max() - y_img.min() < delta_pixel:
                sources = sources[sources.SOURCE_NUMBER != source_number]

    return sources


def calc_r_squared(y_fit, y_data):
    '''
    Calculates the r-squared fit parameter to verify the linear motion

    input
    ------
    y_fit - list, values of fit function
    y_data - list, data points

    return
    ------
    r_squared - float, between 0 and 1
    '''

    residuals = y_data - y_fit
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y_data-np.mean(y_data))**2)

    r_squared = 1 - (ss_res / ss_tot)
    return r_squared


def linear_function(x, m, n):
    return x*m + n


def motion_is_linear(epoch, dim, dimerr, r_squared):
    '''
    Motion fitting function

    input
    ------
    epoch - np.array, epoch of source
    ra - pd.Series, right ascension of source
    dec - pd.Series, declination of source
    r_squared - float, minimum r_squared for good fit

    return
    ------
    True if motion is linear else False
    '''

    coords = dim.values
    sigma = dimerr.values

    try:
        popt, pcov = curve_fit(linear_function, epoch, coords, sigma=sigma, absolute_sigma=True)
    except RuntimeError:
        return False # If fit does not converge, discard this source

    fitted_r_squared = calc_r_squared(linear_function(epoch, *popt), coords)

    if fitted_r_squared >= r_squared:
        return True
    else:
        return False


def linear_motion(sources, settings):
    '''
        Remove sources based on linearity of motion and the Median Absolute Deviation

        input
        ------
        sources - pandas dataframe, table of source data
        settings - dict, 'parameter': value

        return
        ------
        sources - pandas dataframe, sources data without the sources filtered in this step
    '''

    r_squ, out_thres, id_out = settings['R_SQU_M'], settings['OUTLIER_THRESHOLD'],\
                               settings['IDENTIFY_OUTLIER']

     # Lower limit of subgroup size
    min_detections = 3

    sources_to_remove = []

    for source_number, group in sources.copy().groupby('SOURCE_NUMBER'):
        # GROUP contains the detections of a single source
        epoch = group['EPOCH'].values

        if id_out:
            # Detect outliers using the Median Absolute Deviation of the EPOCHS
            outlier_index = np.where(abs(np.diff(epoch)) > robust.mad(epoch) *
                                                           out_thres)[0]
            if len(outlier_index)  == 0:  # no outlier in EPOCH. Check edges
                outlier_in_middle =  np.where(abs(np.diff(epoch[:-1])) > robust.mad(epoch[:-1]) *
                                                                         out_thres)[0]
                if len(outlier_in_middle) == 0:
                    for dim, dimerr in [(group['ALPHA_J2000'], group['ERRA_WORLD']),
                                        (group['DELTA_J2000'], group['ERRB_WORLD'])]:
                        if not motion_is_linear(epoch, dim, dimerr, r_squ):
                            sources_to_remove.append(source_number)
                            break
                    continue

                else: # outlier found in middle (jump in epochs)
                    outlier_index = outlier_in_middle

            # Found outlier in EPOCH
            subgroups = np.split(group[['EPOCH', 'ALPHA_J2000', 'DELTA_J2000',
                                        'ERRA_WORLD', 'ERRB_WORLD']], outlier_index + 1)

            for subgroup in subgroups:

                if len(subgroup) < min_detections: # if there aren't sufficient detections
                    sources.loc[subgroup.index, 'FLAGS_SSOS'] +=1  # Add outlier flag

                else:
                    epochs = subgroup['EPOCH']
                    for dim, dimerr in [(subgroup['ALPHA_J2000'], subgroup['ERRA_WORLD']),
                                        (subgroup['DELTA_J2000'], subgroup['ERRB_WORLD'])]:
                        if not motion_is_linear(epochs, dim, dimerr, r_squ):
                            sources.loc[subgroup.index, 'FLAGS_SSOS'] +=1  # Add outlier flag
                            break

            # FLAG_SSOS is only uneven if detection is outlier
            if all(sources[sources.SOURCE_NUMBER == source_number]['FLAGS_SSOS'] % 2 == 1):
                sources_to_remove.append(source_number)

        else:
            for dim, dimerr in [(group['ALPHA_J2000'], group['ERRA_WORLD']),
                                (group['DELTA_J2000'], group['ERRB_WORLD'])]:
                if not motion_is_linear(epoch, dim, dimerr, r_squ):
                    sources_to_remove.append(source_number)
                    break

    sources = sources[~sources.SOURCE_NUMBER.isin(sources_to_remove)]
    return sources


def compare_std_and_sigma_of_average(y, sigma):
    ''' Compares weighted average uncertainty to standard deviation '''

    weights = 1 / sigma**2
    weighted_average_uncertainty = 1 / np.sqrt(np.sum(weights))
    standard_deviation_of_data = np.std(y)
    ratio = weighted_average_uncertainty / standard_deviation_of_data

    return ratio


def constant_trail(sources, settings):
    '''
    Remove sources based on constant trail size

    input
    ------
    sources - pd.DataFrame, source data
    settings - dict, 'parameter': value

    return
    ------
    sources - pandas dataframe, sources data without the sources filtered in this step
    '''

    ratio = settings['RATIO']

    for source_number, group in sources.copy().groupby('SOURCE_NUMBER'):

        awin = group['AWIN_IMAGE']
        bwin = group['BWIN_IMAGE']

        for i, dimension in enumerate([awin, bwin]):

            sigma = group['ERRAWIN_IMAGE'] if i == 0 else group['ERRBWIN_IMAGE']

            fitted_ratio = compare_std_and_sigma_of_average(dimension, sigma)

            if fitted_ratio >= ratio and i == 0:
                pass
            elif fitted_ratio >= ratio and i == 1:
                pass
            else:
                sources = sources[sources.SOURCE_NUMBER != source_number]

    return sources


def trail_distribution(sources, settings):
    '''

    ####
    DEPRECTATED - Use the stellar catalogue filter instead.
    ####

    Remove sources based on distribution of size parameters

    input
    ------
    sources - pandas dataframe, table of source data
    settings - dict, 'parameter': value

    return
    ------
    sources - pandas dataframe, sources data without the sources filtered in this step
    '''

    sigma = settings['SIGMA']
    a = sources['AWIN_IMAGE']
    b = sources['BWIN_IMAGE']
    mu_a, std_a = np.mean(a), np.std(a)
    mu_b, std_b = np.mean(b), np.std(b)

    # Check if for any source any AWIN or BWIN value outside mu + sigma * std
    for source_number, group in sources.copy().groupby('SOURCE_NUMBER'):
        if any(group['AWIN_IMAGE'] > mu_a + sigma * std_a):
            sources = sources[sources.SOURCE_NUMBER != source_number]
        if any(group['BWIN_IMAGE'] > mu_b + sigma * std_b):
            sources = sources[sources.SOURCE_NUMBER != source_number]

    return sources


def star_catalog(sources, settings):
    '''
        Remove sources based on proximity to stars. Requires the HYG stellar
        catalog.

        input
        ------
        sources - pandas dataframe, table of source data
        settings - dict, 'parameter': value

        return
        ------
        sources - pandas dataframe, sources data without the sources filtered in this step
    '''

    distance = settings['DISTANCE'] / 3600 # convert distance to degree

    # -----
    # Open the HYG catalog
    stars = pd.read_csv(settings['HYGCAT'])
    stars['ra'] *= 15    # Convert RA coordinates in the HYG catalog from decimal hours to degrees

    # Remove stars which are outside region of interest, given by the minimum and maximum
    # RA and Dec values of the source candiates plus the distance of the stellar regions
    upper_ra, lower_ra = (sources['ALPHA_J2000'].max() + distance,
                          sources['ALPHA_J2000'].min() - distance)
    upper_dec, lower_dec = (sources['DELTA_J2000'].max() + distance,
                            sources['DELTA_J2000'].min() - distance)

    stars = stars[(stars['ra'] > lower_ra) &\
                  (stars['ra'] < upper_ra)]
    stars = stars[(stars['dec'] > lower_dec) &\
                  (stars['dec'] < upper_dec)]

    for source_number, group in sources.copy().groupby('SOURCE_NUMBER'):

            mean_ra = np.mean(group['ALPHA_J2000'])
            mean_dec = np.mean(group['DELTA_J2000'])

            try:
                min_distance_to_star = min(np.sqrt((stars['ra'] - mean_ra)**2 +
                                                   (stars['dec'] - mean_dec)**2).abs())

            except ValueError:  # reports "min() arg is an empty sequence"
                continue

            if min_distance_to_star < distance:
                sources = sources[sources.SOURCE_NUMBER != source_number]

    return sources
