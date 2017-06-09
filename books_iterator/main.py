from decimal import Decimal


class Book(object):
    def __init__(self, title, authors, price_amount, price_currency):
        # initialize attributes
        self.title = title
        self.authors = authors
        self.price_amount = price_amount
        self.price_currency = price_currency

    @property
    def price(self):
        return Price(self.price_amount, self.price_currency)

    def __str__(self):
        # check the string format in the unit tests
        return '{} (by {}) - {}${}'.format(self.title, self.authors, self.price_currency, self.price_amount)


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
        pass

    def get_currency(self):
        return self.currency

    def __add__(self, other):
        # return a new `Price` instance, representing the sum of
        # both given ones
        return Price(self.amount + other.get_value(self.get_currency()))
        

    def __eq__(self, other):
        # compare if two prices are equal. Keep in mind that both prices
        # might have different currencies. Use the `.get_value()` function
        # to transform prices to a comparable currency.
        return self.amount == other.get_value(self.get_currency())

    def __ne__(self, other):
        # opposite to __eq__
        return self.amount != other.get_value(self.get_currency())

    def get_value(self, currency=None):
        # compare currency of object to the currency passed to this function
        # if no currency is given, returns the current price amount. If a
        # different currency is given, handles the price convertion to the
        # given currency. Use the `EXCHANGE_RATES` dict for that.
        if currency is None or currency is self.currency:
            return self.amount
        else:
            return self.amount * self.EXCHANGE_RATES[self.currency][currency]
            # return USD * EXCHANGE_RATES[USD][EUR value]



class BookIterator(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.count = 0 
        self.book_lists = read_file_line_by_line(self.file_path)
        
    def __iter__(self):
        self.count = 0
        return self

    def __next__(self):
        # make sure each execution of __next__ returns an instance
        # of the `Book` class.
        if self.count >= len(self.book_lists):
            raise StopIteration
        item = Book(*self.book_lists[self.count])
        self.count += 1
        return item        


    next = __next__


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
