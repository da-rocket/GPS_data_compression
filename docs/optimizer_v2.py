import os
from os import listdir
import csv
import math
from geographiclib.geodesic import Geodesic
from tkinter.messagebox import showinfo, showerror

# general configuration
try:
    import config
    cfgs = config.__dict__
except Exception as e:                                      # define in client app directory
    print(e)

# main control
def manager(optInDir, switch, statsDir, compsDir):
    stop = int(cfgs['end'] / cfgs['step'])  # number of iterations for length optimization
    for tracks in fileReaderOpt(optInDir):
        if switch == 0:     # 0-application; 1-calibration
            fdir = compsDir
            if cfgs['appByLen'] and cfgs['appByAlt'] and cfgs['appBySpd']:
                """application for length att"""
                byLen = onLengthOptimize(tracks, cfgs['devByAng'], 0, switch)

                """application for altitude attribute"""
                min_alt = math.floor(getMin(tracks, 'altIdx'))
                max_alt = math.ceil(getMax(tracks, 'altIdx'))
                range_alt = max_alt - min_alt
                width_alt = range_alt / cfgs['hNumClasses']
                byAlt = onAltitudeOptimize(tracks, min_alt, width_alt, cfgs['hNumClasses'], switch)

                """application for speed attribute"""
                min_speed = getMin(tracks, 'speedIdx')
                max_speed = getMax(tracks, 'speedIdx')
                range_speed = max_speed - min_speed
                width_speed = range_speed / cfgs['spd_NumClasses']
                bySpd = onSpeedOptimize(tracks, min_speed, width_speed, cfgs['spd_NumClasses'], switch)

                """combine lists together, remove duplicates and sort them in order"""
                aggSeq = (byLen + byAlt + bySpd)
                cleanSeq = list(dict.fromkeys(aggSeq))
                cleanSeq.sort()
                compTrack = [tracks[index] for index in cleanSeq]
                fileWriter(fdir, compTrack, switch)

        else:
            fdir = statsDir
            if cfgs['calByLen']:
                iter_num = [(round(x * cfgs['step'], 1), x) for x in range(cfgs['start'], stop)]
                for (devByAng, x) in iter_num:
                    calByLenRec = onLengthOptimize(tracks, devByAng, x, switch)
                    fileWriter(fdir, calByLenRec, 1)

            if cfgs['calByAlt']:
                min_alt = math.floor(getMin(tracks, 'altIdx'))
                max_alt = math.ceil(getMax(tracks, 'altIdx'))
                range_alt = max_alt - min_alt
                qty_alts = [i for i in range(cfgs['hstart'], cfgs['hstop'])]
                for qty_alt in qty_alts:
                    width_alt = range_alt / qty_alt
                    calByAltRec = onAltitudeOptimize(tracks, min_alt, width_alt, qty_alt, switch)
                    fileWriter(fdir, calByAltRec, 1)

            if cfgs['calBySpd']:
                min_speed = getMin(tracks, 'speedIdx')
                max_speed = getMax(tracks, 'speedIdx')
                range_speed = max_speed - min_speed
                qty_speeds = [i for i in range(cfgs['spd_start'], cfgs['spd_stop'])]
                for qty_speed in qty_speeds:
                    width_speed = range_speed / qty_speed
                    calBySpeedRec = onSpeedOptimize(tracks, min_speed, width_speed, qty_speed, switch)
                    fileWriter(fdir, calBySpeedRec, 1)

            if cfgs['calByLen'] and cfgs['calByAlt'] and cfgs['calBySpd']:
                pass
                # show message: not implemented

# def fileReader(optInDir):     # function to read clean tracks
def fileReaderOpt(cleanDir):  # function to read clean tracks
    for filename in listdir(cleanDir):
        if filename.endswith('.csv'):
            fpath = os.path.join(cleanDir, filename)
            tracks = []    # read individual paths
            with open(fpath, newline='') as f:
                for line in f:
                    line = line.strip().split(',')
                    pntGroup  = line[cfgs['groupIdx']]
                    pntUnit   = line[cfgs['unitIdx']]
                    pntDate   = line[cfgs['dateIdx']]
                    pntTime   = line[cfgs['timeIdx']]
                    pntLat    = float(line[cfgs['latIdx']])
                    pntLong   = float(line[cfgs['longIdx']])
                    pntAlt    = float(line[cfgs['altIdx']])
                    pntSpeed  = float(line[cfgs['speedIdx']])
                    pntSec    = line[cfgs['secsIdx']]
                    pntTrack  = line[cfgs['trackIdx']]
                    pntSeq    = int(line[cfgs['seqIdx']])
                    tracks.append([pntGroup, pntUnit, pntDate, pntTime, pntLat, pntLong, pntAlt, pntSpeed,
                                 pntSec, pntTrack, pntSeq])
            yield tracks

