import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from datetime import date


# Parameters #############################################

Lf = 4.0
Lw = 6.0
R  = 1.0
H  = 4.0
res = 1.0

##########################################################

file_name = "blockMeshDict" 
f = open(file_name, "w+")
np.set_printoptions(precision=8)

## Comments
f.write("// Mesh generated on {}\n\n".format(date.today()))
f.write("// Lf (fore)  = {}\n".format(Lf))
f.write("// Lw (wake)  = {}\n".format(Lw))
f.write("// R  (outer) = {}\n".format(R))
f.write("// H  (top/bottom) = {}\n".format(H))
f.write("// res = {}\n".format(res))

# Header
f.write("FoamFile\n")
f.write("{\n")
f.write("    version  2.0;\n")
f.write("    format   ascii;\n")
f.write("    class    dictionary;\n")
f.write("    object   blockMeshDict;\n")
f.write("}\n\n")

f.write("convertToMeters {};\n\n".format(1.0))

# Vertices
vert = np.array([
    [0.5, 0, -0.05], # 0
    [0.5*sqrt(2)/2, 0.5*sqrt(2)/2, -0.05], # 1
    [0, 0.5, -0.05], # 2
    [-0.5*sqrt(2)/2, 0.5*sqrt(2)/2, -0.05], # 3
    [-0.5, 0, -0.05], # 4
    [-0.5*sqrt(2)/2, -0.5*sqrt(2)/2, -0.05], # 5
    [0, -0.5, -0.05], # 6
    [0.5*sqrt(2)/2, -0.5*sqrt(2)/2, -0.05], # 7

    [R, 0, -0.05], # 8
    [R*sqrt(2)/2, R*sqrt(2)/2, -0.05], # 9
    [0, R, -0.05], # 10
    [-R*sqrt(2)/2, R*sqrt(2)/2, -0.05], # 11
    [-R, 0, -0.05], # 12
    [-R*sqrt(2)/2, -R*sqrt(2)/2, -0.05], # 13
    [0, -R, -0.05], # 14
    [R*sqrt(2)/2, -R*sqrt(2)/2, -0.05], # 15

    [Lw, 0, -0.05], # 16
    [Lw, R*sqrt(2)/2, -0.05], # 17
    [Lw, H, -0.05], # 18
    [R*sqrt(2)/2, H, -0.05], # 19
    [0, H, -0.05], # 20
    [-R*sqrt(2)/2, H, -0.05], # 21
    [-Lf, H, -0.05], # 22
    [-Lf, R*sqrt(2)/2, -0.05], # 23
    
    [-Lf, 0, -0.05], # 24
    [-Lf, -R*sqrt(2)/2, -0.05], # 25
    [-Lf, -H, -0.05], # 26
    [-R*sqrt(2)/2, -H, -0.05], # 27
    [0, -H, -0.05], # 28
    [R*sqrt(2)/2, -H, -0.05], # 29
    [Lw, -H, -0.05], # 30
    [Lw, -R*sqrt(2)/2, -0.05] # 31
])

vert = np.vstack((vert, vert))
vert[32:,2] += 0.1

# Write Vertices
f.write("vertices\n")
f.write("(\n")
for i, row in enumerate(vert):
    f.write("    ( ")
    f.write("  ".join(map("{: .10e}".format, row)))
    # f.write(")\n")
    f.write(") // {0} \n".format(i))
f.write(");\n\n")


# Blocks
blocks = np.array([
    [0, 8, 9, 1, 32, 40, 41, 33],
    [1, 9, 10, 2, 33, 41, 42, 34],
    [2, 10, 11, 3, 34, 42, 43, 35],
    [3, 11, 12, 4, 35, 43, 44, 36],
    [4, 12, 13, 5, 36, 44, 45, 37],
    [5, 13, 14, 6, 37, 45, 46, 38],
    [6, 14, 15, 7, 38, 46, 47, 39],
    [7, 15, 8, 0, 39, 47, 40, 32],
    [8, 16, 17, 9, 40, 48, 49, 41],
    [9, 17, 18, 19, 41, 49, 50, 51],
    [10, 9, 19, 20, 42, 41, 51, 52],
    [11, 10, 20, 21, 43, 42, 52, 53],
    [23, 11, 21, 22, 55, 43, 53, 54],
    [24, 12, 11, 23, 56, 44, 43, 55],
    [25, 13, 12, 24, 57, 45, 44, 56],
    [26, 27, 13, 25, 58, 59, 45, 57],
    [27, 28, 14, 13, 59, 60, 46, 45],
    [28, 29, 15, 14, 60, 61, 47, 46],
    [29, 30, 31, 15, 61, 62, 63, 47],
    [15, 31, 16, 8, 47, 63, 48, 40]
])

