class Node:
    def __init__(self, data, responses=None):
        self.data = data
        self.left_node = None
        self.right_node = None
        self.responses = responses or []

    def append(self, data, responses=None):
        if data < self.data:
            if self.left_node is None:
                self.left_node = Node(data, responses)
            else:
                self.left_node.append(data, responses)
        elif data > self.data:
            if self.right_node is None:
                self.right_node = Node(data, responses)
            else:
                self.right_node.append(data, responses)

    def search(self, data):
        if data == self.data:
            return self
        elif data < self.data:
            if self.left_node is None:
                return None
            else:
                return self.left_node.search(data)
        else:
            if self.right_node is None:
                return None
            else:
                return self.right_node.search(data)

    def __str__(self):
        txt = str(self.data)
        if self.left_node is not None:
            txt += "-" + str(self.left_node)
        if self.right_node is not None:
            txt += "-" + str(self.right_node)
        return txt

    def get_responses(self):
        return self.responses


class BinaryTree:
    def __init__(self, data, responses=None):
        self.first_node = Node(data, responses)

    def append(self, data, responses=None):
        self.first_node.append(data, responses)

    def search(self, data):
        return self.first_node.search(data)

    def __str__(self):
        return str(self.first_node)

    