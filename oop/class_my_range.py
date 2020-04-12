class MyRange:
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop
        self.current = start

    def __next__(self):
        print("вызываю __next__")
        value = self.current
        if value == self.stop:
            raise StopIteration
        self.current += 1
        return value

    def __iter__(self):
        print("вызываю __iter__")
        return self


if __name__ == "__main__":
    int_range = MyRange(1, 10)
    for i in int_range:
        print(i)
