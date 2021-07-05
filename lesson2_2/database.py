class Simpledb:
    def __init__(self, filename):
        self.filename = filename
    def __repr__(self):
        return ("<" + self.__class__.__name__ +
        " file=" + str(self.filename) +
        ">")

    #database functions

    def insert(self, key, value):
        f = open(self.filename, 'a')
        f.write(key + '\t' + value + '\n')
        f.close() 

    def select_one(self, key):
        f = open(self.filename, 'r')
        for row in f:
            (k, v) = row.split('\t', 1)
            if k == key:
                return v[:-1]
        f.close()

    def delete(self, key):
        f = open(self.filename, 'r')
        result = open('result.txt', 'w')
        found = False
        for (row) in f:
            (k, v) = row.split('\t', 1)
            if k != key:
                result.write(row)
            else:
                found = True
        f.close()
        result.close()
        import os
        os.replace('result.txt', self.filename)
        return found
        
    def update(self, key, value):
        f = open(self.filename, 'r')
        result = open('result.txt', 'w')
        for (row) in f:
            (k, v) = row.split('\t', 1)
            if k == key:
                result.write(key + '\t' + value + '\n')
            else:
                result.write(row)
        f.close()
        result.close()
        import os
        os.replace('result.txt', self.filename)