ncells = np.array([
    [20, 20, 1],
    [20, 20, 1],
    [20, 20, 1],
    [20, 20, 1],
    [20, 20, 1],
    [20, 20, 1],
    [20, 20, 1],
    [20, 20, 1],
    [30, 20, 1],
    [30, 30, 1],
    [20, 30, 1],
    [20, 30, 1],
    [15, 30, 1],
    [15, 20, 1],
    [15, 20, 1],
    [15, 30, 1],
    [20, 30, 1],
    [20, 30, 1],
    [30, 30, 1],
    [30, 20, 1],
]) 
ncells[:,0:2] = np.around(ncells[:,0:2] * res)
ncells = ncells.astype(int)

grading = np.array([
    [2.0, 1.0, 1.0],
    [2.0, 1.0, 1.0],
    [2.0, 1.0, 1.0],
    [2.0, 1.0, 1.0],
    [2.0, 1.0, 1.0],
    [2.0, 1.0, 1.0],
    [2.0, 1.0, 1.0],
    [2.0, 1.0, 1.0],
    [4.0, 1.0, 1.0],
    [4.0, 4.0, 1.0],
    [1.0, 4.0, 1.0],
    [1.0, 4.0, 1.0],
    [0.25, 4.0, 1.0],
    [0.25, 1.0, 1.0],
    [0.25, 1.0, 1.0],
    [0.25, 0.25, 1.0],
    [1.0, 0.25, 1.0],
    [1.0, 0.25, 1.0],
    [4.0, 0.25, 1.0],
    [4.0, 1.0, 1.0],
])

# Write Blocks
f.write("blocks\n")
f.write("(\n")
for i, (block, n, grad) in enumerate(zip(blocks, ncells, grading)):
    # Connectivity
    f.write("    // block {}\n".format(i))
    f.write("    hex (")
    f.write(" ".join(map(str, block)))
    f.write(") ")

    # Number of Cells
    f.write("(")
    f.write(" ".join(map(str, n)))
    f.write(") ")

    # Grading
    f.write(" simpleGrading ")
    f.write("(")
    f.write(" ".join(map(str, grad)))
    f.write(")\n\n")

f.write(");\n\n")

# Edges
edges = np.array([
    [0, 1],
    [8, 9],
    [32, 33],
    [40, 41],
    [1, 2], 
    [9, 10],
    [33, 34],
    [41, 42],
    [2, 3],
    [10, 11],
    [34, 35],
    [42, 43],
    [3, 4],
    [11, 12],
    [35, 36],
    [43, 44],
    [4, 5],
    [12, 13],
    [36, 37],
    [44, 45],
    [5, 6],
    [13, 14],
    [37, 38],
    [45, 46],
    [6, 7],
    [14, 15],
    [38, 39],
    [46, 47],
    [7, 0],
    [15, 8],
    [39, 32],
    [47, 40]
])

