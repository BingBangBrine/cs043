import sqlite3

connection = sqlite3.connect('business.db')
cursor = connection.cursor()

# product_cursor = cursor.execute('SELECT price, prodname FROM products')
# product_cursor = cursor.execute('SELECT prodname, price, weight, price/weight FROM products')

product_cursor = cursor.execute('SELECT prodname, weight FROM products')
product_list = product_cursor.fetchall()

for prodname, weight in product_list:
    print('Product: {}\tWeight: {} kg'.format(prodname, weight))

# for product in product_list:
#     print(product)


# Updating
# connection.execute('UPDATE products SET weight = ?', [9])  # Set all weights to 9
# connection.commit()                                        # Remember to commit()

# Deleting
# connection.execute('DELETE FROM products')                 # Delete all rows in products
# connection.commit()                                        # Remember to commit()

# Where clause
# # Check if username Joe is taken
# products = cursor.execute('SELECT * FROM users WHERE username = ?', ['Joe'])
#
# # Verify the username and password stored in variables u and p, respectively
# products = cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', [u, p])
#
# # Set all weights smaller than 1 to 0
# connection.execute('UPDATE products SET weight = ? WHERE weight < ?', [0, 1])
#
# # Delete book from the product list
# # connection.execute('DELETE FROM products WHERE prodname = ?', ['book'])
