import numpy as np

MONTHS = { 
    'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4,
    'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8,
    'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
}

def parse_timestamp(timestr): #Converts the time column into np.datetime() format
    parts = timestr.strip().split()
    month = MONTHS[parts[1]]
    day = int(parts[2])
    time_parts = list(map(int, parts[3].split(':')))
    year = int(parts[4])
    return np.datetime64(f'{year:04d}-{month:02d}-{day:02d}T{time_parts[0]:02d}:{time_parts[1]:02d}:{time_parts[2]:02d}')

def format(date): #splits np.datetime() format into date and time to present them in a line
    s=str(date)
    if 'T' in s:
        date,time=s.split('T')
        return f"{date} {time}"
    return s