#----------------------------------------------------------------------------------
# General configurations
# comment-out any setting in this section to accept Tk or program defaults;
#----------------------------------------------------------------------------------

# header index for gps file
groupIdx    = 0
unitIdx     = 1
dateIdx     = 2
timeIdx     = 3
latIdx      = 4
longIdx     = 5
altIdx      = 6
speedIdx    = 7
secsIdx     = 8
trackIdx    = 9
seqIdx      = 10

# header index for stats file
trackId     = 0
numRecs     = 1
minHeight   = 2
maxHeight   = 3
minSpeed    = 4
maxSpeed    = 5
fileSize    = 6
trackLength = 7

# altitude & instanteneous speed intervals
altMin = 200.0          # in meters
altMax = 600.           # in meters
spdMin = 0.             # in km/hr
spdMax = 40.            # in km/hr

# switch to run calibration components
calByLen    = 0         # 0-False, 1-True
calByAlt    = 0
calBySpd    = 0

# switch to run validation components
appByLen    = 1         # 0-False, 1-True
appByAlt    = 1
appBySpd    = 1

# default settings for length compression (calibration)
start           = 1     # in degrees
end             = 5     # in degrees
step            = 0.1   # in degrees

# default settings for length compression (application)
devByCathetus   = 15.0  # in meters
devByAng        = 6.8   # in degrees

# settings for byLength
lenLatIdx      = 0
lenLongIdx     = 1

# default settings for height compression using equal intervals method (calibration)
hstart         = 1      # class start
hstop          = 101    # class end
hstep          = 1      # class step

# default settings for altitude compression (application)
hNumClasses    = 45     # number of classes

# default settings for speed compression using equal intervals method (calibration)
spd_start         = 1      # class start
spd_stop          = 41     # class end
spd_step          = 1      # class step

# default settings for speed compression (application)
spd_NumClasses    = 20      # number of classes

