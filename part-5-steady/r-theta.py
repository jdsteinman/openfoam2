import numpy as np
import matplotlib.pyplot as plt

from math import pi, cos, sin, sqrt

## Import data
path1 = "../data/coarse/steady/postProcessing/singleGraph/40/"
path2 = "../data/fine/steady1/postProcessing/singleGraph/40/"
path3 = "../data/fine/steady2/postProcessing/singleGraph/40/"
path4 = "../data/fine/steady3/postProcessing/singleGraph/40/"
paths = [path1, path2, path3, path4]
files = ["lineP_4_U.xy","lineP_2_U.xy","line3P_4_U.xy"]
labels = ["A", "B", "C", "D", "E"]
angles = ["45deg", "90deg", "135deg"]

e_rr_ = []
e_rt_ = []
delta_ = []

# Set up plots
fig,  ax  = plt.subplots(3,1, sharex=True)  # Ur Plot
fig2, ax2 = plt.subplots(3,1, sharex=True)  # Ut Plot
colors = plt.get_cmap('tab10')

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
plt.rcParams['lines.linestyle'] = '-'
plt.rcParams["xtick.labelsize"] = fsize
plt.rcParams["ytick.labelsize"] = fsize
plt.rcParams['legend.handlelength'] = lhandle

for j, p in enumerate(paths):

    for i, f in enumerate(files):
        Uxy = np.loadtxt(p + f)

        # Convert to r-theta velocity
        theta = [pi/4, pi/2, 3*pi/4]
        Ur = []
        Ut = []
        R = []

        for row in Uxy:
            r = (row[0]**2+row[1]**2)**0.5 - 0.5
            R.append(r)

            ux = row[3]
            uy = row[4]
            Ur.append(cos(theta[i])*ux + sin(theta[i])*uy)
            Ut.append(sin(theta[i])*ux - cos(theta[i])*uy ) 

        R = np.array(R)
        Ur = np.array(Ur)
        Ut = np.array(Ut)

        # strain tensors
        e_rr = np.gradient(Ur, r, edge_order=2)
        e_rt = 0.5*r*np.gradient(Ut/r, r, edge_order=2)

        e_rr_.append(e_rr[0])
        e_rt_.append(e_rt[0])

        # Deltas
        d1 = (R[0]+R[1])/2 - R[0]
        d2 = (R[1]+R[2])/2 - R[1]
        delta = sqrt(d1*d2)
        delta_.append(delta)

        # Plot
        ax[i].plot(R, Ur, c=colors(3*j), label=labels[j])
        ax2[i].plot(R, Ut, c=colors(3*j+1), label=labels[j])

        print("============================================")
        print("File: " + p + f)
        print("e_rr = ", e_rr[0])
        print("e_rt = ", e_rt[0])

    # Length of Recirculation Region
    Ux = np.loadtxt(p + "line0_U.xy")
    x = Ux[:,0]
    Ux = Ux[:,3]
    L = 0 
    for i, ux in enumerate(Ux):
        if ux > 0:
            h = x[i]-x[i-1]
            dudx = (Ux[i]-Ux[i-1]) / h
            L = x[i] - Ux[i]/dudx
            break

    print("L/D =  ",  L)

e_rr_ = np.array(e_rr_)
e_rt_ = np.array(e_rt_)
delta_ = np.array(delta_)

e_rr_ =  e_rr_.reshape((-1,3))
e_rt_ =  e_rt_.reshape((-1,3))
delta_ = delta_.reshape((-1,3))

# Plot formats
fig.suptitle(r"$U_r$ along various directions", fontsize=25)

ax[0].set_title(r"$\theta=45^{\circ}$")
ax[1].set_title(r"$\theta=90^{\circ}$")
ax[2].set_title(r"$\theta=135^{\circ}$")

ax[0].set_ylabel(r"Normalized $U_r$")
ax[1].set_ylabel(r"Normalized $U_r$")
ax[2].set_ylabel(r"Normalized $U_r$")

ax[2].set_xlabel(r"Normalized Distance from Cylinder, r")

ax[0].legend()
ax[1].legend()
ax[2].legend()

ax[0].xaxis.set_tick_params(labelbottom=True)
ax[1].xaxis.set_tick_params(labelbottom=True)
ax[2].xaxis.set_tick_params(labelbottom=True)

fig2.suptitle(r"$U_{theta}$ along various directions", fontsize=25)

ax2[0].set_title(r"$\theta=45^{\circ}$")
ax2[1].set_title(r"$\theta=90^{\circ}$")
ax2[2].set_title(r"$\theta=135^{\circ}$")

ax2[0].set_ylabel(r"Normalized $U_{theta}$")
ax2[1].set_ylabel(r"Normalized $U_{theta}$")
ax2[2].set_ylabel(r"Normalized $U_{theta}$")

ax2[2].set_xlabel(r"Normalized Distance from Cylinder, r")

ax2[0].legend()
ax2[1].legend()
ax2[2].legend()

ax2[0].xaxis.set_tick_params(labelbottom=True)
ax2[1].xaxis.set_tick_params(labelbottom=True)
ax2[2].xaxis.set_tick_params(labelbottom=True)

# Plot Deltas
fig3, ax3 = plt.subplots(1,1)
fig4, ax4 = plt.subplots(1,1)
for i in range(3):
    ax3.plot(1/delta_[:,i], e_rr_[:,i], label=r"$e_{rr}$ "+angles[i])
    ax3.plot(1/delta_[:,i], e_rt_[:,i], label=r"$e_{r\theta}$ "+angles[i])

    ax4.loglog(1/delta_[:,i], e_rr_[:,i], label=r"$e_{rr}$ "+angles[i])
    ax4.loglog(1/delta_[:,i], e_rt_[:,i], label=r"$e_{r\theta}$ "+angles[i])

ax3.set_title("Strain tensors at wall")
ax3.set_xlabel(r"Mesh Resolution, $1/\delta$")
ax3.set_ylabel("Strain")
ax3.legend()

ax4.set_title("Strain tensors at wall")
ax4.set_xlabel(r"Mesh Resolution, $1/\delta$")
ax4.set_ylabel("Strain")
ax4.legend()
plt.show()
