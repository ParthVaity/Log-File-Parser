#Event Code Distribution graph code

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from timeparser import parse_timestamp,format

def generate_eventcode_graph(csv_path, output_png, mintime, maxtime):
    eventcode=['E1','E2','E3','E4','E5','E6']
    count = [0,0,0,0,0,0]
    with open(csv_path, 'r') as f: #iterating through the file to find count of each event
        header=next(f)
        for line in f:
            h=line.strip().split(',')
            timestamp=parse_timestamp(h[1].strip())
            g=h[4]
            if mintime and timestamp < mintime:
                continue
            if maxtime and timestamp > maxtime:
                continue
            if(g == 'E1'):
                count[0]+=1
            if(g == 'E2'):
                count[1]+=1
            if(g == 'E3'):
                count[2]+=1
            if(g == 'E4'):
                count[3]+=1
            if(g == 'E5'):
                count[4]+=1
            if(g == 'E6'):
                count[5]+=1
    fig, ax = plt.subplots()  
    bars = ax.bar(eventcode, count, color='skyblue')
    ax.bar_label(bars)
    plt.xlabel('Events')
    plt.ylabel('Count')
    plt.title(f'Event Code Distribution\n({format(mintime)} to {format(maxtime)})')
    os.makedirs(os.path.dirname(output_png), exist_ok=True)
    plt.savefig(output_png)
    plt.close()