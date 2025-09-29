from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

############# PARAMETERS ##############

steps = 1000
# Fask Spiking
a = 0.1
b = 0.20
c = -65.0
d = 2

# Regular Spiking
# a = 0.02
# b = 0.20
# c = -65
# d = 8

V = -65.0
u = b*V

tau = 0.25

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
        plt.xlabel('Time series')
        plt.ylabel('Vm')
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

def plot_RvI_comparison():
    df_fast = pd.read_csv('./AVG_R_VALUES_FS.csv')
    df_regular = pd.read_csv('./AVG_R_VALUES_RS.csv')

    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

    # Fast Spiking neuron RvI
    axes[0].plot(df_fast['I_input'], df_fast['avg_spike_count'], label="Fast Spiking", color="blue")
    axes[0].set_xlabel('I Value')
    axes[0].set_ylabel('R Value (Hz)')
    axes[0].set_title('Fast Spiking Neuron')
    axes[0].grid(True)

    # Regular Spiking neuron RvI
    axes[1].plot(df_regular['I_input'], df_regular['avg_spike_count'], label="Regular Spiking", color="red")
    axes[1].set_xlabel('I Value')
    axes[1].set_title('Regular Spiking Neuron')
    axes[1].grid(True)

    plt.tight_layout()
    plt.show()


def run_talking_neurons_simulation(W):
    a = 0.02
    b = 0.2
    c = -50
    d = 2.0
    IA = 5
    IB = 2

    VA, VB = V, V
    uA, uB = b*V, b*V


    VA_trace, VB_trace = [], []
    spikes_A, spikes_B = [], []

    for t in tspan:
        # Spike indicators
        yA = 1 if VA > 30 else 0
        yB = 1 if VB > 30 else 0

        # Total input currents
        I_total_A = IA + (-W) * yB
        I_total_B = IB + (+W) * yA

        if I_total_A != 5 or I_total_B != 2:
            print(I_total_A, I_total_B)

        # Update dynamics
        VA += tau * (0.04 * VA**2 + 5 * VA + 140 - uA + I_total_A)
        VB += tau * (0.04 * VB**2 + 5 * VB + 140 - uB + I_total_B)

        uA += tau * a * (b * VA - uA)
        uB += tau * a * (b * VB - uB)

        # Spike reset
        if VA > 30:
            VA_trace.append(30)
            VA = c
            uA += d
            spikes_A.append(1)
        else:
            VA_trace.append(VA)
            spikes_A.append(0)

        if VB > 30:
            VB_trace.append(30)
            VB = c
            uB += d
            spikes_B.append(1)
        else:
            VB_trace.append(VB)
            spikes_B.append(0)

    return VA_trace, VB_trace, spikes_A, spikes_B


def plot_chattering_neurons():
    Ws = [0, 15, 30, 45, 60]
    plt.figure(figsize=(12, 10))

    for i, W in enumerate(Ws, start=1):
        VA, VB, _, _ = run_talking_neurons_simulation(W)
        plt.subplot(len(Ws), 1, i)
        plt.plot(tspan, VA, label="Neuron A (Excitatory)")
        plt.plot(tspan, VB, label="Neuron B (Inhibitory)")
        plt.title(f"Two-Neuron Network, W = {W}")
        plt.xlabel("Time")
        plt.ylabel("Vm")
        plt.legend()
        plt.grid(True)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # spikes_ts_list = []
    # uu_list = []
    # VV_list = []
    # avg_spike_count_list = []
    # I_input_vals = [1, 10, 20, 30, 40, 50, 60]
    # I_values=[]

    # for I in range(0, 61, 2):
    #     spike_ts, uu, VV, avg_spike_count, spike_count = simulation_block(
    #         a, b, c, d, V, u, I_input=I
    #     )
    #     avg_spike_count_list.append({"I_input": I, "avg_spike_count": avg_spike_count})

    # avg_spike_count_df = pd.DataFrame(avg_spike_count_list)

    # avg_spike_count_df.to_csv('./AVG_R_VALUES_FS.csv', index=False)

    # plot_RvI_comparison()


    # for I in I_input_vals:
    #     spike_ts, uu, VV, avg_spike_count, spike_count = simulation_block(
    #         a, b, c, d, V, u, I_input=I
    #     )
    #     spikes_ts_list.append(spike_ts)

    #     uu_list.append(uu)
    #     VV_list.append(VV)
    #     I_values.append(I)


    # plot_subgraphs(VV_list, tspan, steps, I_values)

    plot_chattering_neurons()