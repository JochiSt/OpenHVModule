
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # input filename
    filename = "../BoostConverter_varF_BC847A.txt"

    dutycycle_dict = {}
    uoutmax_dict = {}

    ##########################################################################
    with open(filename, "r") as ltspice_file:
        for line in ltspice_file:

            try:
                dutycycle, frequency, uoutmax = line.split("\t")

                frequency = float(frequency)

                if frequency not in dutycycle_dict.keys():
                    dutycycle_dict[frequency] = []
                    uoutmax_dict[frequency] = []

                dutycycle = float(dutycycle)
                uoutmax = float(uoutmax)

                dutycycle_dict[frequency].append(dutycycle)
                uoutmax_dict[frequency].append(uoutmax)

                print(frequency/1000, dutycycle, uoutmax)

            except Exception as e:
                print(e)
                pass

    for key in dutycycle_dict.keys():
        # convert array into numpy
        dutycycle_dict[key] = np.array(dutycycle_dict[key])
        uoutmax_dict[key] = np.array(uoutmax_dict[key])

        # sort arrays using the dutycycle
        p = dutycycle_dict[key].argsort()
        dutycycle_dict[key] = dutycycle_dict[key][p]
        uoutmax_dict[key] = uoutmax_dict[key][p]

    plt.title("Boost converter parameter evaluation")

    for key in dutycycle_dict.keys():
        plt.plot(dutycycle_dict[key], uoutmax_dict[key], label='f=%d kHz'%(key/1000))

    plt.xlabel('duty cycle / %')
    plt.ylabel('output voltage / V')
    plt.legend()
    plt.show()