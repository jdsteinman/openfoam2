import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Read data
with open("./unsteady/postProcessing/probes/0/U") as f:
    clean_lines = (line.replace('(',' ').replace(')',' ') for line in f)
    U = np.loadtxt(clean_lines, dtype=float, comments='#')

p = np.loadtxt("./unsteady/postProcessing/probes/0/p", dtype=float, comments='#')

# Plot Data
fsize = 15
tsize = 18
tdir = 'in'
major = 5.0
minor = 3.0
lwidth = 2.0
lhandle = 2.0
plt.style.use('seaborn-whitegrid')
plt.rcParams['font.size'] = fsize
plt.rcParams['legend.fontsize'] = tsize
plt.rcParams['xtick.direction'] = tdir
plt.rcParams['ytick.direction'] = tdir
plt.rcParams['xtick.major.size'] = major
plt.rcParams['xtick.minor.size'] = minor
plt.rcParams['ytick.major.size'] = 5.0
plt.rcParams['ytick.minor.size'] = 5.0
plt.rcParams['axes.linewidth'] = lwidth
plt.rcParams['legend.handlelength'] = lhandle
colors = [mpl.cm.tab10(i) for i in range(6)]


# (x,y) = (5.5,-0.5)
fig, ax = plt.subplots(3,1, sharex=True)
ax[0].plot(p[:,0], p[:,1], c=colors[0], label="p/pU^2")
ax[0].set_title("Probe at (x,y)=(5.5,-0.5)")
ax[0].set_ylabel("Normalized Pressure")
ax[0].legend(loc=5)

# fig2, ax2 = plt.subplots(1,1)
ax[1].plot(U[:,0], U[:,1], c=colors[1], label="u/U")
ax[1].set_ylabel("Normalized Velocity")
ax[1].legend(loc=1)

# fig3, ax3 = plt.subplots(1,1)
ax[2].plot(U[:,0], U[:,2],  c=colors[2], label="v/U")
ax[2].set_xlabel("Normalized Time t/(D/U)")
ax[2].set_ylabel("Normalized Velocity")
ax[2].legend(loc=1)


# (x,y) = (5.5,0.5)
fig2, ax2 = plt.subplots(3,1, sharex=True)
ax2[0].plot(p[:,0], p[:,2], c=colors[1], label="p/pU^2")
ax2[0].set_title("Probe (x,y)=(5.5,0.5)")
ax2[0].set_ylabel("Normalized Pressure")
ax2[0].legend(loc=1)

# fig5, ax5 = plt.subplots(1,1)
ax2[1].plot(U[:,0], U[:,4], c=colors[4], label="u/U")
ax2[1].set_ylabel("Normalized Velocity")
ax2[1].legend(loc=5)

ax2[2].plot(U[:,0], U[:,5], c=colors[5], label="v/U")
ax2[2].set_xlabel("Normalized Time t/(D/U)")
ax2[2].set_ylabel("Normalized Velocity")
ax2[2].legend(loc=1)

plt.show()