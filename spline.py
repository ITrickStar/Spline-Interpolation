from numpy import resize, array, float32, linspace
import var

def arr_resize(arr):
    for i in range(len(arr)):
        if (arr[i] == ''):
            arr = resize(arr, i)
            break
    return arr

def compute_changes(x):
    return [x[i+1] - x[i] for i in range(len(x) - 1)]

# # Сортировка иксов и соответственное перемещение игриков
def insertion_sort(x, y):
# # Сортировку начинаем со второго элемента, т.к. считается, что первый элемент уже отсортирован
    for i in range(1, len(x)):
        item_to_insert = x[i]
        item_to_shuffle = y[i]
        j = i - 1
        while j >= 0 and x[j] > item_to_insert:
            x[j + 1] = x[j]
            y[j + 1] = y[j]
            j -= 1
        x[j + 1] = item_to_insert
        y[j + 1] = item_to_shuffle
    return x,y

def build_spline(list_x, list_y):
    n = len(list_x)
    
    for i in range(n-1):
        if (list_x[i] == '' or list_y[i] == ''):
          raise ValueError('Не задано одно из значений')  
    if n < 3:
        raise ValueError('Недостаточно данных для построения сплайна')
    if n != len(list_y):
        raise ValueError('Количество аргументов X и Y различно')
    h = compute_changes(list_x)
    if any(v < 0 for v in h):
        raise ValueError('Аргумент X должен строго возрастать')

    a = []
    b = [0] * n
    c = [0] * n
    d = [0] * n
    for i in range (n):
        a.append(list_y[i])
    c[0], c[n-1] = 0, 0
    alpha = [0] * (n - 1)
    beta = [0] * (n - 1)

    for i in range(1, n - 1):
        h_prev = list_x[i] - list_x[i - 1]
        h_next = list_x[i + 1] - list_x[i]
        A, B, C, F = h_prev, 2.0 * (h_prev + h_next), h_next, 6.0 * ((a[i + 1] - a[i]) / h_next - (a[i] - a[i - 1]) / h_prev)
        z = (A * alpha[i - 1] + B)
        alpha[i] = -C / z
        beta[i] = (F - A * beta[i - 1]) / z
    #print(alpha)
    print('beta')
    print(beta)

    for i in range(n - 1, 1, -1):
        c[i - 1] = alpha[i - 1] * c[i] + beta[i - 1]
    print('c')
    print(c)
    print('d')
    for i in range(n - 1, 0, -1):
        h_prev = list_x[i] - list_x[i - 1]
        #d[i] = (c[i] - c[i - 1]) / (3 * h_prev)
        #b[i] = (a[i] - a[i - 1]) / h_prev - ( (2.0 * c[i] + c[i - 1]) / 3.0 ) * h_prev
        d[i] = (c[i] - c[i - 1]) / h_prev
        b[i] = h_prev * (2.0 * c[i]+ c[i - 1]) / 6.0 + (a[i] - a[i - 1]) / h_prev
    print(d)
    print('koef')
    for i in range(1, n):
        print(a[i], b[i], c[i], d[i], sep = ' ')
    return a, b, c, d

def interpolate(a, b, c, d, list_x, one_x):

    n = len(list_x)  # Calculate the gap
    i = 0
    j = n - 1
    while i + 1 < j:
        k = i + (j - i) // 2
        if one_x <= list_x[k]:
            j = k
        else:
            i = k

    h = one_x - list_x[j]
    return a[j] + (b[j] + (c[j] / 2.0 + d[j] * h / 6.0) * h) * h