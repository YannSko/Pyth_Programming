class Hashtable:
    def __init__(self,elements):
        self.bucket_size = len(elements)
        self.bucket = [[]for i in range [self.bucket] ]
        self._assign_buckets(elements)
    
    def _assign_buckets(self,input_key):
       pass