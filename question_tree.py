class node:
  def __init__(self, answer_to_go_here, question):
    self.answer_to_go_here = answer_to_go_here
    self.question = question
    self.next_nodes = []

  def size(self):
    count = 1 
    for node in self.next_nodes:
      count += node.size()  
    return count

  def deepth(self):
    Max = 0
    for node in self.next_nodes:
      if node.deepth() > Max:
        Max = node.deepth()
    return Max + 1

  def append(self,question, reponses, question_precedante):
    if question_precedante == self.question:
      self.next_nodes.append(node(question, reponses))
    for n in self.next_nodes:
      n.append(question, reponses, question_precedante)
      
  def traverse(self, answer):
    if not self.next_nodes:
      return self.answer_to_go_here
    for node in self.next_nodes:
      if answer == node.answer_to_go_here:
        return node.question
    return None

class Tree:
    def __init__(self,question):
        self.first_node = node("",question)
        self.current_node = self.first_node

    def size(self):
        return self.first_node.size()

    def deepth(self):
        return self.first_node.deepth()

    def append(self, question, reponses, question_precedante):
        self.first_node.append( question, reponses, question_precedante)

    def get_question(self):
        return self.current_node.question

    def choice(self, message):
        found = False
        for node in self.current_node.next_nodes:
            if node.answer_to_go_here == message:
                self.current_node = node
                found = True
                break
            if not found:
                self.current_node = self.first_node
    def reset(self):
        self.current_node = self.first_node

    def traverse(self, answer):
        response = self.current_node.traverse(answer)
        if response:
            self.current_node = self.current_node.next_nodes[0]
        return response
