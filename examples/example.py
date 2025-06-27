import matplotlib.pyplot as plt
import sys

from matplotlib.patches import Circle, Rectangle

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111)

ax.add_patch( Circle((1,1), radius=0.1, color='b', alpha=0.3) )

ax.set_title("This is a title")

plt.show()
