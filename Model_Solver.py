import sys, os
from matplotlib import pyplot as plt
from statistics import mean
import numpy as np
import pandas as pd

# Sample txt files: EEE158_Week4_InputData_BELLEN_SYZ1.txt, EEE158_Week4_InputData_SOMBRITO_SYZ1.txt
data_txt_name = "EEE158_Week4_InputData_SOMBRITO_SYZ1.txt"
step_input = 3

os.chdir(os.path.dirname(sys.argv[0]))

data = pd.read_csv(data_txt_name, header=None)
data.columns = ["points"]



# set initial value of V_temp
init_v_temp = data["points"].values[0]

time = np.arange(0, len(data["points"]))

# turn into LTI system by subtracting V_temp(0) and shifting the V_temp readings
v_temp = data["points"].values - init_v_temp
# Assume that system reaches steady state at t = total_time_readings - num_of_steady_state_readings
num_of_steady_state_readings = 1
v_steadystate = np.mean(v_temp[-num_of_steady_state_readings:])

# let β = K/α
β = v_steadystate / step_input


# compute for all possible α given different times and V_temp readings
# exclude t = 0 and any V_temp readings higher than V_steadystate
# since these will result to a math error
mask = np.logical_and(v_temp < v_steadystate, time != 0)
possible_α_values = []

for i in range(len(mask)):
    if mask[i]:
        possible_α_values.append(np.log((step_input * β - round(v_temp[i], 2)) / (step_input * β)) / (- time[i]))


# get the mean α that will be used to model the system
α_mean = np.mean(possible_α_values)


# solve for K for model specification
K = β * α_mean


# construct model give values for α and β
v_temp_model = (step_input * β) * (1 - (np.exp(- α_mean * time)))


# re-shift actual and model readings by initial V_temp value
v_temp = v_temp + init_v_temp
v_temp_model = v_temp_model + init_v_temp




# plot the Actual and Model V_temp
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)

ax1.plot(time, v_temp, 'k--', label= 'V_temp Actual')
ax1.plot(time, v_temp_model, marker='o', label= 'V_temp Model')

ax1.fill_between(time, v_temp, v_temp_model, where= (v_temp > v_temp_model), color='green', alpha= 0.25, label= 'Undershoot', interpolate= True)
ax1.fill_between(time, v_temp, v_temp_model, where= (v_temp < v_temp_model), color='red', alpha= 0.25, label= 'Overshoot', interpolate= True)

ax1.set_title('Model and Actual Voltages')
ax1.set_xlabel('Time (min)')
ax1.set_ylabel('Voltage (V)')

ax1.legend()
ax1.grid(b=True)

ax2.plot(time, ((v_temp_model - v_temp) / v_temp) * 100, marker='o')

ax2.set_title('Model-Actual Voltage Difference Error')
ax2.set_xlabel('Time (min)')
ax2.set_ylabel('Error (%)')

ax2.grid(b=True)

# Print out constant values used in the model
print(f'v_steadystate = {v_steadystate + init_v_temp}')
print(f'β = {round(β, 6)}')
print(f'α = {round(α_mean, 6)}')
print(f'K = {round(K, 6)}')

print()
print(f'Model: V_temp(t) = [({round(3 * β, 6)}) * (1 - e ^ (-{round(α_mean, 6)} t)) + 2.74] u(t)')

plt.tight_layout()
plt.show()