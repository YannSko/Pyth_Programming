class Binary_Tree:
    def __init__(self):
        self.subjects = {}
        self.root = None

    def next_junction(self, junction_node, is_right):
        if is_right:
            return junction_node.right
        else:
            return junction_node.left

    def add_subject(self, subject, text):
        self.subjects.update({subject: text})

    def print_subject(self, subject):
        if subject in self.subjects:
            return self.subjects[subject]
        else:
            return "No such subject"


class Junction:
    def __init__(self, junction_text):
        self.text = junction_text
        self.right = None
        self.left = None

    def __str__(self):
        return self.text

    def add_junction(self, text, is_right):
        if is_right:
            self.right = Junction(text)
        else:
            self.left = Junction(text)

    def add_leaf(self, text, is_right):
        if is_right:
            self.right = text
        else:
            self.left = text