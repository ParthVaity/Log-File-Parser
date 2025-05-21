import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

def generate_self_plot(csv_path, output_png, mintime ,maxtime):
    #Define fields here as arrays
    with open(csv_path, 'r') as f:
        header=next(f)
        for line in f:
            h=line.strip().split(',')
            #Initial CSV file is of the format LineId,Time,Level,Content,EventId,EventTemplate
            #Select which columns you want in your fields
            #use parse_timestamp if u are using the time column
    plt.figure(figsize=(6,6))
    #plt.(typeofgraph) here
    plt.title(f'Self plot\n({format(mintime)} to {format(maxtime)})')
    os.makedirs(os.path.dirname(output_png), exist_ok=True)
    plt.savefig(output_png)
    plt.close()

MONTHS = {
    'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4,
    'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8,
    'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
}

def parse_timestamp(timestr):
    parts = timestr.strip().split()
    month = MONTHS[parts[1]]
    day = int(parts[2])
    time_parts = list(map(int, parts[3].split(':')))
    year = int(parts[4])
    return np.datetime64(f'{year:04d}-{month:02d}-{day:02d}T{time_parts[0]:02d}:{time_parts[1]:02d}:{time_parts[2]:02d}')

def format(date):
    s=str(date)
    if 'T' in s:
        date,time=s.split('T')
        return f"{date} {time}"
    return s