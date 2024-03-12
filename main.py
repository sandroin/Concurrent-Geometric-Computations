import random as rd
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


class Trapezoid:
    def __init__(self, trap=None):
        if trap is None:
            trap = [0, 0, 0]
        self.a = min(trap)
        self.b = max(trap)
        self.h = sum(trap) - self.a - self.b

    def __str__(self):
        return 'ტოლფერდა ტრაპეციის დიდი ფუძეა -> {}, პატარა ფუძეა -> {}, ხოლო სიმაღლეა ->{}'.format(self.b, self.a,
                                                                                                    self.h)

    def area(self):
        return (self.a + self.b) / 2 * self.h

    def __lt__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() < other.area()
        return False

    def __eq__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() == other.area()
        return False

    def __ge__(self, other):
        if isinstance(other, Trapezoid):
            return not self.__lt__(other)
        return False

    def __add__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() + other.area()
        else:
            raise TypeError("Unsupported operand type(s) for +: '{}' and '{}'".format(
                type(self).__name__, type(other).__name__))

    def __sub__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() - other.area()
        else:
            raise TypeError("Unsupported operand type(s) for -: '{}' and '{}'".format(
                type(self).__name__, type(other).__name__))

    def __mod__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() % other.area()
        else:
            raise TypeError("Unsupported operand type(s) for %: '{}' and '{}'".format(
                type(self).__name__, type(other).__name__))


class Rectangle(Trapezoid):
    def __init__(self, re=None):
        if re is None:
            re = [0, 0]
        super().__init__([re[0], re[0], re[1]])

    def __str__(self):
        return "მართკუთხედის სიმაღლეა -> {}, ხოლო სიგანე -> {}".format(self.a, self.h)


class Square(Rectangle):
    def __init__(self, c):
        super().__init__([c, c])

    def __str__(self):
        return "კვადრატის გვერდი არის -> {}".format(self.a)


def trapezoid_area(arr):
    for i in arr:
        t = Trapezoid(i)
        t.area()


def rectangle_area(arr):
    for i in arr:
        r = Rectangle(i)
        r.area()


def square_area(arr):
    for i in arr:
        s = Square(i)
        s.area()


def regular(arr):
    start = time.perf_counter()

    trapezoid_area(arr)

    finish = time.perf_counter()

    print('regular finished in: ', round(finish - start, 2), 'second(s)')


def threads(arr, num_threads):
    chunk_size = len(arr) // num_threads

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        [executor.submit(trapezoid_area, arr[i * chunk_size:(i + 1) * chunk_size]) for i in range(num_threads)]


def multiprocess(arr, num_processes):
    start = time.perf_counter()

    chunk_size = len(arr) // num_processes

    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        [executor.submit(trapezoid_area, arr[i * chunk_size:(i + 1) * chunk_size]) for i in range(num_processes)]

    finish = time.perf_counter()
    print('With processes Finished in:', round(finish - start, 2), 'seconds')


def multiprocess_with_threads(arr, num_processes, num_threads):
    start = time.perf_counter()

    chunk_size = len(arr) // num_threads

    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        for i in range(num_processes):
            executor.submit(threads, arr[i * chunk_size:(i + 1) * chunk_size], num_threads)

    finish = time.perf_counter()
    print('With processes and threads Finished in:', round(finish - start, 2), 'seconds')


if __name__ == "__main__":
    trapezoids = [[rd.randint(1, 200), rd.randint(
        1, 200), rd.randint(1, 200)] for _ in range(1000000)]

    # Generating parameters for 10000 rectangles: width and height
    rectangles = [[rd.randint(1, 200), rd.randint(1, 200)] for _ in range(100000)]

    squares = [rd.randint(1, 200) for _ in range(100000)]

    regular(trapezoids)
    beginning = time.perf_counter()
    threads(trapezoids, 20)
    end = time.perf_counter()
    print('With threads Finished in:', round(end - beginning, 2), 'seconds')
    multiprocess(trapezoids, 10)
    multiprocess_with_threads(trapezoids, 10, 20)
