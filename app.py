import re

from flask import Flask, render_template, request, redirect, session

from datetime import datetime, timedelta


app = Flask(__name__)

app.secret_key = 'dev-secret-key-change-later'


# Product Data
PRODUCTS = [
    {
        'id': 'laptop',
        'name': 'Laptop',
        'price': 50000,
        'category': 'Electronics',
        'image': 'laptop.jpg'
    },
    {
        'id': 'headphones',
        'name': 'Headphones',
        'price': 2000,
        'category': 'Electronics',
        'image': 'headphones.jpg'
    },
    {
        'id': 'smartphone',
        'name': 'iphone',
        'price': 150000,
        'category': 'Electronics',
        'image': 'smartphone.jpg'
    },
    {
        'id': 'smartwatch',
        'name': 'Smartwatch',
        'price': 4500,
        'category': 'Electronics',
        'image': 'smartwatch.jpg'
    },
    {
        'id': 'speaker',
        'name': 'Bluetooth Speaker',
        'price': 1800,
        'category': 'Electronics',
        'image': 'speaker.jpg'
    },
    {
        'id': 'tshirt',
        'name': 'Cotton T-Shirt',
        'price': 500,
        'category': 'Fashion',
        'image': 'tshirt.jpg'
    },
    {
        'id': 'jeans',
        'name': 'Blue Jeans',
        'price': 1200,
        'category': 'Fashion',
        'image': 'jeans.jpg'
    },
    {
        'id': 'jacket',
        'name': 'Denim Jacket',
        'price': 2200,
        'category': 'Fashion',
        'image': 'jacket.jpg'
    },
    {
        'id': 'shoes',
        'name': 'Running Shoes',
        'price': 1500,
        'category': 'Shoes',
        'image': 'shoes.jpg'
    },
    {
        'id': 'sneakers',
        'name': 'White Sneakers',
        'price': 1800,
        'category': 'Shoes',
        'image': 'sneakers.jpg'
    },
    {
        'id': 'novel',
        'name': 'Mystery Novel',
        'price': 300,
        'category': 'Books',
        'image': 'novel.jpg'
    },
    {
        'id': 'cookbook',
        'name': 'Cookbook',
        'price': 450,
        'category': 'Books',
        'image': 'cookbook.jpg'
    },
    {
        'id': 'frock',
        'name': 'Onepiece',
        'price': 1000,
        'category': 'Fashion',
        'image': 'frock.jpg'
    },
    {
        'id': 'iphone',
        'name': 'iphone 16 pro max',
        'price': 135000,
        'category': 'Electronics',
        'image': 'iphone.jpg'
    },
    {
        'id': 'kurtha',
        'name': 'Short Kurtha',
        'price': 450,
        'category': 'Fashion',
        'image': 'kurtha.jpg'
    },
    {
        'id': 'macbook',
        'name': 'Macbook',
        'price': 100000,
        'category': 'Electronics',
        'image': 'macbook.jpg'
    },
    {
        'id': 'biography',
        'name': 'Biography',
        'price': 400,
        'category': 'Books',
        'image': 'sketch.jpg'
    },
    {
        'id': 'onepiece',
        'name': 'Onepiece',
        'price': 800,
        'category': 'Fashion',
        'image': 'onepiece.jpg'
    }
]


USERS = {
    'test@gmail.com': 'password123'
}


@app.route('/')
def home():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():

    error = None

    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')

        if email in USERS and USERS[email] == password:
            return redirect('/home')

        else:
            error = 'Invalid email or password'

    return render_template(
        'login.html',
        error=error
    )


@app.route('/home')
def home_page():

    return render_template(
        'home.html',
        products=PRODUCTS
    )


@app.route('/products')
def products():

    query = request.args.get('search', '').lower()
    category = request.args.get('category', '')

    results = PRODUCTS

    if query:
        results = [
            p for p in results
            if query in p['name'].lower()
        ]

    if category:
        results = [
            p for p in results
            if p['category'] == category
        ]

    return render_template(
        'products.html',
        products=results,
        query=query
    )


@app.route('/product/<product_id>')
def product_detail(product_id):

    product = next(
        (p for p in PRODUCTS if p['id'] == product_id),
        None
    )

    if not product:
        return 'Product not found', 404

    return render_template(
        'product.html',
        product=product
    )


@app.route('/add-to-cart/<product_id>', methods=['POST'])
def add_to_cart(product_id):

    quantity_text = request.form.get(
        'quantity',
        '1'
    )

    if not quantity_text:
        quantity = 1
    else:
        quantity = int(quantity_text)

    cart = session.get(
        'cart',
        {}
    )

    if product_id in cart:
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity

    session['cart'] = cart

    return redirect('/cart')


@app.route('/cart')
def cart():

    cart_data = session.get('cart', {})

    items = []
    total = 0

    for product_id, qty in cart_data.items():

        product = next(
            (p for p in PRODUCTS if p['id'] == product_id),
            None
        )

        if product:

            subtotal = product['price'] * qty

            total += subtotal

            items.append({
                'product': product,
                'quantity': qty,
                'subtotal': subtotal
            })

    return render_template(
        'cart.html',
        items=items,
        total=total
    )


@app.route('/remove-from-cart/<product_id>', methods=['POST'])
def remove_from_cart(product_id):

    cart = session.get('cart', {})

    if product_id in cart:
        del cart[product_id]

    session['cart'] = cart

    return redirect('/cart')


@app.route('/update-cart/<product_id>', methods=['POST'])
def update_cart(product_id):
    action = request.form.get('action')

    cart = session.get('cart', {})

    if product_id in cart:

        if action == 'increase':
            cart[product_id] += 1

        elif action == 'decrease':
            cart[product_id] = max(
                1,
                cart[product_id] - 1
            )

    session['cart'] = cart

    return redirect('/cart')


