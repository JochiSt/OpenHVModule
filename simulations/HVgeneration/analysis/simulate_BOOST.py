import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append("../../PyLTSpice")

from PyLTSpice import LTSpiceBatch, LTSteps

# store the simulation results
frequency = np.array([])
dutycycle = np.array([])
uoutmax   = np.array([])

def processing_data(raw_filename, log_filename):
    # read the spice log file
    log_info = LTSteps.LTSpiceLogReader(log_filename)
    names = log_info.get_measure_names()

    global frequency
    global dutycycle
    global uoutmax

    # ensure that we get our results
    assert "f" in names
    assert "d" in names
    assert "uoutmax" in names

    print(log_info.get_measure_value("f"), end="\t")
    print(log_info.get_measure_value("d"), end="\t")
    print(log_info.get_measure_value("uoutmax"))

    frequency = np.append(frequency, log_info.dataset["f"])
    dutycycle = np.append(dutycycle, log_info.dataset["d"])
    uoutmax   = np.append(uoutmax,   log_info.dataset["uoutmax"])

LTC = LTSpiceBatch.SimCommander(
        "../BoostConverter.asc",    # path to LTspice simulation file
        parallel_sims=2             # limit number of parallel simulations
        )
LTC.set_parameters(temp=40)         # Sets the simulation temperature

for duty in np.linspace(20, 90, 10):
    for freq in np.linspace(50e3, 500e3, 10):
        print("Simulating frequency:", freq , "Hz + dutycycle:", duty , "%")

        LTC.set_parameter("duty", duty)
        LTC.set_parameter("frequency", freq)
        LTC.run(wait_resource=True, callback=processing_data)

#        LTC.set_component_value('R1', res_value)  #  Updates the resistor R1 value to be 3.3k


LTC.wait_completion()  # Waits for the LTSpice simulations to complete
print("Total Simulations: {}".format(LTC.runno))
print("Successful Simulations: {}".format(LTC.okSim))
print("Failed Simulations: {}".format(LTC.failSim))

# sort data according to frequency
p = frequency.argsort()
frequency = frequency[p]
dutycycle = dutycycle[p]
uoutmax   = uoutmax[p]

# get unique dutycycle
dutycycle_unique = np.unique(dutycycle)
print(dutycycle_unique)

# Plotting
plt.title("Boost converter parameter evaluation")

for cycle in dutycycle_unique:
    select = np.where(dutycycle == cycle)
    plt.plot(frequency[select]/1000, uoutmax[select],
                 label='dutycycle = {}%'.format(cycle))

plt.xlabel('frequency / kHz')
plt.ylabel('output voltage / V')
plt.legend()
plt.show()