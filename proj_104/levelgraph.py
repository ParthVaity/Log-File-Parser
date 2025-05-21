#Level State Distribution graph code

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from timeparser import parse_timestamp,format

def generate_level_graph(csv_path, output_png, mintime ,maxtime):
    level=['notice','error']
    colors=['red','green']
    count = [0,0]
    with open(csv_path, 'r') as f: #iterating though the file to find the count of each event
        header=next(f)
        for line in f:
            h=line.strip().split(',')
            timestamp = parse_timestamp(h[1].strip())
            g=h[2]
            if mintime and timestamp < mintime:
                continue
            if maxtime and timestamp > maxtime:
                continue
            if(g == 'notice'):
                count[0]=count[0]+1
            else:
                count[1]=count[1]+1
    plt.figure(figsize=(6,6))
    plt.pie(count, labels=level, colors=colors, autopct=make_autopct(count), startangle=90)
    plt.title(f'Level State Distribution\n({format(mintime)} to {format(maxtime)})')
    os.makedirs(os.path.dirname(output_png), exist_ok=True)
    plt.savefig(output_png)
    plt.close()
    
def make_autopct(values):#Presents percentage and numerical values both ono the pie chart
    def my_autopct(pct):
        total = sum(values)
        count = int(round(pct * total / 100.0))
        return f'{pct:.1f}%\n({count})'
    return my_autopct