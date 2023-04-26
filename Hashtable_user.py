from Liste_chained import list_chained, Node, fifo

class HashTableUser:
    def __init__(self, bucket_size):
        self.buckets = []
        self.bucket_size = bucket_size
        for i in range(bucket_size):
            self.buckets.append([])

    def append(self, user_id, value):
        hashed_key = hash(user_id)
        indice_bucket = hashed_key % self.bucket_size
        found = False
        for i, (bucket_key, bucket_value) in enumerate(self.buckets[indice_bucket]):
            if bucket_key == user_id:
                self.buckets[indice_bucket][i] = (bucket_key, bucket_value.append(value))
                found = True
                break
        if not found:
            self.buckets[indice_bucket].append((user_id, list_chained(value)))

    def get(self, user_id):
        hashed_key = hash(user_id)
        indice_bucket = hashed_key % self.bucket_size
        for bucket_key, bucket_value in self.buckets[indice_bucket]:
            if bucket_key == user_id:
                return bucket_value
        return None

    def sup(self, user_id):
        hashed_key = hash(user_id)
        indice_bucket = hashed_key % self.bucket_size
        for i, (bucket_key, bucket_value) in enumerate(self.buckets[indice_bucket]):
            if bucket_key == user_id:
                del self.buckets[indice_bucket][i]
                return bucket_value
        return None
