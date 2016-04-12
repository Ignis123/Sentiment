#import matplotlib.animation as animation
from matplotlib import style
import matplotlib.pyplot as plt

style.use("ggplot")

myFigure = plt.figure()
ax1 = myFigure.add_subplot(1, 1, 1)


#def animate(i):
pullData = open("graph_data.txt","r").read()
lines = pullData.split('\n')

xArray = []
yArray = []

x = 0
y = 0

for l in lines:
    x += 1
    if "positive" in l:
        y += 1
    elif "negative" in l:
        y -= 1

    xArray.append(x)
    yArray.append(y)

ax1.clear()
ax1.plot(xArray, yArray)

#ani = animation.FuncAnimation(myFigure, animate, interval=1000)

# while(window.isOpen()
# -> Run Command
fig1 = plt.gcf()
fig1.savefig('static/css/images/my_graph.png', interval=1000)
# i = 0
# while os.path.exists('{}{:d}.png'.format('static/css/images/my_graph', i)):
#     i += 1
# plt.savefig('{}{:d}.png'.format('static/css/images/my_graph', i))