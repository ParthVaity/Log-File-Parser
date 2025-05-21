#Event Logged with Time graph code

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from timeparser import parse_timestamp,format

def generate_eventvtime_graph(csv_path, selected_events, output_png, mintime, maxtime):
    event_time_dict = {} #dictionary of type dict[event]=list[timestamps] to keep track of timestamps of each event

    with open(csv_path, 'r') as f: #iterating through the file to find the timestamps of each event and appending into the dictionary
        header = next(f)
        for line in f:
            if line.strip():
                parts = line.strip().split(',')
                time_str = parts[1].strip()
                event = parts[4].strip()
                ts = parse_timestamp(time_str)
                if mintime and ts < mintime: continue
                if maxtime and ts > maxtime: continue
                if event in selected_events:
                    if event not in event_time_dict:
                        event_time_dict[event] = []
                    event_time_dict[event].append(ts)


    plt.figure(figsize=(12, 6))
    colors = ['red', 'green', 'blue', 'purple', 'orange', 'cyan']
    color_map = {event: colors[i % len(colors)] for i, event in enumerate(selected_events)}

    for event in selected_events:
        times = np.array(event_time_dict.get(event, []))
        if times.size == 0:
            continue
        unique_times, counts = np.unique(times, return_counts=True) #getting the count of each timestamp
        plt.plot(unique_times, counts, marker='o', label=event, color=color_map[event], linewidth=1.0, markersize=4) #combining plots of all selected evets

    title = ",".join(selected_events)
    plt.xlabel('Time')
    plt.ylabel('Number of Events')
    plt.title(f"{title} occurrences over Time\n({format(mintime)} to {format(maxtime)})")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    os.makedirs(os.path.dirname(output_png), exist_ok=True)
    plt.savefig(output_png)
    plt.close()
