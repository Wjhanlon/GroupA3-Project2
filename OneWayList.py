class OneWayList:
    def __init__(self, initial_data=None):
        self._data = list(initial_data) if initial_data else []

    def append(self, item):
        self._data.append(item)

    def __getitem__(self, index):
        return self._data[index]

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return f"AppendOnlyList({self._data})"