from decimal import Decimal

class Book(object):
    def __init__(self, title, authors, price_amount, price_currency):
        # initialize attributes
        self.title = title
        self.authors = authors
        self.price_currency = price_currency
        self.price_amount = price_amount

    @property
    def price(self):
        # create an instance of `Price`, using the book's attributes
        return Price(self.price_amount, self.price_currency)

    def __str__(self):
        # check the string format in the unit tests
        return "{} (by {}) - {}${}".format(
               self.title, self.authors, self.price_currency, self.price_amount)


class Price(object):
    EXCHANGE_RATES = {
        'USD': {
            'EUR': Decimal('0.89'),
            'YEN': Decimal('109.8'),
        },
        'EUR': {
            'USD': Decimal('1.13'),
            'YEN': Decimal('123.6')
        },
        'YEN': {
            'USD': Decimal('0.0091'),
            'EUR': Decimal('0.0081')
        },
    }

    def __init__(self, amount, currency='USD'):
        self.amount = amount
        self.currency = currency

    def get_currency(self):
        return self.currency

    def get_value(self, currency=None):
        # if no currency is given, returns the current price amount. If a
        # different currency is given, handles the price convertion to the
        # given currency. Use the `EXCHANGE_RATES` dict for that.
        if not currency or (currency == self.currency):
            return self.amount
        else:
            return Price.EXCHANGE_RATES[self.currency][currency] * self.amount

    def __str__(self):
        return "{} {}".format(self.currency, self.amount)

    def __add__(self, other):
        # return a new `Price` instance, representing the sum of
        # both given ones
        return Price(self.get_value() + other.get_value(self.currency))

    def __eq__(self, other):
        # compare if two prices are equal. Keep in mind that both prices
        # might have different currencies. Use the `.get_value()` function
        # to transform prices to a comparable currency.
        if self.get_value('USD') == other.get_value('USD'):
            return True

    def __ne__(self, other):
        # opposite to __eq__
        if self.get_value('USD') != other.get_value('USD'):
            return False


class BookIterator(object):
    def __init__(self, file_path):
        self.values = read_file_line_by_line(file_path)
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.count < len(self.values):
            self.count += 1
            return Book(*self.values[self.count-1])
        else:
            self.count = 0
            raise StopIteration

    next = __next__
    
def read_file_line_by_line(file_path):
    with open(file_path, 'r') as f_obj:
        return [line.rstrip().split(',') for line in f_obj.readlines()]


