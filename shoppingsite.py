"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken, Katie Byers.
"""

from flask import Flask, render_template, redirect, flash, session, request
import jinja2

import melons
import customers

app = Flask(__name__)

# A secret key is needed to use Flask sessioning features
app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.
app.jinja_env.undefined = jinja2.StrictUndefined

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.jinja")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    return render_template("all_melons.jinja",
                           melon_list=melon_list)


@app.route("/melon/<melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)
    return render_template("melon_details.jinja",
                           display_melon=melon)


@app.route("/add_to_cart/<melon_id>")
def add_to_cart(melon_id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Melon successfully added to
    cart'."""

    session["cart"] = session.get("cart", {})
    session["cart"][melon_id] = session["cart"].get(melon_id, 0) + 1

    melon = melons.get_by_id(melon_id)
    melon_name = melon.common_name

    flash(f"You've added {melon_name} to your cart")
    return redirect("/cart")


@app.route("/cart")
def show_shopping_cart():
    """Display content of shopping cart."""

    # Initialize cart variable to session cart
    cart = session.get("cart", {})

    # Initialize checkout cart list and order total
    melon_cart = []
    order_total = 0

    # Loop through session cart and retrieve melon id and qty
    for melon_id, melon_qty in cart.items():

        # For each melon id, get melon object from melons.py
        # and append it to melon cart list
        melon = melons.get_by_id(melon_id)
        melon_cart.append(melon)

        # Update melon object qty and total price
        melon.quantity = melon_qty
        melon.total_price = melon.quantity * melon.price

        # Update order total based on melon total price
        order_total += melon.total_price

    # Render cart template with melon cart and order total formatted with two decimal points
    return render_template("cart.jinja", melon_cart=melon_cart, order_total=f"{order_total:.2f}")


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.jinja")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    # Get user-provided name and password from request.form
    email = request.form.get("email")
    password = request.form.get("password")

    # Use customers.get_by_email() to retrieve corresponding Customer object (if any)
    customer = customers.get_by_email(email)

    # If a Customer with that email was not found, flash a failure message and redirect back to "/login"
    if not customer:
        flash("No customer with that email found!")
        return redirect("/login")

    # If a Customer with that email was found, and the entered password does not match the customer's password, flash a failure message and redirect back to "/login"
    if customer.password != password:
        flash("Incorrect password!")
        return redirect("/login")

    # If Customer is found and entered password matches the customer's password, store the user's email in the session, flash a success message and redirect the user to the "/melons" route
    flash("Login successful!")
    session["email"] = customer.email
    return redirect("/melons")


@app.route("/logout", methods=["GET"])
def process_logout():
    """Redirect user back to melon page upon logout."""

    del session["email"]
    flash("Successfully logged you out!")
    return redirect("/melons")


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
