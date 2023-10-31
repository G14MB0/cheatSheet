'''
if you're using a resolving plugin, there would be the case that hello could not be resolved
this is because the file hello.cp311..... is imported here as "hello" (and it's correct) but
the resolving alghorithm won't work with non-python files
'''

import hello
import timeit
import random


print(hello.hello_world())  # Stampa: Hello, World!

floats = [random.uniform(0, 100) for _ in range(1000)]
floats = [float(i) for i in floats]

# Tempo per la nostra funzione C estesa
start_time = timeit.default_timer()
sorted_floats_c = hello.sort_float_list(floats)
end_time = timeit.default_timer()
print("C Extension Time:", end_time - start_time)
# print(sorted_floats_c)  # Stampa: [0.5, 1.41, 2.0, 2.71, 3.14]

# Tempo per il metodo sort di Python
start_time = timeit.default_timer()
floats.sort()
end_time = timeit.default_timer()
print("Python Sort Time:", end_time - start_time)
# print(floats)  # Stampa: [0.5, 1.41, 2.0, 2.71, 3.14]