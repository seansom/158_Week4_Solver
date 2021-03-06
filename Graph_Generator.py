import sys, os
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

data_foldername = "158_Week3_Graph_Generator_data"
data_txt_name = "158_Week4_InputData_SOM_SYZ1.txt"

os.chdir(os.path.dirname(sys.argv[0]))

data = pd.read_csv(data_txt_name, header=None)
data.columns = ["points"]

indices = range(len(data["points"]))

init_v_temp = data["points"][0]

ambient_temps = np.repeat(init_v_temp * 10, len(indices)) 
bulb_temps = data["points"].values
bulb_temps = bulb_temps * 10


fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)

ax1.plot(indices, bulb_temps, marker='o', label= 'Bulb Temperatures')
ax1.plot(indices, ambient_temps, color='black', linestyle='--', label= 'Ambient Temperatures')

ax1.fill_between(indices, bulb_temps, ambient_temps, where= (bulb_temps > ambient_temps), alpha= 0.25, label= 'Temperature Difference', interpolate= True)

ax1.set_title('Bulb and Ambient Temperatures')
ax1.set_xlabel('Time (min)')
ax1.set_ylabel('Temperature (C°)')

ax1.legend()
ax1.grid(b=True)

ax2.plot(indices, bulb_temps - ambient_temps, marker='o')

ax2.set_title('Bulb-Ambient Temperature Difference')
ax2.set_xlabel('Time (min)')
ax2.set_ylabel('Temperature (C°)')

ax2.legend()
ax2.grid(b=True)

plt.tight_layout()
plt.show()
