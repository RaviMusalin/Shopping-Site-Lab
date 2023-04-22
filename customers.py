"""Customers at Hackbright."""


class Customer:
    """Ubermelon customer."""

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def __repr__(self):
        """Convenience method to show information about a customer in console."""

        return (f"<Customer: {self.first_name} {self.last_name}, {self.email}")


def read_customers_from_file():
    """Read customer data from file."""

    customer_dict = {}
    with open("customers.txt") as file:
        for line in file:
            first_name, last_name, email, password = line.rstrip().split("|")
            new_customer = Customer(first_name, last_name, email, password)

            customer_dict[email] = new_customer

    return customer_dict


def get_by_email(email):
    """Return customer object via passed in email."""

    customer_dict = read_customers_from_file()
    return customer_dict.get(email, None)
