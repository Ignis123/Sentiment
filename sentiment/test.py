import matplotlib.pyplot as plt
from mpld3 import fig_to_html, plugins
fig, ax = plt.subplots()
points = ax.plot(range(10), 'o')
plugins.connect(fig, plugins.PointLabelTooltip(points[0]))
fig_to_html(fig)