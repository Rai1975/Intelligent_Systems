from matplotlib import pyplot as plt
import numpy as np

############# PARAMETERS ##############
steps = 1000
a = 0.02
b = 0.25
c = -65.0
d = 6

V = -64.0
u = b*V

VV = []
uu = []
tau = 0.25

tspan = np.arange(0, steps + tau, tau)

T1 = 0
spike_ts = []

#### SIMULATION TIME ###
for t in tspan:
    if (t > T1):
        I = 1
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


######## Plotting ##########
plt.figure(figsize=(10, 8))
plt.subplot(2, 1, 1)
plt.plot(tspan, VV)
plt.axis([0, np.max(tspan), -90, 40])
plt.xlabel('time step')
plt.ylabel('$V_m$')
plt.title('Regular Spiking')
plt.xticks([0, np.max(tspan)], labels=[0, steps])
plt.grid(True)
plt.tight_layout()
plt.show()

print(len(VV))

count = 0
for i in spike_ts:
    if i == 1:
        count += 1

print(count)