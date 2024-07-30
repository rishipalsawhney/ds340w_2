import re

from flask import Flask, render_template, request, redirect, url_for, session
from requests import Session
from sqlalchemy.exc import SQLAlchemyError

import service
from CheckoutPage import CheckoutForm

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
sess = Session()

user_role = ''


@app.route('/', methods=['GET', 'POST'])
def login():
    global user_role
    user_role = ''
    # Initialize the shopping cart in the session
    if 'cart' in session:
        session['cart'] = []
    if request.method == 'POST':
        # Retrieve form data
        username = request.form['username']
        password = request.form['password']

        # call the login_details function from service.py
        result = service.login_details(username, password)

        if result:
            role = result[0]['ROLE']

            if role == 'Customer':
                # Redirect to the customer index page
                session['ROLE'] = 'Customer'
                user_role = role
                return redirect('/indexCustomer')
            else:
                # Redirect to the admin index page for non-customers
                session['ROLE'] = 'Admin'
                user_role = role
                return redirect('/admin_index')  # Changed from '/index' to '/admin_index'

        # Handle unsuccessful login
        error_message = "Invalid username or password"
        return render_template("Login.html", error=error_message)

    # If the request method is not 'POST', render the login page
    return render_template("Login.html")


@app.route('/indexCustomer')
def index():
    return render_template("indexCustomer.html")


@app.route('/admin_index')
def adminindex():
    if 'ROLE' in session:
        if session['ROLE'] == 'Admin':
            return render_template("adminindex.html")

    return redirect('/indexCustomer')
    # return render_template("adminindex.html")


@app.route('/books')
def books():
    global user_role
    books = service.get_books()
    q = request.args.get('sort')
    if q == 'price':
        books = sorted(books, key=lambda i: i['PRICE'])
    elif q == 'title':
        books = sorted(books, key=lambda i: i['TITLE'])
    print(user_role)
    return render_template('books.html', books=books, user_role=user_role)


@app.route('/contact-us')
def contact_us():
    return render_template('ContactUs.html')


@app.route('/accounts')
def accounts():
    return render_template('Account.html')


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    # Your create account logic goes here
    return render_template('create_account.html')


@app.route('/shoppingcart')
def shopping_cart():
    # Check if the 'cart' key is present in the session
    # if 'cart' in session:
    #     shopping_cart_items = session['cart']
    # else:
    #     shopping_cart_items = []
    shopping_cart_items = service.get_shopping_cart_items()

    # shopping_cart_items = service.get_shopping_cart_items()
    # Render the shopping cart template with the cart items
    total_price = 0
    for item in shopping_cart_items:
        if 'Decimal' in str(item['PRICE']):
            price = float(re.findall("\d+\.\d+", item['PRICE'])[0])
        else:
            price = float(item['PRICE'])
        print('price: ', price)
        total_price += price

    return render_template('shoppingcart.html', shopping_cart_items=shopping_cart_items, total_price=total_price)


@app.route('/recommend-us')
def recommend_us():
    return render_template('RecommendUs.html')


@app.route('/delete_customer', methods=['POST'])
def delete_customer_get():
    # Retrieve the selected customer ID from the form
    customer_id = request.form['customer_id']

    # Perform the deletion operation in the database
    success = service.delete_customer(customer_id)

    if success:
        return redirect(url_for('admin_index'))
    else:
        return 'Failed to delete customer. Please try again.'

    @app.route('delete_customer')
    def delete_customer():
        return render_template('delete_customer.html')


# Add this route for submitting recommendations
@app.route('/submit-recommendation', methods=['POST'])
def submit_recommendation():
    book_isbn = request.form['isbn']
    book_name = request.form['bookTitle']
    author_name = request.form['Author']
    recommendation = request.form['Recommendation']
    result = service.add_recommendation(book_isbn, book_name, author_name, recommendation)
    print(result)
    if result:
        return 'Thanks for adding the book! You\'ve got great recommendations. Keep an eye on the email to get updates'
    else:
        return 'Sorry, we could not add the book. Please try again later.'


# def get_book_details_by_name(book_name):
# Assuming 'books' is your list of books
# for book in Books:
# if book['name'].lower() == book_name.replace('-', ' ').lower():
# return book

# Return None if the book is not found
# return None


@app.route('/book/<isbn>')
def book_detail_page(isbn):
    book = service.get_book_details_by_isbn(isbn)
    book = book[0]
    genre = service.get_genre_by_id(book['GENRE_ID'])
    author = service.get_author_by_id(book['AUTHOR_ID'])
    book['GENRE_NAME'] = genre[0]['GENRE_NAME']
    book['AUTHOR_NAME'] = author[0]['AUTHOR_F_NAME'] + ' ' + author[0]['AUTHOR_L_NAME']
    print(book)
    return render_template('book_details_page.html', book=book)


