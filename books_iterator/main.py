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
        # create an instance of `Price`, using the book's attributes
        return Price(self.price_amount, self.price_currency)

    def __str__(self):
        # check the string format in the unit tests
        # 'Harry Potter (by J. K. Rowling) - USD$20.00'
        return "{} (by {}) - {}${}".format(self.title, self.authors, self.price_currency, self.price_amount)


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
        
        #???
        other_amount = other.get_value(self.currency)
        return Price(self.amount + other_amount, self.currency)
        

    def __eq__(self, other):
        # compare if two prices are equal. Keep in mind that both prices
        # might have different currencies. Use the `.get_value()` function
        # to transform prices to a comparable currency.
        
        if self.get_value() == other.get_value(self.currency):
            return True  
        return False

    def __ne__(self, other):
        # opposite to __eq__
        if self.get_value() != other.get_value():
            return False
        else:
            return True

    def get_value(self, currency=None):
        # if no currency is given, returns the current price amount. If a
        # different currency is given, handles the price convertion to the
        # given currency. Use the `EXCHANGE_RATES` dict for that.
        if currency == None:
            return self.amount
        if self.currency != currency:
            return self.amount * self.EXCHANGE_RATES[self.currency][currency]
        return self.amount


class BookIterator(object):
    def __init__(self, file_path):
        self.books = read_file_line_by_line(file_path)
        self.counter = 0

    def __iter__(self):
        # return BookIterator(self.file_path)
        self.counter = 0
        return self
    
    def __next__(self):
        # make sure each execution of __next__ returns an instance
        # of the `Book` class.
        
        # if --something--:
        #     raise StopIteration
        """
        my_func(1, 2, 3)
        t = (1,2,3)
        my_func(*t)
        d = {'a':1, 'b': 2}
        my_func(**d)
        my_func(a=1, b=2)
        """
        if self.counter < len(self.books):
        
            current_book = Book(*self.books[self.counter])
            self.counter += 1
            return current_book
        else:
        
            raise StopIteration()
            


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


# class StringIterator():
#     def __init__(self, string_to_iter):
#         self.s = string_to_iter
#         self.pos = 0
        
#     def __iter__(self):
#         self.pos = 0
#         return self
        
#     def __next__(self):
#         if self.pos < len(self.s):
#             char = self.s[self.pos]
#             self.pos +=1
#             return char
#         else:
#             raise StopIteration

#     next = __next__
            
# my_iter = StringIterator('stuff')
# for c in my_iter:
#     print(c)
    
# for c in "stuff":
#     print(c)