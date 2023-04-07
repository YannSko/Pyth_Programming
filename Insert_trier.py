class list_chained_sorted:
    def __init__(self,data):
        self.first_node = Node(data)
        self.last_node = self.first_node

    def add_data(self,data):


class Node:
    def __init__(self,data):
        self.data = data
        self.next_node = None        