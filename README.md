# QuickCart — E-Commerce Web App with Selenium Test Automation

A fully functional e-commerce web application built with Flask, paired with a comprehensive Selenium + PyTest automated test suite. Built as a college project to demonstrate end-to-end web automation testing skills.

## 🛒 Features

- **User Authentication** — Registration with validation, login/logout
- **Product Catalog** — 18 products across 4 categories (Electronics, Fashion, Shoes, Books), search, and category filtering
- **Shopping Cart** — Add/remove items, live quantity adjustment (+/-), automatic total calculation
- **Wishlist** — Save items for later, move to cart, remove
- **Checkout** — Address form with validation (phone, pincode), delivery option (Standard/Express) with live estimated delivery date
- **Payment** — UPI, Card, and Cash on Delivery, with correct payment status handling (Paid vs Pending)
- **Order Management** — Order history, order details, cancel order

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Frontend | HTML, CSS (custom design system), Jinja2 templates |
| Data | In-memory Python data structures (session-based cart/wishlist/orders) |
| Test Automation | Selenium WebDriver, PyTest |
| Reporting | pytest-html |

## 📁 Project Structure

```
quickcart/
├── app.py                  # Flask application and all routes
├── static/
│   ├── css/style.css       # Site-wide styling
│   └── images/             # Product photos
├── templates/               # All HTML/Jinja2 templates
│   ├── login.html
│   ├── register.html
│   ├── home.html
│   ├── products.html
│   ├── product.html
│   ├── cart.html
│   ├── wishlist.html
│   ├── checkout.html
│   ├── payment.html
│   ├── orders.html
│   ├── order_detail.html
│   └── order_confirmation.html
└── tests/                   # Selenium + PyTest test suite
    ├── test_login.py
    ├── test_registration.py
    ├── test_products.py
    ├── test_cart.py
    ├── test_wishlist.py
    ├── test_checkout.py
    ├── test_payment.py
    ├── test_orders.py
    └── test_navigation.py
```

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Google Chrome browser

### Installation


# Clone the repository
git clone https://github.com/<your-username>/quickcart.git
cd quickcart

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install flask selenium pytest pytest-htm

### Running the app

```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your browser.

**Test login credentials:** `test@gmail.com` / `password123`

## 🧪 Running the Tests

Make sure the Flask app is running in one terminal, then in a second terminal:

```bash
# Run a single test file
pytest tests/test_login.py -v

# Run the entire suite
pytest tests/ -v

# Generate an HTML report
pytest tests/ -v --html=report.html --self-contained-html
```

## 📋 Test Coverage

| Module | Test Cases |
|---|---|
| Login | 5 |
| Registration | 5 |
| Products (search/filter) | 5 |
| Cart | 7 |
| Wishlist | 4 |
| Checkout | 5 |
| Payment | 4 |
| Orders | 4 |
| Navigation | 1 |
| **Total** | **~40** |

## 👤 Author

Built as a Software Testing college project demonstrating Selenium WebDriver, PyTest, and web application development skills.