def fileWriterOpt(ftext, fdir, name, params):
    if params['runmode'] == 0:                      # used for application
        fname = name + '.csv'
        fpath = os.path.join(fdir, fname)
        with open(fpath, 'a', newline='') as f:     # write files
            writer = csv.writer(f)
            writer.writerows(ftext)
    elif params['runmode'] == 1:
        fname = name + '.csv'
        fpath = os.path.join(fdir, fname)
        with open(fpath, 'a', newline='') as f:     # write files
            writer = csv.writer(f)
            writer.writerows(ftext)
    else:
        showinfo('GPS Optimizer', 'Option not available')

def azimuth(lat1, lon1, lat2, lon2, rmode='both'):
    res = Geodesic.WGS84.Inverse(lat1, lon1, lat2, lon2)
    ang, s12 = res['azi1'], res['s12']
    if rmode == 'both':
        if ang < 0:
            ang += 360
        return ang, s12
    else:
        return s12

def reachByLen(devByAng, params):
    rad = (devByAng * math.pi) / 180.0 # convert deg to rad
    len = params['devByCathetus'] / math.tan(rad)
    return len

def getTrackLength(byLength):
    LatLong = [(x[cfgs['lenLatIdx']], x[cfgs['lenLongIdx']]) for x in byLength]
    s12 = 0.0
    for (lat, long) in LatLong:
        if LatLong.index((lat, long)) == 0:     # first record
            lat1, long1 = lat, long
        else:
            lat2, long2 = lat, long
            s12 += azimuth(lat1, long1, lat2, long2, 'dist') # ask to return distance only
            lat1, long1 = lat2, long2
    return s12

# def onLengthOptimize(tracks, devByAng, iter, switch): # add parameter for calibration
def onLengthOptimize(tracks, devByAng, iter, params):  # add parameter for calibration
    byLength = []
    init = True
    devByLen    = reachByLen(devByAng, params)
    trackId     = tracks[0][cfgs['groupIdx']] + '_' + \
                  tracks[0][cfgs['unitIdx']] + '_' + \
                  tracks[0][cfgs['trackIdx']]
    lat1        = tracks[0][cfgs['latIdx']]
    lon1        = tracks[0][cfgs['longIdx']]
    seq1        = tracks[0][cfgs['seqIdx']]
    calibIter   = iter
    byLength.append([lat1, lon1, seq1, trackId])
    for line in tracks[1:]:
        lat2 = line[cfgs['latIdx']]
        lon2 = line[cfgs['longIdx']]
        seq2 = line[cfgs['seqIdx']]
        azi, s12 = azimuth(lat1, lon1, lat2, lon2)
        if init:
            azi_init = azi
            byLength.append([lat2, lon2, seq2, trackId])
            init = False
        else:
            diff = abs(azi - azi_init)
            if diff < devByAng and s12 < devByLen:
                del byLength[len(byLength)-1]
                byLength.append([lat2, lon2, seq2, trackId])
            else:
                lat1 = byLength[len(byLength)-1][0]
                lon1 = byLength[len(byLength)-1][1]
                azi_init, s12 = azimuth(lat1, lon1, lat2, lon2)
                byLength.append([lat2, lon2, seq2, trackId])
    #
    if params['runmode'] == 0:     # 0-application; 1-calibration
        appLen =[]
        for line in byLength:
            appLen.append(line[2])  # return sequence
        return appLen
    elif params['runmode'] == 1:
        calibStr = []
        calibRec = len(byLength)
        calibLen = getTrackLength(byLength)
        calibStr.append([calibIter, trackId, devByAng, calibRec, calibLen])
        return calibStr
    else:
        showerror('GPS Optimizer', 'Option is not available')

def getMax(tracks, idx):
    return max([i[cfgs[idx]] for i in tracks])

def getMin(tracks, idx):
    return min([i[cfgs[idx]] for i in tracks])

def frange(start, stop=None, step=None):
    """
    create float range using start, end and width
    """
    if stop == None:
        stop = start + 0.0
        start = 0.0
    if step == None:
        step = 1.0
    while True:
        if step > 0 and start >= stop:
            break
        elif step < 0 and start <= stop:
            break
        yield start
        start = start + step

def create_bins(lower_bound, width, qty):
    """ create_bins returns an equal-width (distance) partitioning.
        It returns an ascending list of tuples, representing the intervals.
    """
    bins = []
    upper_bound = lower_bound + (width * qty)
    for low in frange(lower_bound, upper_bound, width):
        bins.append((low, low + width))
    return bins

def find_bins(value, bins):
    """ bins is a list of tuples, like [(0,20), (20, 40), (40, 60)],
            binning returns the smallest index i of bins so that
            bin[i][0] <= value < bin[i][1]
    """
    for i in range(0, len(bins)):
        if bins[i][0] <= value < bins[i][1]:
            return i
    return len(bins)-1    # handle exception for speed, when value = max(v)

