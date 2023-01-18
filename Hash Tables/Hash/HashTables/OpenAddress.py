class OpenAddress:

    def __init__(self, num_cells):
        self.collision = 0
        self.explorations = 1
        self.num_cells = num_cells
        self.cells = []
        self.occupied = 0
        for i in range(num_cells):
            self.cells.append(None)

    def get_collision(self):
        return self.collision

    def get_explorations(self):
        return self.explorations

    def hash(self, index, key):
        return ((key % self.num_cells) + index) % self.num_cells

    def insert(self, key):
        if self.occupied < self.num_cells:  # se c'è un None significa che non è piena
            collided = False
            i = 0
            while True:
                self.explorations = i + 1
                j = self.hash(i, key)
                if self.cells[j] is None or self.cells[j] == "DEL":
                    self.cells[j] = key
                    self.occupied += 1
                    return j
                else:
                    i += 1
                    # self.explorations = i
                    if not collided:
                        self.collision += 1
                        collided = True
                if i == self.num_cells:
                    break
            return "Error"

    def search(self, key):
        i = 0
        while True:
            self.explorations = i + 1
            j = self.hash(i, key)
            if self.cells[j] == key:
                return j
            i += 1
            if i == self.num_cells or self.cells[j] is None:
                break
        return None

    def delete(self, key):
        index = self.search(key)
        if index is not None:
            self.cells[index] = "DEL"

    def print(self):
        for i in self.cells:
            if i is not None:
                print(i)