# Extra points
epoints = np.array([
    [0.5*sqrt(3)/2, 0.5/2, -0.05],
    [R*sqrt(3)/2, R/2, -0.05],
    [0.5*sqrt(3)/2, 0.5/2, 0.05],
    [R*sqrt(3)/2, R/2, 0.05],

    [0.5/2, 0.5*sqrt(3)/2, -0.05],
    [R/2, R*sqrt(3)/2, -0.05],
    [0.5/2, 0.5*sqrt(3)/2, 0.05],
    [R/2, R*sqrt(3)/2, 0.05],

    [-0.5/2, 0.5*sqrt(3)/2, -0.05],
    [-R/2, R*sqrt(3)/2, -0.05],
    [-0.5/2, 0.5*sqrt(3)/2, 0.05],
    [-R/2, R*sqrt(3)/2, 0.05],

    [-0.5*sqrt(3)/2, 0.5/2, -0.05],
    [-R*sqrt(3)/2, R/2, -0.05],
    [-0.5*sqrt(3)/2, 0.5/2, 0.05],
    [-R*sqrt(3)/2, R/2, 0.05],

    [-0.5*sqrt(3)/2, -0.5/2, -0.05],
    [-R*sqrt(3)/2, -R/2, -0.05],
    [-0.5*sqrt(3)/2, -0.5/2, 0.05],
    [-R*sqrt(3)/2, -R/2, 0.05],

    [-0.5/2, -0.5*sqrt(3)/2, -0.05],
    [-R/2, -R*sqrt(3)/2, -0.05],
    [-0.5/2, -0.5*sqrt(3)/2, 0.05],
    [-R/2, -R*sqrt(3)/2, 0.05],

    [0.5/2, -0.5*sqrt(3)/2, -0.05],
    [R/2, -R*sqrt(3)/2, -0.05],
    [0.5/2, -0.5*sqrt(3)/2, 0.05],
    [R/2, -R*sqrt(3)/2, 0.05],

    [0.5*sqrt(3)/2, -0.5/2, -0.05],
    [R*sqrt(3)/2, -R/2, -0.05],
    [0.5*sqrt(3)/2, -0.5/2, 0.05],
    [R*sqrt(3)/2, -R/2, 0.05]
])


# Write Edges
f.write("edges\n")
f.write("(\n")
for i, (edge, point) in enumerate(zip(edges, epoints)):

    f.write("    arc ")
    f.write(" ".join(map(str, edge)))

    f.write(" (")
    f.write("  ".join(map("{:.10e}".format, point)))
    f.write(")\n")

f.write(");\n\n")

# Boundaries

inlet = np.array([
    [22, 54, 55, 23],
    [23, 55, 56, 24],
    [24, 56, 57, 25],
    [25, 57, 58, 26]
])

outlet = np.array([
    [18, 50, 49, 17],
    [17, 49, 48, 16],
    [16, 48, 63, 31],
    [31, 63, 62, 30]
])

cylinder = np.array([
    [0, 32, 33, 1],
    [1, 33, 34, 2],
    [2, 34, 35, 3],
    [3, 35, 36, 4],
    [4, 36, 37, 5],
    [5, 37, 38, 6],
    [6, 38, 39, 7],
    [7, 39, 32, 0]
])

top = np.array([
    [22, 54, 53, 21],
    [21, 53, 52, 20],
    [20, 52, 51, 19],
    [19, 51, 50, 18]
])

bottom = np.array([
    [26, 58, 59, 27],
    [27, 59, 60, 28],
    [28, 60, 61, 29],
    [29, 61, 62, 30]
])


boundaries=[inlet, outlet, cylinder, top, bottom]
bnames = ["inlet","outlet","cylinder","top","bottom"]
btypes = ["patch", "patch", "wall", "symmetryPlane", "symmetryPlane"]

# Write Boundaries
f.write("boundary\n")
f.write("(\n")
for i, (name, arr, btype) in enumerate(zip(bnames, boundaries, btypes)):
    f.write("    {}\n".format(name))
    f.write("    {\n")
    f.write("        type {};\n".format(btype))
    f.write("        faces\n")
    f.write("        (\n")

    for row in arr:
        f.write("            (")
        f.write(" ".join(map(str, row)))
        f.write(")\n")

    f.write("        );\n")
    f.write("    }\n\n")

f.write(");")
f.close()

# plots
fig, ax = plt.subplots(1,1)
ax.set_title('Mesh Vertices')

# Edit the font, font size, and axes widthmpl.rcParams['font.family'] = 'Avenir'
plt.rcParams['font.size'] = 18
plt.rcParams['axes.linewidth'] = 2

# Vertices
ax.scatter(vert[:,0], vert[:,1], c='k')
# for i in range(32):
#     s1 = str(i) 
#     s2 = "(" + str(i+32) + ")"
#     ax.text(vert[i,0]+.05, vert[i,1], s1, c='r', fontsize=8)
#     ax.text(vert[i,0]+.15, vert[i,1], s2, c='b', fontsize=8)


ax.scatter(epoints[:,0], epoints[:,1], c='r')
# for j, pt in enumerate(epoints):
#     if pt[2] == 0.5:
#         ax.annotate(str(j), (pt[0], pt[1]), fontsize=8)    

plt.show()
