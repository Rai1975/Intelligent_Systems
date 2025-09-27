from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

############# PARAMETERS ##############
steps = 1000
a = 0.02
b = 0.25
c = -65.0
d = 6

V = -64.0
u = b*V

tau = 0.25


###### MAIN FUNCTION #######
tspan = np.arange(0, steps + tau, tau)

def simulation_block(a, b, c, d, V, u, I_input):
    VV = []
    uu = []
    T1 = 0
    spike_ts = []
    spike_count = 0

    #### SIMULATION TIME ###
    for t in tspan:
        if (t > T1):
            I = I_input
        else:
            I = 0

        V = V + tau * (0.04 * (V**(2)) + 5 * V + 140 - u + I)
        u = u + tau * a * (b * V - u)

        if V > 30:
            VV.append(30)
            V = c
            u += d
            spike_ts.append(1)

        else:
            VV.append(V)
            spike_ts.append(0)

        uu.append(u)

    for i in spike_ts[801:]:
        if i == 1:
            spike_count += 1

    avg_spike_count = spike_count / 800


    return spike_ts, uu, VV, avg_spike_count, spike_count




######## Plotting ##########
def plot_subgraphs(data_list, tspan, steps, I_values=None, titles=None,
                   ylabels=None, xlabels=None, ylim=(-90, 40), figsize=(12, 20)):
    n_subplots = len(data_list)
    plt.figure(figsize=figsize)

    for i, data in enumerate(data_list, start=1):
        plt.subplot(n_subplots, 1, i)
        plt.plot(tspan, data)
        plt.axis([0, np.max(tspan), ylim[0], ylim[1]])
        plt.xticks([0, np.max(tspan)], labels=[0, steps])

        # Titles
        if I_values and i-1 < len(I_values):
            plt.title(f"I = {I_values[i-1]}")
        elif titles and i-1 < len(titles):
            plt.title(titles[i-1])

        plt.grid(True)

    plt.tight_layout()
    plt.show()

# print(len(VV))

def plot_RvI():
    df = pd.read_csv('./AVG_R_VALUES.csv')

    plt.plot(df['I_input'], df['avg_spike_count'])
    plt.xlabel('I Value')
    plt.ylabel('R Value')

    plt.show()

if __name__ == "__main__":
    # plot_RvI()

    spikes_ts_list = []
    uu_list = []
    VV_list = []
    avg_spike_count_list = []
    I_input_vals = [1, 10, 20, 30, 40, 50, 60]
    I_values=[]

    for I in range(0, 61, 2):
        spike_ts, uu, VV, avg_spike_count, spike_count = simulation_block(
            a, b, c, d, V, u, I_input=I
        )
        avg_spike_count_list.append({"I_input": I, "avg_spike_count": avg_spike_count})

    avg_spike_count_df = pd.DataFrame(avg_spike_count_list)

    avg_spike_count_df.to_csv('./AVG_R_VALUES.csv', index=False)


    for I in range(1, 61, 10):
        spike_ts, uu, VV, avg_spike_count, spike_count = simulation_block(
            a, b, c, d, V, u, I_input=I
        )
        spikes_ts_list.append(spike_ts)

        uu_list.append(uu)
        VV_list.append(VV)
        I_values.append(I)


    plot_subgraphs(VV_list, tspan, steps, I_values)