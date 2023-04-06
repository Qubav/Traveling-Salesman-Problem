import numpy as np
from numpy import sqrt, power, max as npmax, min as npmin
from random import randint, sample

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

# funkcja zwraca n losowych int'ów bez powtórzeń z przedziału r
def get_random_locations(r, n):
    locations = sample(range(r), n)

    return locations

# funkcja zwraca odległość punktu E od odcinka pomiędzy punktami A i B
def get_min_distance_from_edge(A, B, E) :

    AB = [None, None]
    AB[0] = B[0] - A[0]
    AB[1] = B[1] - A[1]

    BE = [None, None]
    BE[0] = E[0] - B[0]
    BE[1] = E[1] - B[1]

    AE = [None, None]
    AE[0] = E[0] - A[0]
    AE[1] = E[1] - A[1]

    AB_BE = AB[0] * BE[0] + AB[1] * BE[1]
    AB_AE = AB[0] * AE[0] + AB[1] * AE[1]
    reqAns = 0

    if (AB_BE > 0) :

        y = E[1] - B[1]
        x = E[0] - B[0]
        reqAns = sqrt(x * x + y * y)

    elif (AB_AE < 0) :
        y = E[1] - A[1]
        x = E[0] - A[0]
        reqAns = sqrt(x * x + y * y)

    else:
        x1 = AB[0]
        y1 = AB[1]
        x2 = AE[0]
        y2 = AE[1]
        mod = sqrt(x1 * x1 + y1 * y1)
        reqAns = abs(x1 * y2 - y1 * x2) / mod

    return reqAns

# funkcja zwraca kolejność odiwedzanych miast odczytaną z pliku z optymalną kolejnością
def get_optimal_order(order_opt_list):
    order_opt = []

    for i in range(4, len(order_opt_list) - 1, 1):
        order_opt.append(int(order_opt_list[i]) - 1)

    order_opt.append(int(order_opt_list[4]) - 1)

    return order_opt

# funkcja zwraca kolejność miast stworzoną przy wykorzystaniu algorytmu budującego farthest insertion
# input x i y to aaray'e z odpowiednio koordynatami x i y kolejnych miast, dist_mat to tabela odległości miast między sobą
def FI_algorithm(x, y, dist_mat):
    order = []                              # kolejność odwiedzania miast
    visited = [] 
    three_random = True

    if(three_random is True):
            ln = 3                                  # localisations number
            ftrl = get_random_locations(len(x), ln)      # fisrt three random localisatons
                                    # odziedzione lokalizacje, jeśli punkt został już odwiedzony to w komórce o jego numerze jest True, jeśli nie wtedy jest False

            for i in range(0, len(x)):
                visited.append(False)

            for i in range(0, ln):
                order.append(ftrl[i])
                visited[ftrl[i]] = True

            order.append(ftrl[0])
    
    elif(three_random is False):
        for i in range(0, len(x)):
                visited.append(False)

        max_found = False
        max_dist = npmax(dist_mat[:, :])
        for i in range(0, len(x)):
            for j in range(i + 1, len(x)):
                if(dist_mat[i, j] == max_dist):
                    order.append(i)
                    order.append(j)
                    order.append(i)
                    visited[i] = True
                    visited[j] = True
                    max_found = True
                
                if(max_found is True):
                    break
            if(max_found is True):
                break
        
        max_val = 0
        for i in range(0, len(order) - 1):   # wybór najdalej oddalonego miasta, które nie zostało odwiedzone, od miast już odiwedzonych | len(order) - 1 ponieważ na ostatnim miejscu w kolejności występuje miasto z pierwszego miejsca
            for j in range(0, len(x)):
                if(visited[j] is False):
                    if(max_val < dist_mat[order[i], j]):
                        max_val = dist_mat[order[i], j]
                        next_to_append = j
        
        order.insert(2, next_to_append)
        visited[next_to_append] = True

    for k in range(0, len(x) - 3):
        max_val = 0
        for i in range(0, len(order) - 1):   # wybór najdalej oddalonego miasta, które nie zostało odwiedzone, od miast już odiwedzonych | len(order) - 1 ponieważ na ostatnim miejscu w kolejności występuje miasto z pierwszego miejsca
            for j in range(0, len(x)):
                if(visited[j] is False):
                    if(max_val < dist_mat[order[i], j]):
                        max_val = dist_mat[order[i], j]
                        next_to_append = j

        shortest_distance = max_val

        for i in range(0, len(order) - 1):
            A = [x[order[i]], y[order[i]]]
            B = [x[order[i + 1]], y[order[i + 1]]]
            P = [x[next_to_append], y[next_to_append]]
            D = get_min_distance_from_edge(A, B, P)
            if(D < shortest_distance):
                shortest_distance = D
                place = i + 1

            elif(D == shortest_distance):   # w przypadku gdy najmniejsza odelgłość jest równa dla dwóch krawędzi(odległość od punktu gdzie te krawędzie się łączą), sprawdzane są długości tras
                place2 = i + 1              # dla obu przypadków i punkt włączany jest do tej krawędzi, do której włączenie go zapewni krótszą trasę
                order_copy1 = order.copy()
                order_copy2 = order.copy()
                order_copy1.insert(place, next_to_append)
                order_copy2.insert(place2, next_to_append)
                td1 = get_tour_distance(order_copy1, dist_mat)
                td2 = get_tour_distance(order_copy2, dist_mat)
                if(td1 > td2):
                    place = place2

        order.insert(place, next_to_append)
        visited[next_to_append] = True

    return order

