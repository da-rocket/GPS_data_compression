import os, time, datetime
import csv
from geopy import distance

# general configuration
try:
    import config
    cfgs = config.__dict__
except Exception as e:                                                  # define in client app directory
    print(e)

"""
This module is implemented using generator function to work efficiently with memory. It has:
1. Reads original gps data feed
2. Filter each record by min/max altitude and speed interval
3. Convert data stream into individual tracks using a rule: 120s interval and same date
4. Writes data back to the disk
"""

# main control for testing
def manager(params):
    for (trackIdx, trackList) in fileReader(params):
        fileWriter(trackIdx, trackList, params, name='')
        statsList = stats(trackIdx, trackList, params)
        fileWriter(None, statsList, params, name='original_stats')

def fileReader(params):
    for (thisDir, subsHere, filesHere) in os.walk(params['gpsDir']):    # function to read and clean data
        for filename in filesHere:
            if filename.endswith('.csv'):
                fpath = os.path.join(thisDir, filename)
                clean_pts = []                                          # initialization
                trackIdx = []
                trackId = 0
                ptnSeq = 0
                firstPtFlag = False
                startIdx = endIdx = 0
                secDiff = 0
                pntDate = True
                with open(fpath, newline='') as f:
                    next(f)         # skip header
                    for line in f:
                        line = line.strip().split(',')
                        pntGroup  = line[cfgs['groupIdx']]
                        pntUnit   = line[cfgs['unitIdx']]
                        pntDate   = line[cfgs['dateIdx']]
                        pntTime   = line[cfgs['timeIdx']]
                        pntLat    = line[cfgs['latIdx']]
                        pntLong   = "-" + line[cfgs['longIdx']]
                        pntAlt    = float(line[cfgs['altIdx']])
                        pntSpeed  = float(line[cfgs['speedIdx']])

                        pntSec = timeToSec(pntTime)                     # convert timestamp to seconds
                        # flagByLine = lineFilter(pntAlt, pntSpeed)
                        flagByLine = lineFilter(pntAlt, pntSpeed, params)

                        if flagByLine:
                            if not firstPtFlag:                         # first point(special case)
                                clean_pts.append([pntGroup, pntUnit, pntDate, pntTime, pntLat, pntLong,
                                                  pntAlt, pntSpeed, pntSec, trackId, ptnSeq])
                                firstPtFlag = True
                            else:
                                index = len(clean_pts) - 1
                                secDiff = pntSec - clean_pts[index][cfgs['secsIdx']]
                                sameDate = True if pntDate == clean_pts[index][cfgs['dateIdx']] else False

                                if secDiff <= 120 and sameDate:     # 120 seconds used to split tracks
                                    ptnSeq += 1
                                    clean_pts.append([pntGroup, pntUnit, pntDate, pntTime, pntLat, pntLong,
                                                      pntAlt, pntSpeed, pntSec, trackId, ptnSeq])
                                else:
                                    endIdx = len(clean_pts)         # get indexes (start/end) to split tracks
                                    trackIdx.append((startIdx, endIdx))
                                    startIdx = endIdx

                                    trackId += 1                    # section to start new track
                                    ptnSeq = 0
                                    clean_pts.append([pntGroup, pntUnit, pntDate, pntTime, pntLat, pntLong,
                                                      pntAlt, pntSpeed, pntSec, trackId, ptnSeq])

            endIdx = len(clean_pts)                                 # special case for the last track
            startIdx = len(trackIdx) - 1                            # get indexes (start/end) to split tracks

            if startIdx >= 0:                                       # handle exception when file has 1 line
                startIdx = trackIdx[startIdx][1]
                trackIdx.append((startIdx, endIdx))
                yield trackIdx, clean_pts                           # genetator functions
            else:
                print('skipping: ', fpath)

def timeToSec(timestamp):
    try:
        timeFormat = time.strptime(timestamp, "%H:%M:%S")           # convert timestamp to seconds
        pntSec = datetime.timedelta(hours=timeFormat.tm_hour, minutes=timeFormat.tm_min,
                                    seconds=timeFormat.tm_sec).seconds
        return pntSec
    except:
        print('Cannot convert time to seconds')

def lineFilter(pntAlt, pntSpeed, params):                           # filter points by altitude and speed intervals
    if ((pntAlt > params['altMin']) and (pntAlt < params['altMax'])) and (
            (pntSpeed > params['spdMin']) and (pntSpeed < params['spdMax'])):
        return True

def fileWriter(trackIdx, trackList, params, name=''):
    if trackIdx is not None:                                        # used to write gps files
        for (start, end) in trackIdx:
            sObject = slice(start, end)
            track = (trackList[sObject])
            trackId = getId(track[0])
            fname = trackId + '.csv'
            fpath = os.path.join(params['cleanDir'], fname)
            if not os.path.exists(fpath):
                with open(fpath, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows(track)
    else:                                                           # used to write stats file
        fname = name + '.csv'
        fpath = os.path.join(params['statsDir'], fname)
        with open(fpath, 'a', newline='') as f:                     # write files
            writer = csv.writer(f)
            writer.writerows(trackList)

def getId(track):
    fname = str(track[cfgs['groupIdx']]) + '_' + \
            str(track[cfgs['unitIdx']]) + '_' + \
            str(track[cfgs['trackIdx']])
    return fname

def getNumRecords(track):
    return len(track)

def getMaxHeight(track):
    return max([i[cfgs['altIdx']] for i in track])

def getMinHeight(track):
    return min([i[cfgs['altIdx']] for i in track])

def getMaxSpeed(track):
    return max([i[cfgs['speedIdx']] for i in track])

def getMinSpeed(track):
    return min([i[cfgs['speedIdx']] for i in track])

def getFileSize(trackId, cleanDir):
    fname = trackId + '.csv'
    fpath = os.path.join(cleanDir, fname)
    return os.path.getsize(fpath)

def getTrackLength(track):
    LatLong = [(float(i[cfgs['latIdx']]), float(i[cfgs['longIdx']])) for i in track]
    length = 0.0
    for (lat, long) in LatLong:
        if LatLong.index((lat, long)) == 0:                         # first record
            startPoint = (lat, long)
        else:
            nextPoint = (lat, long)
            length += float(str(distance.distance(startPoint, nextPoint)).split()[0]) # convert geopy result to float
            startPoint = nextPoint
    return length

def stats(trackIdx, trackList, params):
    trackStats = []
    for (start, end) in trackIdx:
        sObject = slice(start, end)
        track = (trackList[sObject])

        trackId     = getId(track[0])
        numRecs     = getNumRecords(track)
        minHeight   = getMinHeight(track)
        maxHeight   = getMaxHeight(track)
        minSpeed    = getMinSpeed(track)
        maxSpeed    = getMaxSpeed(track)
        fileSize    = getFileSize(trackId, params['cleanDir'])
        trackLength = getTrackLength(track)

        trackStats.append((trackId, numRecs, minHeight, maxHeight, minSpeed, maxSpeed, fileSize, trackLength))
    return trackStats

if __name__ == '__main__':
    params = {}
    gpsDir = r'C:\Projects\dataCompression\input_data\test_data'
    cleanDir = r'C:\Projects\dataCompression\input_data\out_data'
    params = {'gpsDir': gpsDir,
              'cleanDir': cleanDir}
    manager(params)
