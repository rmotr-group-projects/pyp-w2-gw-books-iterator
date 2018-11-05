from decimal import Decimal


class Book(object):
    def __init__(self, title, authors, price_amount, price_currency):
        # initialize attributes
        self.title = title
        self.authors = authors
        self.price_amount = price_amount
        self.price_currency = price_currency
        pass

    @property
    def price(self):
        # create an instance of `Price`, using the book's attributes
        return Price(self.price_amount, self.price_currency)

    def __str__(self):
        return str('{} (by {}) - {}${}'.format(self.title, self.authors, self.price_currency, self.price_amount))


class Price(object):
    EXCHANGE_RATES = {
        'USD': {
            'EUR': Decimal('0.89'),
            'YEN': Decimal('109.8')
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

    def __str__(self):
        return str(self.currency, self.amount)

    def get_currency(self):
        return self.currency
    
    def get_value(self, currency=None):
        # if no currency is given, returns the current price amount. If a
        # different currency is given, handles the price convertion to the
        # given currency. Use the `EXCHANGE_RATES` dict for that.
        if currency is None or currency == self.currency:
            return self.amount
        else:
            return self.amount * Price.EXCHANGE_RATES[self.currency][currency]
        
    def __add__(self, other):
        # return a new `Price` instance, representing the sum of
        # both given ones
        return Price(self.get_value(self.currency) + other.get_value(self.currency))
        pass

    def __eq__(self, other):
        # compare if two prices are equal. Keep in mind that both prices
        # might have different currencies. Use the `.get_value()` function
        # to transform prices to a comparable currency.
        return self.get_value('USD') == other.get_value('USD')

    def __ne__(self, other):
        # opposite to __eq__
        return self.get_value('USD') != other.get_value('USD')


def read_file_line_by_line(file_path):
    file_lines = []
    file_obj = open(file_path, 'r')
    try:
        line = file_obj.readline()
        while line:
            book_data = [l.strip() for l in line.split(',')]
            file_lines.append(book_data)
            line = file_obj.readline()
    finally:
        file_obj.close()
    return file_lines
    

class BookIterator(object):
    def __init__(self, file_path):
        self.file = read_file_line_by_line(file_path)
        self.count = 0

    def __iter__(self):
        self.count = 0
        return self
        
    def __next__(self):
        # make sure each execution of __next__ returns an instance
        # of the `Book` class.
        if self.count >= len(self.file):
            raise StopIteration()
        res = Book(*self.file[self.count])
        self.count += 1
        return res

    next = __next__