# funkcja zwraca wartość zmiany długości trasy po zamianie
def distance_change(dist_mat, n1, n2, n3, n4):
    change = dist_mat[n1, n3] + dist_mat[n2, n4] - dist_mat[n1, n2] - dist_mat[n3, n4]

    return change

def check_Tabu(new_candidate, Tabu):

    for i in range(0, len(Tabu)):
        city0 = Tabu[i][0]
        city1 = Tabu[i][1]
        city1_index = new_candidate.index(city1)
        if(new_candidate[city1_index - 1] == city0  or new_candidate[city1_index + 1] == city0):
            return True
    
    return False

# funkcja przegląda wartość funkcji zmiany długości trasy dla wszystkich sąsiadów, zwraca najlepszą kolejność oraz między którymi miastami zamiana krawędzi miała miejsce
def get_best_neighbor(order_, base_distance, dist_mat, best_solution_distance_, Tabu):
    best_solution_distance = best_solution_distance_
    best = order_.copy()
    order = order_.copy()
    min_dist_change = base_distance
    Tabu_indx = -1

    for i in range(1, len(order) - 2):
        for j in range(i + 2, len(order)):

            new_dist_change = distance_change(dist_mat, order[i - 1], order[i], order[j - 1], order[j])

            if(new_dist_change < min_dist_change):
                new_candidate = order.copy()
                new_candidate[i:j] = new_candidate[j - 1: i - 1: -1]
                Tabu_val = check_Tabu(new_candidate, Tabu)

                if(Tabu_val is False):
                    min_dist_change = new_dist_change
                    best = new_candidate
                    new_tour_distance = base_distance + new_dist_change
                    Tabu_indx = i

                    if((new_dist_change + base_distance) < best_solution_distance):
                        best_solution_distance = base_distance + new_dist_change

            if((new_dist_change + base_distance) < best_solution_distance):
                min_dist_change = new_dist_change
                best = order.copy()
                best[i:j] = best[j - 1: i - 1: -1]
                best_solution_distance = base_distance + new_dist_change
                new_tour_distance = base_distance + new_dist_change
                Tabu_indx = i
    
    if(Tabu_indx == -1):
        new_Tabu = [0, 0]
        new_tour_distance = base_distance
    
    else:
        # Tabu_indx = randint(1, len(order) - 2)
        new_Tabu = [order[Tabu_indx - 1], order[Tabu_indx]]

    return best, new_Tabu, new_tour_distance

def Tabu_Search(order_, tabu_tenure,  dist_mat, iterations, f, d):
    # inicjacja zmiennych
    best_solution = order_.copy()
    selected_neighbor = order_.copy()
    best_solution_distance = get_tour_distance(best_solution, dist_mat)
    selected_neighbor_distance = get_tour_distance(selected_neighbor, dist_mat)
    Tabu_list = []

    # podanie długości trasy rozwiązań początkowych
    f.append(selected_neighbor_distance)
    d.append(best_solution_distance)

    #główna pętla
    for i in range(0, iterations):
        
        # wyznaczenie najlepszego sąsiada, nowego Tabu oraz długości trasy nowego sąsiada
        selected_neighbor, new_Tabu, selected_neighbor_distance = get_best_neighbor(selected_neighbor, selected_neighbor_distance, dist_mat, best_solution_distance, Tabu_list)

        # jeśli nowy wyznaczony(najlepszy z sądsiedztwa) sąsiad ma długość trasy mniejszą niż wartość długości dla najkrótszej wcześniej uzyskanej,
        # to wtedy on staje się najlepszą kolejnością
        if(selected_neighbor_distance < best_solution_distance):
            best_solution = selected_neighbor
            best_solution_distance = selected_neighbor_distance
        
        f.append(selected_neighbor_distance)
        d.append(best_solution_distance)

        Tabu_list.append(new_Tabu)
        if(len(Tabu_list) > tabu_tenure):
            Tabu_list.pop(0)
        
        if(i % 25 == 0):
            rand = randint(0, len(Tabu_list) - 1)
            Tabu_list.pop(rand)

    return best_solution    # zwracana jest najlepsza znaleziona kolejność odwiedzania miast