@app.route('/add-to-wishlist/<product_id>', methods=['POST'])
def add_to_wishlist(product_id):

    wishlist = session.get('wishlist', [])

    if product_id not in wishlist:
        wishlist.append(product_id)

    session['wishlist'] = wishlist

    return redirect('/wishlist')


@app.route('/wishlist')
def wishlist():

    wishlist_ids = session.get('wishlist', [])

    items = [
        p for p in PRODUCTS
        if p['id'] in wishlist_ids
    ]

    return render_template(
        'wishlist.html',
        items=items
    )


@app.route('/remove-from-wishlist/<product_id>', methods=['POST'])
def remove_from_wishlist(product_id):

    wishlist = session.get('wishlist', [])

    if product_id in wishlist:
        wishlist.remove(product_id)

    session['wishlist'] = wishlist

    return redirect('/wishlist')


@app.route('/wishlist-to-cart/<product_id>', methods=['POST'])
def wishlist_to_cart(product_id):

    wishlist = session.get('wishlist', [])

    if product_id in wishlist:
        wishlist.remove(product_id)

    session['wishlist'] = wishlist

    cart = session.get('cart', {})

    cart[product_id] = cart.get(product_id, 0) + 1

    session['cart'] = cart

    return redirect('/cart')


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():

    errors = []
    form_data = {}

    if request.method == 'POST':

        form_data = {
            'name': request.form.get(
                'name', ''
            ).strip(),

            'phone': request.form.get(
                'phone', ''
            ).strip(),

            'address': request.form.get(
                'address', ''
            ).strip(),

            'city': request.form.get(
                'city', ''
            ).strip(),

            'pincode': request.form.get(
                'pincode', ''
            ).strip(),

            'delivery': request.form.get(
                'delivery',
                'Standard'
            )
        }

        if not form_data['name']:
            errors.append('Name is required')

        if not form_data['address']:
            errors.append('Address is required')

        if not form_data['city']:
            errors.append('City is required')

        if not (
            form_data['phone'].isdigit()
            and len(form_data['phone']) == 10
        ):
            errors.append(
                'Phone must be exactly 10 digits'
            )

        if not (
            form_data['pincode'].isdigit()
            and len(form_data['pincode']) == 6
        ):
            errors.append(
                'Pincode must be exactly 6 digits'
            )

        # Calculate estimated delivery
        if not errors:

            days = (
                2
                if form_data['delivery'] == 'Express'
                else 6
            )

            delivery_date = (
                datetime.now() + timedelta(days=days)
            ).strftime(
                '%A, %d %b %Y'
            )

            form_data['estimated_delivery'] = delivery_date

            session['shipping'] = form_data

            return redirect('/payment')

    return render_template(
        'checkout.html',
        errors=errors,
        form=form_data
    )


@app.route('/payment', methods=['GET', 'POST'])
def payment():

    cart_data = session.get('cart', {})

    total = sum(
        next(
            (
                p['price']
                for p in PRODUCTS
                if p['id'] == pid
            ),
            0
        ) * qty
        for pid, qty in cart_data.items()
    )

    if request.method == 'POST':

        order_id = (
            'ORD' +
            str(
                1000 +
                len(session.get('orders', [])) +
                1
            )
        )

        method = request.form.get(
            'method',
            'UPI'
        )

        # Set payment status
        payment_status = (
            'Pending (Pay on Delivery)'
            if method == 'COD'
            else 'Paid'
        )

        # Create order
        order = {
            'id': order_id,
            'total': total,
            'method': method,
            'payment_status': payment_status,
            'shipping': session.get(
                'shipping',
                {}
            ),
            'status': 'Processing'
        }

        orders = session.get(
            'orders',
            []
        )

        orders.append(order)

        session['orders'] = orders

        session['cart'] = {}

        return render_template(
            'order_confirmation.html',
            order=order
        )

    return render_template(
        'payment.html',
        total=total
    )


@app.route('/orders')
def orders():

    orders_list = session.get(
        'orders',
        []
    )

    return render_template(
        'orders.html',
        orders=orders_list
    )


@app.route('/order/<order_id>')
def order_detail(order_id):

    orders_list = session.get(
        'orders',
        []
    )

    order = next(
        (
            o
            for o in orders_list
            if o['id'] == order_id
        ),
        None
    )

    if not order:
        return 'Order not found', 404

    return render_template(
        'order_detail.html',
        order=order
    )


@app.route(
    '/cancel-order/<order_id>',
    methods=['POST']
)
def cancel_order(order_id):

    orders_list = session.get(
        'orders',
        []
    )

    for o in orders_list:

        if o['id'] == order_id:
            o['status'] = 'Cancelled'

    session['orders'] = orders_list

    return redirect(
        '/order/' + order_id
    )


@app.route('/register', methods=['GET', 'POST'])
def register():

    error = None
    name = ''
    email = ''

    if request.method == 'POST':

        name = request.form.get(
            'name',
            ''
        ).strip()

        email = request.form.get(
            'email',
            ''
        ).strip()

        password = request.form.get(
            'password',
            ''
        )

        confirm_password = request.form.get(
            'confirm_password',
            ''
        )

        email_pattern = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'

        if (
            not name
            or not email
            or not password
            or not confirm_password
        ):
            error = 'All fields are required'

        elif not re.match(
            email_pattern,
            email
        ):
            error = 'Please enter a valid email address'

        elif email in USERS:
            error = (
                'An account with this email '
                'already exists'
            )

        elif password != confirm_password:
            error = 'Passwords do not match'

        else:

            USERS[email] = password

            return redirect('/login')

    return render_template(
        'register.html',
        error=error,
        name=name,
        email=email
    )


if __name__ == '__main__':
    app.run(debug=True)