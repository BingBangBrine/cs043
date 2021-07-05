from lesson2_2.database import Simpledb

db = Simpledb("telephone.txt")
db.insert("doggy", "555")
print(db.select_one("doggy"))
