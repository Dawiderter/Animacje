import model
import matplotlib.pyplot as plt
import numpy as np
from typing import List

#Prawa granica wykresu
MAX_T = 100
#Krok czasu, im większy, tym większa dokładność
T_STEP = 0.01

t_array : List[float] = []
del_b_array : List[int] = []
del_x_array : List[float] = []
max_x_array : List[float] = []
min_x_array : List[float] = []
x_array : List[float] = []

found = False

t = 0
while t <= MAX_T:
    t_array.append(t)
    model.update_pos(t)
    (min_x, max_x) = model.get_min_max_x()
    del_x_array.append(max_x - min_x)
    if (max_x - min_x) > 0.99 and not found:
        print(t)
        found = True
    x_array.append(model.Cache[model.DEFAULT_NUM][1])
    min_x_array.append(min_x)
    max_x_array.append(max_x)

    t = t + T_STEP

t_points = np.array(t_array)
del_x_points = np.array(del_x_array)
x_points = np.array(x_array)
min_x_points = np.array(min_x_array)
max_x_points = np.array(max_x_array)

plt.subplot(2,1,1)
plt.plot(t_points, del_x_points)
plt.title("Niepewność pozycji", loc="left")
plt.xlabel("Czas [s]")
plt.ylabel("Maksymalny błąd pozycji [m]")
plt.xlim(0,MAX_T)
plt.ylim(0,1)
plt.grid()

plt.subplot(2,1,2)
plt.plot(t_points, x_points, linewidth = '2', label = 'X dla v = 1 m/s')
plt.plot(t_points, min_x_points, ls = '--', color = 'red', label = 'Minimalny X')
plt.plot(t_points, max_x_points, ls = '--', color = 'green', label = 'Maksymalny X')
plt.title("Granice pozycji", loc="left")
plt.xlabel("Czas [s]")
plt.ylabel("Pozycja [m]")
plt.xlim(0,MAX_T)
plt.ylim(0,1)
plt.legend()
plt.grid()

plt.suptitle(f"δv = {model.MAX_ERROR} [m/s]")

plt.show()



