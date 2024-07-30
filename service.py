import pymysql
import random
from flask import redirect, session, render_template
import wtforms
from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms.validators import InputRequired, Length

shopping_cart = []


def execute_query(query):
    # Connect to the database
    connection = pymysql.connect(host='localhost',
                                 user='anushka',
                                 password='Jeonjungkook97',
                                 db='BookshopDB',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        # Execute the query
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            # use commit to save changes made
            connection.commit()
            return result
    except Exception as e:
        print(e)
        # rollback in case there is any error
        connection.rollback()
        return e
    finally:
        connection.close()


def get_books():
    # Do a join for genre and author
    query = "SELECT * FROM BOOKS"
    books = execute_query(query)
    for book in books:
        genre = get_genre_by_id(book['GENRE_ID'])
        author = get_author_by_id(book['AUTHOR_ID'])
        book['GENRE_NAME'] = genre[0]['GENRE_NAME']
        book['AUTHOR_NAME'] = str(author[0]['AUTHOR_F_NAME']) + ' ' + str(author[0]['AUTHOR_L_NAME'])

    return books


def get_authors():
    # Get all authors from the database and return as a json
    query = "SELECT * FROM AUTHOR"
    return execute_query(query)


print(get_authors())


def add_recommendation(book_isbn, book_name, author_name, recommendation):
    try:
        num = execute_query("SELECT COUNT(*) FROM RECOMMENDATIONS")
        num = num[0]['COUNT(*)'] + 1
        print(num)

        add_recommendation = ("INSERT INTO RECOMMENDATIONS"
                              " (Reco_ID, ISBN, BOOK_NAME, AUTHOR_NAME, RECOMMENDATION_TEXT) "
                              "VALUES (%s, %s, %s, %s, %s)")
        # execute_query(
        #     "INSERT INTO RECOMMENDATIONS"
        #     " (Reco_ID, ISBN, BOOK_NAME, AUTHOR_NAME, RECOMMENDATION_TEXT)"
        #     " VALUES (%s, %s, %s, %s, %s)")

        data_recommendation = (num, book_isbn, book_name, author_name, recommendation)
        connection = pymysql.connect(host='localhost',
                                     user='anushka',
                                     password='Jeonjungkook97',
                                     db='BookshopDB',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        with connection.cursor() as cursor:
            cursor.execute(add_recommendation, data_recommendation)
            result = cursor.fetchall()
            # use commit to save changes made
            connection.commit()
            connection.close()
        return True
    except Exception as e:
        return False


def get_book_details_by_isbn(isbn):
    return execute_query("SELECT * FROM BOOKS WHERE ISBN = '{}'".format(isbn))


def add_book(book):
    # Add the book to the database
    try:
        num = execute_query("SELECT COUNT(*) FROM BOOKS")
        num = num[0]['COUNT(*)'] + random.randint(10, 200)

        add_book = ("INSERT INTO BOOKS "
                    "(PRODUCT_ID, TITLE, GENRE_ID, AUTHOR_ID, PUBLICATION_DATE, ISBN, AVAILABILITY, PRICE) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

        data_book = (num, book['TITLE'], book['GENRE_ID'], book['AUTHOR_ID'], book['PUBLICATION_DATE'], book['ISBN'], book['AVAILABILITY'], book['PRICE'])
        # execute_query("INSERT INTO BOOKS (PRODUCT_ID, TITLE, GENRE_ID, AUTHOR_ID, PUBLICATION_DATE, ISBN, AVAILABILITY, PRICE) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(num, book['TITLE'], book['GENRE_ID'], book['AUTHOR_ID'], book['PUBLICATION_DATE'], book['ISBN'], book['AVAILABILITY'], book['PRICE']))
        connection = pymysql.connect(host='localhost',
                                     user='anushka',
                                     password='Jeonjungkook97',
                                     db='BookshopDB',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        with connection.cursor() as cursor:
            cursor.execute(add_book, data_book)
            result = cursor.fetchall()
            # use commit to save changes made
            connection.commit()
            connection.close()

            return True
    except Exception as e:
        # rollback in case there is any error
        connection.rollback()
        return False


def login_details(username, password):
    query = "SELECT * FROM USERS WHERE USERNAME = '{}' AND PASSWORD_HASH = '{}'".format(username, password)
    return execute_query(query)

    # # Assuming the result is a dictionary representing the user details
    # if result:
    #     role = result[0]['ROLE']
    #
    #     if role == 'Customer':
    #         # Redirect to the customer index page
    #         return redirect('/indexCustomer')
    #     else:
    #         # Redirect to the default index page for non-customers
    #         return redirect('/adminindex')
    #
    # # Return an error or handle the case where the login details are incorrect
    # return "Invalid username or password"


# def checkout():
#     # Clear the shopping cart
#     shopping_cart.clear()
#
#     # Redirect to the index page
#     return redirect('/')


def initialize_shopping_cart():
    # Initialize the shopping cart in the session
    # Initialize the cart in the session if it doesn't exist
    shopping_cart = []
    # if 'cart' not in session:
    #     session['cart'] = []

#def get_user_role(username):
    # Get the user role from the database using a parameterized query
    #query = "SELECT ROLE FROM USERS WHERE USERNAME = %s"
    #params = (username,)
    #result = execute_query(query, params)

    # Assuming execute_query returns the result of the query
    #return result


def add_to_cart(isbn):
    # Get book details by ISBN (you might want to implement this function)
    book = get_book_details_by_isbn(isbn)
    shopping_cart.append(book[0])

    # # Initialize the cart in the session if it doesn't exist
    # if 'cart' not in session:
    #     session['cart'] = []

    # Add the book details to the cart in the session
    # session['cart'].append(book[0])
    # print(session['cart'])
    return True


def get_genre_id(genre_name):
    # Get the genre ID from the database
    query = "SELECT * FROM GENRE WHERE GENRE_NAME = '{}'".format(genre_name)
    result = execute_query(query)

    print(result)

    if result:
        return result[0]['GENRE_ID']

    return None


def get_author_id(author):
    # Get the author ID from the database
    query = "SELECT * FROM AUTHORS WHERE AUTHOR_NAME = '{}'".format(author)
    result = execute_query(query)

    print(result)

    if result:
        return result[0]['AUTHOR_ID']

    return None


def add_customer(customer):
    try:
        num = execute_query("SELECT COUNT(*) FROM CUSTOMERS")
        num = num[0]['COUNT(*)'] + random.randint(10, 200)

        add_customer = ("INSERT INTO CUSTOMERS "
                        "(CUSTOMER_ID, F_NAME, L_NAME, EMAIL, PHONE_NO, ADDRESS, ZIP_CODE) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s)")

        data_customer = (num, customer['FIRST_NAME'], customer['LAST_NAME'], customer['EMAIL'], customer['PHONE'], customer['ADDRESS'], customer['ZIP_CODE'])

        connection = pymysql.connect(host='localhost',
                                     user='anushka',
                                     password='Jeonjungkook97',
                                     db='BookshopDB',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        with connection.cursor() as cursor:
            cursor.execute(add_customer, data_customer)
            result = cursor.fetchall()
            # use commit to save changes made
            connection.commit()
            connection.close()
        # execute_query(
        #     "INSERT INTO CUSTOMERS (CUSTOMER_ID, F_NAME, L_NAME, EMAIL, PHONE_NO, ADDRESS, ZIP_CODE) "
        #     "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".
        #     format(num, customer['CUSTOMER_ID'], customer['FIRST_NAME'], customer['LAST_NAME'], customer['EMAIL'],
        #            customer['PHONE'], customer['ADDRESS'], customer['ZIP_CODE']))
        return True
    except Exception as e:
        # rollback in case there is any error
        connection.rollback()
        return False


def get_user_by_id(user_id):
    # Get the user details from the database
    query = "SELECT * FROM CUSTOMERS WHERE CUSTOMER_ID = '{}'".format(user_id)
    result = execute_query(query)

    print(result)

    if result:
        return result[0]

    return None


def get_user_id(user_name):
    # Split first and last name
    first_name, last_name = user_name.split(' ')

    # Get user ID
    query = "SELECT CUSTOMER_ID FROM CUSTOMERS WHERE F_NAME = '{}' AND L_NAME = '{}'".format(first_name, last_name)
    result = execute_query(query)
    if result.__len__ is 0:
        # If the user doesn't exist, add the user to the database
        # Make sure you get all data from the user which is needed in adding in DB
        return add_customer()
    print(result)
    return result[0]['CUSTOMER_ID']


def delete_customer(customer_id):
    try:
        # Delete customer from the database based on the provided customer_id
        query = "DELETE FROM CUSTOMERS WHERE CUSTOMER_ID = {}".format(customer_id)
        execute_query(query)
        return True
    except Exception as e:
        return False


def update_user(customer):
    try:
        # Update user information in the database
        query = """
            UPDATE CUSTOMERS
            SET FIRST_NAME = '{}', LAST_NAME = '{}', EMAIL = '{}', 
                PHONE_NO = '{}', ADDRESS = '{}', ZIP_CODE = '{}'
            WHERE CUSTOMER_ID = {}
        """.format(
            customer['CUSTOMER.F_NAME'], customer['CUSTOMER.L_NAME'], customer['CUSTOMER.EMAIL'],
            customer['CUSTOMER.PHONE'], customer['CUSTOMER.ADDRESS'], customer['CUSTOMER.ZIP_CODE'],
            customer['CUSTOMER_ID']
        )
        execute_query(query)
        return True
    except Exception as e:
        return False


def delete_book(isbn):
    # get product id
    query = "SELECT PRODUCT_ID FROM BOOKS WHERE ISBN = '{}'".format(isbn)
    result = execute_query(query)
    product_id = result[0]['PRODUCT_ID']

    # Delete the book from the database
    query = "DELETE FROM BOOKSHOPDB.BOOKS WHERE PRODUCT_ID = '{}'".format(product_id)
    execute_query(query)
    return True


def get_sales_report():
    # Modify this function to fetch data from the REVIEWS table
    # For example, fetch books with their ratings from the REVIEWS table
    query = """
        SELECT B.TITLE, B.ISBN, R.RATING
        FROM BOOKS B
        JOIN REVIEWS R ON B.PRODUCT_ID = R.PRODUCT_ID
        ORDER BY R.RATING DESC;
    """
    result = execute_query(query)

    # Return the result as a list of dictionaries
    return result


def get_shopping_cart_items():
    return shopping_cart


def add_payment_info(payment_info):
    # Get new payment ID
    query = "SELECT COUNT(*) FROM PAYMENT_INFO"
    num = execute_query(query)
    num = num[0]['COUNT(*)'] + 1

    query = 'INSERT INTO PAYMENT_INFO (PAYMENT_ID, CUSTOMER_ID, CARD_NUM, CVV, ZIP_CODE, EXP_DATE, ADDRESS) VALUES (\'{}\', ' \
            '\'{}\', \'{}\', \'{}\', \'{}\', \'{}\')'.format(num, payment_info['CUSTOMER_ID'],
                                                             payment_info['CARD_NUM'], payment_info['CVV'],
                                                             payment_info['ZIP_CODE'], payment_info['EXP_DATE'], payment_info['ADDRESS'])

    execute_query(query)


def get_genre_by_id(id):
    return execute_query("SELECT * FROM GENRE WHERE GENRE_ID = '{}'".format(id))


def get_author_by_id(id):
    return execute_query("SELECT * FROM AUTHOR WHERE AUTHOR_ID = '{}'".format(id))


def get_book_by_id(isbn):
    return execute_query("SELECT * FROM BOOKS WHERE ISBN = '{}'".format(isbn))[0]


def update_book(updated_book):
    query = """
        UPDATE BOOKS
        SET TITLE = '{}', GENRE_ID = '{}', AUTHOR_ID = '{}', PUBLICATION_DATE = '{}', ISBN = '{}', AVAILABILITY = '{}', PRICE = '{}'
        WHERE ISBN = '{}'
    """.format(
        updated_book['TITLE'], updated_book['GENRE_ID'], updated_book['AUTHOR_ID'], updated_book['PUBLICATION_DATE'],
        updated_book['ISBN'], updated_book['AVAILABILITY'], updated_book['PRICE'], updated_book['ISBN']
    )
    execute_query(query)


# Add a new function in service.py to get books sorted by publication date
def get_books_sorted_by_date():
    query = "SELECT TITLE, ISBN, PUBLICATION_DATE FROM BOOKS ORDER BY PUBLICATION_DATE DESC"
    result = execute_query(query)
    return result