def onAltitudeOptimize(tracks, min_alt, width_alt, qty_alt, params):
    """
    for every interval, collect start and end points for altitude attribute
    """
    byAltitude = []
    bins = create_bins(min_alt, width_alt, qty_alt)

    trackId = tracks[0][cfgs['groupIdx']] + '_' + \
              tracks[0][cfgs['unitIdx']] + '_' + \
              tracks[0][cfgs['trackIdx']]

    counter = 0
    """
    for line in tracks:        
        # for every interval, collect start and end points for altitude attribute    
        alt = float(line[cfgs['altIdx']])
        seq = line[cfgs['seqIdx']]
        int = find_bins(alt, bins)  # find bin
        if counter == 0:            # start point of an interval
            byAltitude.append([trackId, alt, seq, int])
            counter += 1
        elif counter == 1:
            if int == byAltitude[len(byAltitude)-1][3]: # [3] is for bins
                byAltitude.append([trackId, alt, seq, int])
                counter += 1
            else:
                byAltitude.append([trackId, alt, seq, int])
                counter = 1
        else:
            if int == byAltitude[len(byAltitude) - 1][3]:
                del byAltitude[len(byAltitude)-1]       # delete row
                byAltitude.append([trackId, alt, seq, int])
                counter += 1
            else:                   # start point of an interval
                byAltitude.append([trackId, alt, seq, int])
                counter = 1
    """

    for line in tracks:
        """
        for every interval, collect start point for altitude attribute
        """
        alt = float(line[cfgs['altIdx']])
        seq = line[cfgs['seqIdx']]
        int = find_bins(alt, bins)  # find bin
        if counter == 0:            # first point (special case)
            byAltitude.append([trackId, alt, seq, int])
            counter += 1
        else:
            if int != byAltitude[len(byAltitude) - 1][3]:
                byAltitude.append([trackId, alt, seq, int])

    if params['runmode'] == 0:     # 0-application; 1-calibration
        appAlt = []
        for line in byAltitude:
            appAlt.append(line[2])  # return sequence only
        return appAlt
    elif params['runmode'] == 1:
        calibStr = []
        calibRec = len(byAltitude)
        calibStr.append([trackId, calibRec, qty_alt])
        return calibStr
    else:
        showinfo('GPS Optimizer', 'Option not available')

def onSpeedOptimize(tracks, min_speed, width_speed, qty_speed, params):
    """
    for every interval, collect start and end points for altitude attribute
    """
    bySpeed = []
    bins = create_bins(min_speed, width_speed, qty_speed)

    trackId = tracks[0][cfgs['groupIdx']] + '_' + \
              tracks[0][cfgs['unitIdx']] + '_' + \
              tracks[0][cfgs['trackIdx']]

    counter = 0
    """
    for line in tracks:        
        # for every interval, collect start and end points for altitude attribute    
        alt = float(line[cfgs['altIdx']])
        seq = line[cfgs['seqIdx']]
        int = find_bins(alt, bins)  # find bin
        if counter == 0:            # start point of an interval
            byAltitude.append([trackId, alt, seq, int])
            counter += 1
        elif counter == 1:
            if int == byAltitude[len(byAltitude)-1][3]: # [3] is for bins
                byAltitude.append([trackId, alt, seq, int])
                counter += 1
            else:
                byAltitude.append([trackId, alt, seq, int])
                counter = 1
        else:
            if int == byAltitude[len(byAltitude) - 1][3]:
                del byAltitude[len(byAltitude)-1]       # delete row
                byAltitude.append([trackId, alt, seq, int])
                counter += 1
            else:                   # start point of an interval
                byAltitude.append([trackId, alt, seq, int])
                counter = 1
    """

    for line in tracks:
        """
        for every interval, collect start point for altitude attribute
        """
        spd = float(line[cfgs['speedIdx']])
        seq = line[cfgs['seqIdx']]
        int = find_bins(spd, bins)  # find bin
        if counter == 0:  # first point (special case)
            bySpeed.append([trackId, spd, seq, int])
            counter += 1
        else:
            if int != bySpeed[len(bySpeed) - 1][3]:
                bySpeed.append([trackId, spd, seq, int])

    if params['runmode'] == 0:  # 0-application; 1-calibration
        appSpd = []
        for line in bySpeed:
            appSpd.append(line[2])  # return sequence
        return appSpd
    elif params['runmode'] == 1:
        calibStr = []
        calibRec = len(bySpeed)
        calibStr.append([trackId, calibRec, qty_speed])
        return calibStr
    else:
        showinfo('GPS Optimizer', 'Option not available')

if __name__ == '__main__':
    optInDir = r'C:\Projects\dataCompression\data\clean_tracks'
    statsDir = r'C:\Projects\dataCompression\data\stats'
    compsDir = r'C:\Projects\dataCompression\data\compressed_tracks'
    switch = 0 # switch 0-application, 1-calibration
    manager(optInDir, switch, statsDir, compsDir)