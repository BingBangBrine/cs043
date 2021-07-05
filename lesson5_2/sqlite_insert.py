import sqlite3

connection = sqlite3.connect('business.db')

connection.execute('INSERT INTO products VALUES (?, ?, ?)', ['book', 7.99, 0.5])
# This line connects to the products table that was created with the other file.
# You use the question marks because it is much safer.
# It is two arguments to insert instead of just one for creating the table itself.
# It inserts the prodname = 'book', the price = 7.99, and the weight = 0.5 into the table.
connection.execute('INSERT INTO products VALUES (?, ?, ?)', ['drink', 2.00, 0.4])

connection.execute('INSERT INTO products VALUES (?, ?, ?)', ['car', 70000, 1875])

connection.commit()
