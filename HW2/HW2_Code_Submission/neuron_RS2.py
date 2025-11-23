from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

############# PARAMETERS ##############

steps = 1000

V = -65.0

tau = 0.25

tspan = np.arange(0, steps + tau, tau)

def get_neuron_params(neuron_type):
    if neuron_type == 'fast':
        return 0.1, 0.20, -65.0, 2
    else:
        return 0.02, 0.20, -65, 8


## This section of the code has been implemented directly with reference to
# Izhikev's matlab code as provided with the assignment in a file titled
# `neuron_RS2.m`
def simulation_block(a, b, c, d, V, u, I_input):
    VV = []
    uu = []
    T1 = 0
    spike_ts = []
    spike_count = 0

    for t in tspan:
        # This part of the code doesn't contribute much,
        # but is kept as an artifact from Izhikev's code
        # where they intended the spiking to only begin after
        # t = 50.
        if (t > T1):
            I = I_input
        else:
            I = 0

        # Update neuron state using Izhikevich model equations
        # V equation: dV/dt = 0.04V² + 5V + 140 - u + I
        # u equation: du/dt = a(bV - u)
        V = V + tau * (0.04 * (V**(2)) + 5 * V + 140 - u + I)
        u = u + tau * a * (b * V - u)

        # Record traces of V and u, and keep track of spikes.
        if V > 30:
            VV.append(30)
            V = c
            u += d
            spike_ts.append(1)
        else:
            VV.append(V)
            spike_ts.append(0)

        uu.append(u)

    # Calculate average spike count
    # R = (number of spikes in last 800 steps) / 800
    for i in spike_ts[801:]:
        if i == 1:
            spike_count += 1

    avg_spike_count = spike_count / 800

    return spike_ts, uu, VV, avg_spike_count, spike_count


# Function to plot different voltage traces
def plot_subgraphs(data_list, tspan, steps, I_values=None, titles=None,
                   ylabels=None, xlabels=None, ylim=(-90, 40), figsize=(12, 20)):
    n_subplots = len(data_list)
    plt.figure(figsize=figsize)

    for i, data in enumerate(data_list, start=1):
        plt.subplot(n_subplots, 1, i)
        plt.plot(tspan, data)
        plt.axis([0, np.max(tspan), ylim[0], ylim[1]])
        plt.xticks([0, np.max(tspan)], labels=[0, steps])

        plt.xlabel('Time series')
        plt.ylabel('Vm')
        if I_values and i-1 < len(I_values):
            plt.title(f"I = {I_values[i-1]}")
        elif titles and i-1 < len(titles):
            plt.title(titles[i-1])

        plt.grid(True)

    plt.tight_layout()
    plt.show()

# Function to plot RvI
def plot_RvI():
    df = pd.read_csv('./AVG_R_VALUES.csv')

    plt.plot(df['I_input'], df['avg_spike_count'])
    plt.xlabel('I Value')
    plt.ylabel('R Value')

    plt.show()


# Function to plot RvI for RS vs FS (fig 2.2)
def plot_RvI_comparison():
    df_fast = pd.read_csv('./AVG_R_VALUES_FS.csv')
    df_regular = pd.read_csv('./AVG_R_VALUES_RS.csv')

    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

    axes[0].plot(df_fast['I_input'], df_fast['avg_spike_count'], label="Fast Spiking", color="blue")
    axes[0].set_xlabel('I Value')
    axes[0].set_ylabel('R Value (Hz)')
    axes[0].set_title('Fast Spiking Neuron')
    axes[0].grid(True)

    axes[1].plot(df_regular['I_input'], df_regular['avg_spike_count'], label="Regular Spiking", color="red")
    axes[1].set_xlabel('I Value')
    axes[1].set_title('Regular Spiking Neuron')
    axes[1].grid(True)

    plt.tight_layout()
    plt.show()


