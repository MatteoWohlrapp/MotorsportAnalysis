import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import os

"""
### Read Data

To read in the data I use a dataframe. It saves some of the overhead from objects and is lazy. <br>
If you want to run this code, you need to load one of the csv files into a 'data' folder at the root of the repository
"""

data_dir = os.path.join(os.path.curdir, 'data')
available_files = os.listdir(data_dir)
for file_name in available_files:
    if '.csv' in file_name:
        file = os.path.join(data_dir, file_name)
        break
header = pd.read_csv(file, encoding='unicode_escape', skiprows=10, nrows=1, header=None)
df = pd.read_csv(file, encoding='unicode_escape', skiprows=12, header=None, names=header.iloc[0])


"""
### Overview
To get a first overview of the problem, I plot some of the most promising columns, like throttle, break and steering angle.
"""

x = df['time'].tolist()
y = df['handwheelAngle'].tolist()
fig = px.line(df, x='time', y='handwheelAngle', title='Handwheel Angle')
fig.show()

y = df['throttle'].tolist()
fig = px.line(df, x='time', y='throttle', title='Throttle')
fig.show()

y = df['brake'].tolist()
fig = px.line(df, x='time', y='brake', title='Brake')
fig.show()

y = df['horizontalSpeed'].tolist()
fig = px.line(df, x='time', y='horizontalSpeed', title='Speed')
fig.show()

"""
### Lap Split

While there are trends and patterns, especially on the steering angle, it is not trivial yet to divide into laps. <br>
My first intution was to use statistical tools, however, this yielded no result. <br>
Looking at the distance is also not an option as this might vary depending on the line and tire warming procedures etc. <br>
I therefore looked at the north and east velocity:
"""

y = df['vNorth'].tolist()
fig = px.line(df, x='time', y='vNorth', title='Speed')
fig.add_scatter(x=x, y=df['vEast'])
fig.show()


"""
The basic idea is that the start and finish straight runs south west, and so where vEast and vNorth are both highly negative, the car is on the start finish straight. <br>
In the word document, you can find more information about this idea.
With that information I create a threshold for both velocities and collect time stamps bigger than that value, then filter consecutive ones:
"""

threshold = -20
indices = []

for i in range(len(df)):
    if df['vNorth'].iloc[i] < threshold * 2 and df['vEast'].iloc[i] < threshold:
        indices.append(i)

combined_indices = []

i = 0
while i < len(indices):
    index = indices[i]
    while i < len(indices) - 1 and indices[i] == indices[i + 1] - 1:
        i += 1
    combined_indices.append(index)
    i += 1

print(combined_indices)

laps = []
# timestamp where consecutive lap begins is where current lap ends
for i in range(0, len(combined_indices) - 1):
    laps.append([combined_indices[i], combined_indices[i + 1]])


"""
### Map to distance
To make any meaningful comparisons, the values at a specific time need to be mapped to the distance travelled in that lap. <br>
"""

df_laps = []
lap_times = []

for lap in laps:
    start = df['distance'].iloc[lap[0]]
    throttle = []
    brake = []
    angle = []
    distance = []
    current_distance = 0
    lap_time = lap[1] - lap[0]

    for i in range(lap[0], lap[1]):
        if df['distance'].iloc[i] > current_distance + start:
            throttle.append(df['throttle'].iloc[i])
            brake.append(df['brake'].iloc[i])
            angle.append(df['handwheelAngle'].iloc[i])
            distance.append(current_distance)
            current_distance += 1

    new_df = pd.DataFrame({'throttle': throttle, 'brake': brake, 'distance': distance, 'handwheelAngle': angle})
    df_laps.append(new_df)
    lap_times.append(lap_time)


"""
### Visualization

After the necessary data for each lap is saved in its own dataframe, we can visualize the most interesting properties. <br>
In the following case, I compare the throttle, brake and steering angle for the three fastest laps to see what makes a difference.
"""

metrics = ['throttle', 'brake', 'handwheelAngle']


def laptimeRanking(laptimes, time):
    place = 1
    for laptime in laptimes:
        if laptime < time:
            place += 1

    return place


compare_fastest_x_laps = 3

for metric in metrics:
    fig, ax = plt.subplots()
    for i in range(len(lap_times)):
        rankedLap = laptimeRanking(lap_times, lap_times[i])
        if rankedLap <= compare_fastest_x_laps:
            label = str(laptimeRanking(lap_times, lap_times[i])) + "fastest lap"
            ax.plot(df_laps[i]['distance'], df_laps[i][metric], label=label)
    plt.xlabel('distance')
    plt.ylabel(metric)
    plt.legend(loc="upper left")
    plt.title(metric)

plt.show()
"""
With the mapping done, further extensions can be applied easily.
"""