from traveling_salesman_problem_functions import  get_tour_distance
from numpy import max as npmax, sqrt
from random import sample

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