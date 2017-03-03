import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

x = [0,0]
total_energy = [2,2]

fig, ax = plt.subplots()
line, = ax.plot(x, total_energy, color='k')



def update(num, x, total_energy, line):
    new_x = np.array([num])
    x = np.append(x,new_x)

    print(x)
    
    new_energy = np.array([2])
    total_energy = np.append(total_energy,new_energy)

    print(total_energy)

    print(num)


    line.set_data(x[:num], total_energy[:num])
    line.axes.axis([0, 10, 0, 3])
    return line,

ani = animation.FuncAnimation(fig, update, len(x), fargs=[x, total_energy, line],
                              interval=25, blit=True)

plt.show()