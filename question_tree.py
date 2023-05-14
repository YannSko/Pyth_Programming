class Node:
    def __init__(self, question, responses):
        self.question = question
        self.responses = responses
        self.next_nodes = []

    def append(self, question, responses, previous_question):
        if previous_question == self.question:
            self.next_nodes.append(Node(question, responses))
        else:
            for N in self.next_nodes:
                N.append(question, responses, previous_question)

    def delete(self, question):
        for N in self.next_nodes:
            if N.question == question:
                self.next_nodes.remove(N)
            else:
                N.delete(question)

class Tree:
    def __init__(self, first_question):
        self.first_node = Node(first_question, [])
        self.current_node = self.first_node

    def append_question(self, question, responses, previous_question):
        self.first_node.append(question, responses, previous_question)

    def delete_question(self, question):
        if self.first_node.question == question:
            self.first_node = None
        else:
            self.first_node.delete(question)

    def get_question(self):
        return self.current_node.question

    def send_answer(self, response):
        for N in self.current_node.next_nodes:
            if response.content.lower() in N.responses:
                self.current_node = N
                break

        return self.current_node.question

    def reset(self):
        self.current_node = self.first_node

    def speak_about(self, topic):
        for n in self.current_node.next_nodes:
            if topic.lower() in n.question.lower():
                return f"Yes, I can speak about {topic}"
        return f"Sorry, I cannot speak about {topic}"