# Code to run simulation for 2 chattering neuron network.
def run_talking_neurons_simulation(W):
    a, b, c, d = 0.02, 0.2, -50, 2

    IA = 5
    IB = 2

    VA, VB = V, V
    uA, uB = b*V, b*V

    VA_trace, VB_trace = [], []
    spikes_A, spikes_B = [], []

    # These are used to keep track of yA and yB so
    yA_prev = 0
    yB_prev = 0

    for t in tspan:
        I_total_A = IA + (-W) * yB_prev
        I_total_B = IB + (+W) * yA_prev

        # Update neuron state using Izhikevich model equations
        # V equation: dV/dt = 0.04V² + 5V + 140 - u + I
        # u equation: du/dt = a(bV - u)
        VA += tau * (0.04 * VA**2 + 5 * VA + 140 - uA + I_total_A)
        VB += tau * (0.04 * VB**2 + 5 * VB + 140 - uB + I_total_B)

        uA += tau * a * (b * VA - uA)
        uB += tau * a * (b * VB - uB)

        # Updated traces AND y values here for the next iteration.
        if VA >= 30:
            VA_trace.append(30)
            VA = c
            uA += d
            spikes_A.append(1)
            yA_prev = 1
        else:
            VA_trace.append(VA)
            spikes_A.append(0)
            yA_prev = 0

        if VB >= 30:
            VB_trace.append(30)
            VB = c
            uB += d
            spikes_B.append(1)
            yB_prev = 1
        else:
            VB_trace.append(VB)
            spikes_B.append(0)
            yB_prev = 0

    return VA_trace, VB_trace, spikes_A, spikes_B

# Functino to plot all graphs for
# chattering neurons with different values of W
def plot_chattering_neurons():
    Ws = [0, 15, 30, 45, 60]
    plt.figure(figsize=(12, 10))

    for i, W in enumerate(Ws, start=1):
        VA, VB, _, _ = run_talking_neurons_simulation(W)
        plt.subplot(len(Ws), 1, i)
        plt.plot(tspan, VA, label="Neuron A (Excitatory)")
        plt.plot(tspan, VB, label="Neuron B (Inhibitory)")
        plt.title(f"Two-Neuron Network (Chattering Neurons), W = {W}")
        plt.xlabel("Time")
        plt.ylabel("Vm")
        plt.legend()
        plt.grid(True)

    plt.tight_layout()
    plt.show()


# Generate RvI data for either kind of neuron
def generate_RvI_data(neuron_type='fast'):
    a, b, c, d = get_neuron_params(neuron_type)
    u = b * V

    avg_spike_count_list = []
    for I in range(0, 61, 2):
        spike_ts, uu, VV, avg_spike_count, spike_count = simulation_block(
            a, b, c, d, V, u, I_input=I
        )
        avg_spike_count_list.append({"I_input": I, "avg_spike_count": avg_spike_count})

    avg_spike_count_df = pd.DataFrame(avg_spike_count_list)
    filename = f"./AVG_R_VALUES_{'FS' if neuron_type == 'fast' else 'RS'}.csv"
    avg_spike_count_df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")


# Function to plot voltage traces for either type of neuron
def plot_voltage_traces(neuron_type='fast'):
    a, b, c, d = get_neuron_params(neuron_type)
    u = b * V

    I_input_vals = [1, 10, 20, 30, 40, 50, 60]
    VV_list = []
    I_values = []

    for I in I_input_vals:
        spike_ts, uu, VV, avg_spike_count, spike_count = simulation_block(
            a, b, c, d, V, u, I_input=I
        )
        VV_list.append(VV)
        I_values.append(I)

    plot_subgraphs(VV_list, tspan, steps, I_values)


# Helper function to get neuron type
def get_neuron_type_input():
    while True:
        print("\nSelect neuron type:")
        print("1. Fast Spiking")
        print("2. Regular Spiking")
        choice = input("Enter choice (1-2): ").strip()

        if choice == '1':
            return 'fast'
        elif choice == '2':
            return 'regular'
        else:
            print("Invalid choice. Please enter 1 or 2.")


# Function to display menu for interface
def display_menu():
    print("\n" + "="*50)
    print("NEURON SIMULATION MENU")
    print("="*50)
    print("1. Generate R vs I Data")
    print("2. Plot R vs I Comparison")
    print("3. Plot Voltage Traces")
    print("4. Plot Chattering Neurons")
    print("5. Exit")
    print("="*50)


if __name__ == "__main__":
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == '1':
            neuron_type = get_neuron_type_input()
            generate_RvI_data(neuron_type)
        elif choice == '2':
            plot_RvI_comparison()
        elif choice == '3':
            neuron_type = get_neuron_type_input()
            plot_voltage_traces(neuron_type)
        elif choice == '4':
            plot_chattering_neurons()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")