def two_opt(order_, dist_mat):
    best = order_.copy()
    improved = True
    while(improved):
        improved = False
        for i in range(1, len(best) - 2):
            for j in range(i + 2, len(best)):
                if(distance_change(dist_mat, best[i - 1], best[i], best[j - 1], best[j]) < 0):
                    improved = True
                    best[i:j] = best[j - 1: i - 1: -1]
        order = best
    return order

def get_dail_tour(limit, order, dist_mat):

    base = order[0]
    #jeśli podany limit jest zbyt mały zostaje zwiększony do minimalnej wartości pozwalającej na stworzenie mini trasy dla pojedynczego najdalej oddalonego od bazy miasta
    if(limit < 2 * (npmax(dist_mat[base, :])) + 1):
        limit = 2 * (npmax(dist_mat[base, :])) + 1
    order = order.copy()
    cities_left = True
    able_to_add_location = True
    current_position = 0
    last_tour_start_point = 0
    daily_tours_count = 0
    all_tours_distance = 0
    distance = 0

    while(cities_left):
        
        distance = dist_mat[base, order[current_position]]  # ustawienie dystansu na wartość odległości od bazy do kolejnego miasta
        last_tour_start_point = current_position            # nadpisanie punktu startowego ostatniej dniówki dla każdego rozpoczętego tworzenia dniówki
        able_to_add_location = True
        while(able_to_add_location):
            
            # sprawdzenie czy po dodaniu do obecnej długości trasy odległości od ostatniego w kolejce mista do miasta potecnajlnie dodanego oraz od miasta potencjalnie
            # dodanego do bazy długości trasy będzie niższą bądź równa ustalnemu limitowi
            if((distance + dist_mat[order[current_position], order[current_position + 1]] + dist_mat[order[current_position + 1], base]) <= limit):
                distance = distance + dist_mat[order[current_position], order[current_position + 1]]
                current_position = current_position + 1
                if(current_position == (len(order) - 1)):
                    able_to_add_location = False
            else:
                distance = distance + dist_mat[base, order[current_position]]
                order.insert(current_position + 1, base)
                able_to_add_location = False
                current_position = current_position + 2
        
        all_tours_distance = all_tours_distance + distance
        daily_tours_count = daily_tours_count + 1
        if(current_position == (len(order) - 1)):
                    cities_left = False
    
    
    last_tour = order[last_tour_start_point: len(order)]
    last_tour_distance = get_tour_distance(last_tour, dist_mat) + dist_mat[order[last_tour_start_point], base]

    return order, daily_tours_count, all_tours_distance, last_tour_distance

def set_base(base, order):
    order = order.copy()
    if(base == order[0]):
        return order
    
    order = order.copy()
    base_index = order.index(base)
    order.pop(len(order) - 1)
    temp1 = order[base_index: len(order)]
    temp2 = order[0: base_index]
    new_order = temp1 + temp2
    new_order.append(base)

    return new_order

def get_best_neighbor_daily(order_, limit, dist_mat, Tabu, best_daily_tour_count_, best_last_tour_distance_, best_all_tour_distance_):
    order = order_.copy()

    best_order = order_.copy()
    best_daily_tour_count = best_daily_tour_count_
    best_all_tour_distance = best_all_tour_distance_
    best_last_tour_distance = best_last_tour_distance_

    new_candidate = best_order
    min_daily_tours_count = best_daily_tour_count * 2
    min_last_tour_distance = best_last_tour_distance * 2
    min_all_tours_distance = best_all_tour_distance * 2

    new_solution_generated = False

    for i in range(1, len(order) - 2):
        for j in range(i + 2, len(order)):

            new_candidate = order.copy()
            new_candidate[i:j] = new_candidate[j - 1: i - 1: -1]
            unchanged_new_candidate = new_candidate.copy()
            new_candidate, new_candidate_daily_tours_count, new_all_tours_distance, new_last_tour_distance = get_dail_tour(limit, new_candidate, dist_mat)
            Tabu_val = check_Tabu(new_candidate, Tabu)

            if(new_candidate_daily_tours_count < min_daily_tours_count and Tabu_val is False):
                # best_order = new_candidate
                best_order = unchanged_new_candidate
                min_daily_tours_count = new_candidate_daily_tours_count
                min_last_tour_distance = new_last_tour_distance
                min_all_tours_distance = new_all_tours_distance
                new_solution_generated = True
                Tabu_indx = i

            elif(new_candidate_daily_tours_count == min_daily_tours_count and Tabu_val is False):

                if(new_last_tour_distance < min_last_tour_distance):
                    # best_order = new_candidate
                    best_order = unchanged_new_candidate
                    min_daily_tours_count = new_candidate_daily_tours_count
                    min_last_tour_distance = new_last_tour_distance
                    min_all_tours_distance = new_all_tours_distance
                    new_solution_generated = True
                    Tabu_indx = i

                elif(new_last_tour_distance == min_last_tour_distance):

                    if(new_all_tours_distance < min_all_tours_distance):
                        # best_order = new_candidate
                        best_order = unchanged_new_candidate
                        min_daily_tours_count = new_candidate_daily_tours_count
                        min_last_tour_distance = new_last_tour_distance
                        min_all_tours_distance = new_all_tours_distance
                        new_solution_generated = True
                        Tabu_indx = i
    
    if(new_solution_generated is False):
        new_Tabu = [0, 0]
        min_daily_tours_count = best_daily_tour_count_
        min_last_tour_distance = best_last_tour_distance_
        min_all_tours_distance = best_all_tour_distance_
    else:
        # Tabu_indx = randint(1, len(order) - 2)
        # new_Tabu = [order[Tabu_indx - 1], order[Tabu_indx], order[Tabu_indx + 1]]
        new_Tabu = [order[Tabu_indx - 1], order[Tabu_indx]]
    
    return best_order, new_Tabu, min_daily_tours_count, min_last_tour_distance, min_all_tours_distance


