import numpy as np
from numpy import sqrt, power, max as npmax, min as npmin



# funckja zwraca dwa wektory x i y, które mają w sobie odpowiednio współrzędnie x i y i'tego miasta we wczytanyach danych
# współrzędne we floatach bo jest 2137.0, można zmienić na int ale nie bawiłem się tym
# city_list -> odczyt pliku, start -> od której linijki pliku ma czytać bo najpierw są jakieś informacje
# len(city_list) - 1 bo ostatnia linijka pomijana("EOF")
def get_coordinates(city_list, start):
    x = []
    y = []

    for i in range(start, len(city_list) - 1):
        k = city_list[i].split()
        x.append(float(k[1]))
        y.append(float(k[2]))

    return x, y

# funkcja zwraca dystans pomiedzy punktami znajdującymi się we wprowadzonych współrzędnych
def get_distance(x1, y1, x2, y2):
    distance = int(0.5 + sqrt(power((x1 - x2), 2) + power((y1 - y2), 2)))

    return distance

# funkcja zwraca długość trasy na podstawie kolejności oraz tablicy odleglosci
def get_tour_distance(order, dist_mat):
    tour_distance = 0

    for i in range(0, len(order) - 1):
        tour_distance = tour_distance + dist_mat[order[i], order[i + 1]]

    return tour_distance

# funkcja zwraca array o wymiara n x n, zawierający odległości pomiędzy poszczególnymi punktami
# tarray(i, j) -> i to wiersz, j to kolumna
def get_distance_table(x, y):
    n = len(x)
    distance_matrix = np.zeros((n, n), int)

    for i in range(0, n, 1):
        for j in range(0, n, 1):
            distance_matrix[i, j] = get_distance(x[i], y[i], x[j], y[j])

    return distance_matrix

# funkcja zwraca kolejność odiwedzanych miast odczytaną z pliku z optymalną kolejnością
def get_optimal_order(order_opt_list):
    order_opt = []

    for i in range(4, len(order_opt_list) - 1, 1):
        order_opt.append(int(order_opt_list[i]) - 1)

    order_opt.append(int(order_opt_list[4]) - 1)

    return order_opt
