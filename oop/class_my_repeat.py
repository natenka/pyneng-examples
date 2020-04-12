class MyRepeat:
    def __init__(self, value):
        self._value = value

    def __next__(self):
        return self._value

    def __iter__(self):
        return self



if __name__ == "__main__":
    print(list(zip([1,2,3], MyRepeat(100))))
    # [(1, 100), (2, 100), (3, 100)]