def TS_daily_tours(order, limit, base, tabu_tenure, dist_mat, iterations, f, d, g, ff, dd, gg):
    order = order.copy()
    order = set_base(base, order)
    best_order, best_daily_tour_count, best_all_daily_tours_distance, best_last_tour_distance = get_dail_tour(limit, order, dist_mat)
    changed_selected_order, selected_daily_tour_count, selected_all_daily_tour_distance, selectes_last_tour_distance = best_order, best_daily_tour_count, best_all_daily_tours_distance, best_last_tour_distance
    selected_order = order.copy()
    Tabu_list = []
    how_often = 1
    if(iterations > 500):
        how_often = int(iterations / 500)
    
    # podanie długości trasy rozwiązań początkowych
    f.append(selected_daily_tour_count)
    d.append(selectes_last_tour_distance)
    g.append(selected_all_daily_tour_distance)
    ff.append(best_daily_tour_count)
    dd.append(best_last_tour_distance)
    gg.append(best_all_daily_tours_distance)

    #główna pętla
    for i in range(0, iterations):
        
        # wyznaczenie najlepszego sąsiada, nowego Tabu oraz długości trasy nowego sąsiada
        # selected_neighbor, new_Tabu, selected_neighbor_distance = get_best_neighbor(selected_neighbor, selected_neighbor_distance, dist_mat, best_solution_distance, Tabu_list)
        
        # jeśli nowy wyznaczony(najlepszy z sądsiedztwa) sąsiad ma długość trasy mniejszą niż wartość długości dla najkrótszej wcześniej uzyskanej,
        # to wtedy on staje się najlepszą kolejnością

        selected_order, new_Tabu, selected_daily_tour_count, selectes_last_tour_distance, selected_all_daily_tour_distance = get_best_neighbor_daily(selected_order, limit, dist_mat, Tabu_list, selected_daily_tour_count, selectes_last_tour_distance, selected_all_daily_tour_distance)
        
        if(selected_daily_tour_count < best_daily_tour_count):
            best_order = selected_order
            best_daily_tour_count = selected_daily_tour_count
            best_all_daily_tours_distance = selected_all_daily_tour_distance
            best_last_tour_distance = selectes_last_tour_distance

        elif(selected_daily_tour_count == best_daily_tour_count):

            if(selectes_last_tour_distance < best_last_tour_distance):
                best_order = selected_order
                best_daily_tour_count = selected_daily_tour_count
                best_all_daily_tours_distance = selected_all_daily_tour_distance
                best_last_tour_distance = selectes_last_tour_distance

            elif(selectes_last_tour_distance == best_last_tour_distance):

                if(selected_all_daily_tour_distance < best_all_daily_tours_distance):
                    best_order = selected_order
                    best_daily_tour_count = selected_daily_tour_count
                    best_all_daily_tours_distance = selected_all_daily_tour_distance
                    best_last_tour_distance = selectes_last_tour_distance
                
        if(i % how_often == 0):
            f.append(selected_daily_tour_count)
            d.append(selectes_last_tour_distance)
            g.append(selected_all_daily_tour_distance)
            ff.append(best_daily_tour_count)
            dd.append(best_last_tour_distance)
            gg.append(best_all_daily_tours_distance)

        Tabu_list.append(new_Tabu)

        if(len(Tabu_list) > tabu_tenure):
            Tabu_list.pop(0)
        
        if(i % 25 == 0):
            rand = randint(0, len(Tabu_list) - 1)
            Tabu_list.pop(rand)

    updated_best_order, _, __, ___ = get_dail_tour(limit, best_order, dist_mat)

    return updated_best_order, best_daily_tour_count