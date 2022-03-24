#Konfiguracja

#Maksymalny błąd prędkości początkowej w m/s względem 1 m/s
MAX_ERROR = 0.3

#Ile kul ma wziąć udział w symulacji
#Kule będą rozmieszczone w przedziale [1 - MAX_ERROR, 1 + MAX_ERROR] co ERROR_STEP (tak plus minus)
#Ostateczna liczba kul to (round((2*MAX_ERROR)/ERROR_STEP) + 1)
ERROR_STEP = 0.1

