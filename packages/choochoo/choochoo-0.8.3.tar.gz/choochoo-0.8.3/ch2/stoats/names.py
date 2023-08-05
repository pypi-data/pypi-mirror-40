
ACTIVE_DISTANCE = 'Active Distance'
ACTIVE_TIME = 'Active Time'
ACTIVE_SPEED = 'Active Speed'
ACTIVITY = 'Activity'
CUMULATIVE_STEPS_START = 'Cumulative Steps Start'
CUMULATIVE_STEPS_FINISH = 'Cumulative Steps Finish'
DAILY_STEPS = 'Daily Steps'
DISTANCE = 'Distance'
FATIGUE = 'Fatigue'
FITNESS = 'Fitness'
FTHR = 'FTHR'
HEART_RATE = 'Heart Rate'
HR_IMPULSE = 'HR Impulse'
HR_ZONE = 'HR Zone'
LATITUDE = 'Latitude'
LONGITUDE = 'Longitude'
MEDIAN_KM_TIME = 'Median %dkm Time'
MEDIAN_KM_TIME_ANY = 'Median % Time'
PERCENT_IN_Z = 'Percent in Z%d'
PERCENT_IN_Z_ANY = 'Percent in Z%'
SEGMENT_TIME = 'Segment Time'
SEGMENT_DISTANCE = 'Segment Distance'
SEGMENT_HEART_RATE = 'Segment Heart Rate'
SPEED = 'Speed'
SPHERICAL_MERCATOR_X = 'Spherical Mercator X'
SPHERICAL_MERCATOR_Y = 'Spherical Mercator Y'
STEPS = 'Steps'
REST_HR = 'Rest HR'
TIME_IN_Z = 'Time in Z%d'
MAX_MED_HR_M = 'Max Med HR %dm'
MAX_MED_HR_M_ANY = 'Max Med HR %'

HR_MINUTES = (5, 10, 15, 20, 30, 60, 90, 120, 180)

MAX = '[max]'
MIN = '[min]'
CNT = '[cnt]'
AVG = '[avg]'
SUM = '[sum]'
MSR = '[msr]'   # measure (separate table, less efficient)


def summaries(*args):
    return ','.join(args)


M = 'm'
S = 's'
H = 'h'
DEG = 'deg'
KMH = 'km/h'
PC = '%'
BPM = 'bpm'
KG = 'kg'
STEPS_UNITS = 'steps'
ENTRIES = 'entries'


def round_km():
    yield from range(5, 21, 5)
    yield from range(25, 76, 25)
    yield from range(100, 251, 50)
    yield from range(300, 1001, 100)
