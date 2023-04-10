from tsp_solving_algorithm import TSP_solve

if(__name__ == "__main__"):

    print("Możliwe wybory zestawu danych:\n1 - Berlin52\n2 - Att48\n3 - Eil101\n")
    data_set_number = int(input("Wprowadź liczbę 1, 2 bądź 3 aby wybrać zestaw danych.\n"))
    while(data_set_number != 1 and data_set_number != 2 and data_set_number != 3):
        data_set_number = int(input("Wprowadź liczbę 1, 2 bądź 3 aby dokonać wyboru zestawu danych!\n"))

    if(data_set_number == 1):
        opt_tour_name = "berlin52.opt.tour.txt"
        data_set_name = "berlin52.txt"

    elif(data_set_number == 2):
        opt_tour_name = "att48.opt.txt"
        data_set_name = "att48.txt"

    elif(data_set_number == 3):
        opt_tour_name = "eil101.opt.txt"
        data_set_name = "eil101.txt"

    print("Wybierz:\n1 jeśli chcesz aby dniówki były uwzględnione\n2 jeśli chcesz aby nie były uwzględniane")
    is_daily_number = int(input("Wprowadź liczbę 1 bądź 2.\n"))
    while(data_set_number != 1 and data_set_number != 2):
        is_daily_number = int(input("Wprowadź liczbę 1 bądź 2!\n"))

    if(is_daily_number == 1):
        is_daily = True
    else:
        is_daily = False
    
    print("Wprowadź wartość całkowitą dla parametru tabu tenure w przedziale od 5 do 15\n")
    tabu_tenure = int(input("Wprowadź wartość.\n"))
    while(tabu_tenure < 5 or tabu_tenure > 15):
        tabu_tenure = int(input("Wprowadź wartość całkowitą z przedziału od 5 do 15!\n"))
    
    print("Wprowadź liczbę iteracji dla algorytmu Tabu Search.\n Liczba iteracji powinna być w przedziale od 0 do 5000.")
    iterations = int(input("Wprowadź wartość.\n"))
    while(iterations < 0 or iterations > 5000):
        iterations = int(input("Wprowadź wartość całkowitą z przedziału od 0 do 5000!\n"))
    
    TSP_solve(opt_tour_name, data_set_name, is_daily, tabu_tenure, iterations)
