class hastable_user:
    def __init__(self,bucket_size):
        self.buckets = []
        for i in range (bucket_size):
            self.buckets.append([])

    def append (self, key, value):
        hashed_key = hash(key)
        indice_bucket = hashed_key % len(self.buckets)
        self.buckets[indice_bucket].append((key,value))

    def get (self,key):
        hashed_key = hash(key)
        indice_bucket = hashed_key % len(self.buckets)
        for bucket_key,bucket_value in self.buckets[indice_bucket] :
            if bucket_key == key:
                return bucket_value
        return None

    def sup (self,key):
        hashed_key = hash(key)
        indice_bucket = hashed_key % len(self.buckets)
        for bucket_key,bucket_value in self.buckets[indice_bucket] :
            if bucket_key == key:
                del bucket_value,bucket_key
        return None