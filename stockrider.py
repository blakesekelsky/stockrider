import json
import yfinance as yf

# Build the structure of the gamefile
label = 'stockrider'
creator = 'blake'
description = 'generated gamefile'
duration = 1200
version = '6.2'
audio = None
startPosition = {
    "x": 0,
    "y": 0
}
riders = [
    {
        "startPosition": {
            "x": 0,
            "y": 0
        },
        "startVelocity": {
            "x": 0.4,
            "y": 0
        },
        "remountable": 1
    }
]
layers = [
    {
        "id": 0,
        "name": "Base Layer",
        "visible": True,
        "editable": True
    }
]
lines = []

def stock_plots(ticker='aapl', from_date='2020-01-01', to_date='2020-01-30', x_inc=150, y_mult=40):
    data = yf.download(ticker, from_date, to_date)
    open_close = data[['Open', 'Close']].reset_index(drop=True).values

    plots = []
    counter = 0
    for open, close in open_close:
        plots.append([counter+x_inc, -open*y_mult, counter+(x_inc*2), -close*y_mult])
        counter = counter + x_inc
    return plots

plots = stock_plots(ticker='tsla', from_date='2020-01-01', to_date='2022-01-01', x_inc=150, y_mult=20)

def smooth_plots(plots):
    # O+C/2 [n][3] + [n+1][1] / 2
    counter = 0
    for plot in plots:
        if counter != len(plots)-1:
            plots[counter][3] = (plots[counter+1][1] + plots[counter][3]) / 2
            plots[counter+1][1] = plots[counter][3]
            counter = counter + 1
    return plots

plots = smooth_plots(plots)

def stage_lines(plots):
    lines = []
    counter = 0
    for plot in plots:
        data = {
            "id": counter,
            "type": 1,
            "x1": plot[0],
            "y1": plot[1],
            "x2": plot[2],
            "y2": plot[3],
            "flipped": False,
            "leftExtended": False,
            "rightExtended": False
        }
        lines.append(data)
        counter = counter + 1
    return lines

lines = stage_lines(plots)

def save_track(label= label,
               creator= creator,
               description= description,
               versio= version,
               audio= audio,
               startPosition= startPosition,
               riders= [
                   {
                       "startPosition": {
                           "x": lines[0]['x1'] + 10,
                           "y": lines[0]['y1'] - 20
                       },
                       "startVelocity":{
                           "x": 5,
                           "y": 0
                       },
                       "remountable": 1
                   }
               ],
               layers= layers,
               lines= lines,
               filename='stockrider.track.json'):
    track = {
        "label": label,
        "creator": creator,
        "description": description,
        "version": version,
        "audio": audio,
        "startPosition": startPosition,
        "riders": riders,
        "layers": layers,
        "lines": lines
    }

    with open(filename, 'w') as outfile:
        json.dump(track, outfile)

save_track(lines=lines, filename='smooth.track.json')