@app.route('/ContactUs', methods=['POST'])
def process_return():
    if request.method == 'POST':
        # Retrieve form data
        order_id = request.form['order_id']
        issue = request.form['issue']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        customer_id = request.form['customer_id']

        # TODO: Insert data into the ContactUs table
        # Uncomment and modify the code according to your database schema
        # Assuming you have a service method to handle database operations
        result = service.process_return(order_id, issue, first_name, last_name, customer_id)

        if result:
            # Redirect to a page confirming the return processing
            return render_template('return_processed.html', result='success', order_id=order_id)
        else:
            # Handle the case where return processing fails
            return render_template('return_processed.html', result='failure')

    # If the request method is not POST, you might want to handle it differently
    return redirect(url_for('indexCustomer'))  # Redirect to the home page or another suitable route


@app.route('/refund_page')
def refund_page():
    # Logic for refund page goes here
    return render_template('refund_page.html')


@app.route('/replacement_page')
def replacement_page():
    # Logic for replacement page goes here
    return render_template('replacement_page.html')


@app.route('/add-to-cart/<isbn>')
def add_to_cart(isbn):
    success = service.add_to_cart(isbn)
    if success:
        return redirect('/shoppingcart')
    else:
        return render_template('books.html')


@app.route('/add-book', methods=['GET'])
def add_book_get():
    return render_template('Addbook.html')


@app.route('/add-book', methods=['POST'])
def add_book_post():
    # Extract data from the form
    title = request.form['title']
    author_id = request.form['author_id']
    genre_name = request.form['genre_name']
    publication_date = request.form['publication_date']
    isbn = request.form['isbn']
    availability = request.form['availability']
    price = request.form['price']

    genre_id = service.get_genre_id(genre_name)

    availability = 1 if availability == 'on' else 0

    # Create a new Book instance
    new_book = dict(
        TITLE=title,
        AUTHOR_ID=author_id,
        GENRE_ID=genre_id,
        PUBLICATION_DATE=publication_date,
        ISBN=isbn,
        AVAILABILITY=availability,
        PRICE=price
    )

    service.add_book(new_book)

    return redirect('/books')


@app.route('/delete-book/<isbn>')
def delete_book(isbn):
    service.delete_book(isbn)
    return redirect('/books')


@app.route('/add-customer', methods=['GET'])
def add_customer_get():
    return render_template('addcustomer.html')


@app.route('/add-customer', methods=['POST'])
def add_customer():
    # Retrieve data from the form
    customer_id = request.form['customer_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    phone = request.form['phone']
    address = request.form['address']
    zip_code = request.form['zip_code']

    # Create a new Customer instance
    new_customer = dict(
        CUSTOMER_ID=customer_id,
        FIRST_NAME=first_name,
        LAST_NAME=last_name,
        EMAIL=email,
        PHONE=phone,
        ADDRESS=address,
        ZIP_CODE=zip_code
    )
    service.add_customer(new_customer)

    return redirect('/admin_index')

@app.route('/delete-customer')
def show_users():
    users = service.get_users()
    return render_template('show-customer.html', users=users)

@app.route('/update-customer/<user_id>')
def update_user(user_id):
    if request.method == 'GET':
        # Retrieve the existing user information
        user = service.get_user_by_id(user_id)
        if user:
            return render_template('update-customer.html', CUSTOMERS=user)
        else:
            return 'User not found'  # Handle the case where the user is not found
    elif request.method == 'POST':
        # Handle the form submission to update user information
        updated_user = {
            'user_id': user_id,
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'address': request.form['address'],
            'zip_code': request.form['zip_code']
        }
        success = service.update_user(updated_user)
        return redirect(url_for('/admin_index'))


# @app.route('/update-book/<isbn>', methods=['GET'])
# def update_book_get(isbn):
#     book = service.get_book_by_id(isbn)
#     return render_template('update-books.html', book=book)

@app.route('/update-book/<isbn>', methods=['GET'])
def update_book_get(isbn):
    # Retrieve the existing book information
    book = service.get_book_by_id(isbn)
    if book:
        return render_template('update-books.html', book=book)
    else:
        return 'Book not found'

@app.route('/update-book/<isbn>', methods=['POST'])
def update_book(isbn):
    # Handle the form submission to update book information
    updated_book = {
        'ISBN': isbn,
        'TITLE': request.form['title'],
        'GENRE_ID': request.form['genre_id'],
        'PUBLICATION_DATE': request.form['publication_date'],
        'AVAILABILITY': request.form['availability'],
        'PRICE': request.form['price'],
        'AUTHOR_ID': request.form['author_id'],
        # Add other fields as needed
    }
    service.update_book(updated_book)

    return redirect(url_for('/books'))


@app.route('/create-report')
def create_report():
        #Books are sorted by their publication date
        books = service.get_books_sorted_by_date()
        return render_template('create-report.html', books=books)




@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['nameLabel']
        card_number = request.form['cardNumberLabel']
        cvv = request.form['cvvLabel']
        zip_code = request.form['zipCodeLabel']
        expiry_date = request.form['expiryDateLabel']
        address = request.form['addressLabel']

        cust_id = service.get_user_id(name)

        payment_info = dict(CUSTOMER_ID=cust_id, CARD_NUM=card_number, CVV=cvv, ZIP_CODE=zip_code, EXP_DATE=expiry_date, ADDRESS=address)

        service.add_payment_info(payment_info)
        return redirect('/indexCustomer')

    return render_template('checkout.html')


def db():
    return None


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    # sess.init_app(app)
    app.run(debug=True, host='0.0.0.0', port=8000)
