class node : 
  def __init__(self,data):
    self.data = data
    self.right_node = None
    self.left_node = None

  def append(self,data):
    if data < self.data :
      if self.left_node == None:
        self.left_node = node(data)
      else:
        self.left_node.append(data)
    elif data > self.data:
      if self.right_node == None:
        self.right_node = node(data)
      else:
        self.right_node.append(data)

  def search(self, data):
    if data == self.data:
      return True
    elif data < self.data:
      if self.left_node == None:
        return False
      else:
        return self.left_node.search(data)
    else:
      if self.right_node == None:
        return False
      else:
        return self.right_node.search(data)

  def __str__(self):
    txt = str(self.data)
    if self.left_node != None:
      txt += "-" +str(self.left_node)
    if self.right_node != None:
      txt += "-" +str(self.right_node)
    return txt

class binary_tree:
  def __init__(self,data):
    self.first_node = node(data)
  
  def append(self,data):
    self.first_node.append(data)

  def search(self,data):
    return self.first_node.search(data)

  def __str__(self):
    return str(self.first_node)
    

    