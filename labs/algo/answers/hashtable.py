class HashTable:
    """A dictionary of our own: each key goes in a bucket chosen by its hash."""

    def __init__(self):
        self.buckets = []
        for i in range(1000):
            self.buckets.append([])
        self.count = 0

    def bucket_for(self, key):
        return self.buckets[hash(key) % len(self.buckets)]

    def put(self, key, value):
        bucket = self.bucket_for(key)
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return
        bucket.append([key, value])
        self.count = self.count + 1

    def get(self, key):
        for pair in self.bucket_for(key):
            if pair[0] == key:
                return pair[1]
        return None

    def size(self):
        return self.count
