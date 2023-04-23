class list_chained:
    def __init__(self, first_data):
        self.first_node = Node(first_data)
        self.last_node = self.first_node
        self.size = 1
        
    def append(self, data):
        self.last_node.next_node = Node(data)
        self.last_node = self.last_node.next_node
        self.size += 1
        
    def insert_first(self, data):
        current_node = Node(data)
        current_node.next_node = self.first_node
        self.first_node = current_node
        self.size += 1
        
    def get_size(self):
        return self.size
    
    def insert(self, index, data):
        current_node = self.first_node
        i = 0 
        while index > i:
            current_node = current_node.next_node
            i += 1
        new_node = Node(data)
        new_node.next_node = current_node.next_node
        current_node.next_node = new_node
        self.size += 1
        
    def last_elmt(self):
        return self.last_node.data
    
    def first_elmt(self):
        return self.first_node.data
                
    def delete_last(self):
        if self.size == 1:
            self.first_node = None
            self.last_node = None
            self.size = 0
        else:
            current_node = self.first_node
            while current_node.next_node != self.last_node:
                current_node = current_node.next_node
            current_node.next_node = None
            self.last_node = current_node
            self.size -= 1
            
    def delete_at_index(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")
        if index == 0:
            self.first_node = self.first_node.next_node
            self.size -= 1
        else:
            current_node = self.first_node
            i = 0 
            while index > i + 1:
                current_node = current_node.next_node
                i += 1
            current_node.next_node = current_node.next_node.next_node
            self.size -= 1
    def show_all(self):
        current_node = self.first_node
        i = 0
        List = []
        while current_node is not None:
            pip = "Message numéro: {}\n Contenu: {}".format(i, current_node.data)
            List.append(pip)
            current_node = current_node.next_node
            i += 1
        return List
    def delete_all(self):
        self.first_node = Node("début historique")
        self.last_node = self.first_node
        self.size = 1      
        
class Node:
    def __init__(self,data):
        self.data = data
        self.next_node = None




class list_chained_sorted(list_chained):
    def __init__(self,data):
        self.first_node = Node(data)
        self.last_node = self.first_node

   

    def add_data(self,data):
        if data < self.first_node.data :
            N.next_node = self.first_node
            self.first_node = N 
            return 
        if data > self.last_node.data:
            self.last_node.next_node = N
            self.last_node = N

        
            
        current_node = self.first_node
        while (current_node.next_node.data)<data : 
            curent_node = current_node.next_node

        N = Node(data)
        N.next_node = current_node.next_node
        current_node.next_node = N

class Stack:
    def __init__(self,data):
        self.last_node = Node(data)
        self.size =1

    def push(self,data):
        N = Node(data)
        N.next_node = self.last_node
        self.last_node = N
        self.size +=1

    def pop(self):
        data = self.last_node.data
        self.last_node = self.last_node.next_node
        self.size -=1
        return data 
        
    def size(self):
        return self.size

    def peek(self):
        return self.last_node.data

class fifo:
    def __init__(self,data):
        self.first_node = Node(data)
        self.size =1

    def __str__(self):
        txt = str(self.first_node)
        return txt
    def push(self,data):
        if self.first_node == None :
            self.first_node = Node(data)
            return
        current_node = self.first_node
        while current_node.next_node !=None:
            current_node = current_node.next_node
        current_node.next_node = Node(data)


    def pop(self,data):
        data = self.first_node.data
        self.first_node = self.first_node.next_node
        
        return data 
    def peek(self):
        return self.first_node
    def size(self):
        return self.size
   
class HistoryManager(fifo):
    def __init__(self):
        super().__init__(None)
        self.history_queue = fifo(None)

    def add_to_queue(self, user_id):
        self.history_queue.push(user_id)

    def remove_from_queue(self):
        return self.history_queue.pop()

    def is_queue_empty(self):
        return self.history_queue.size == 0
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    
class Boucle:
    def __init__(self,data):
        self.first_node = Node(data)

        

    

   