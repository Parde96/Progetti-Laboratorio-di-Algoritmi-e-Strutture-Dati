from LinkedList.LinkedList import *


class Chained:

    def __init__(self, num_cells):
        self.collision = 0
        self.num_cells = num_cells
        self.cells = []
        for i in range(num_cells):
            self.cells.append(LinkedList())

    def get_collision(self):
        return self.collision

    def hash(self, key):
        return key % self.num_cells

    def insert(self, node):
        lista = self.cells[self.hash(node.data)]
        if lista.head is not None:
            self.collision += 1
        lista.add(node)

    def delete(self, node):
        lista = self.cells[self.hash(node.data)]
        lista.remove(node)

    def search(self, key):
        lista = self.cells[self.hash(key)]
        return lista.search(key)

    def print_table(self):
        for i in range(self.num_cells):
            self.cells[i].print_l()
