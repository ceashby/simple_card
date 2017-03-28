from __future__ import unicode_literals, absolute_import, division
import datetime as dt
from pytz import UTC


# Sign convention -'ve is paid onto card +'ve is paid from card
class Card(object):
    def __init__(self, number, transactions=None):
        self.number = number
        self.transactions = transactions or []

    def get_transaction(self, transaction_id):
        try:
            return self.transactions[transaction_id]
        except IndexError:
            raise CardError('Unrecognised transaction id')

    def check_amount_is_positive(self, amount):
        if amount <= 0:
            raise CardError('Amount must be greater than zero')

    def load(self, amount):
        self.check_amount_is_positive(amount)

        self.transactions.append({
            'datetime': dt.datetime.now(UTC),
            'requested_amount': -amount,
            'captured_amount': -amount
        })

    def authorise(self, amount):
        self.check_amount_is_positive(amount)
        if amount > self.get_amount_available():
            raise CardError('There is not enough available on the card')

        self.transactions.append({
            'datetime': dt.datetime.now(UTC),
            'requested_amount': amount,
            'captured_amount': 0,
        })
        return len(self.transactions) - 1

    def reverse(self, transaction_id, amount):
        self.check_amount_is_positive(amount)
        transaction = self.transactions[transaction_id]

        if amount > transaction['requested_amount'] - transaction['captured_amount']:
            raise CardError('You can not reverse more than was authorised and remains uncaptured')

        transaction['requested_amount'] -= amount

    def capture(self, transaction_id, amount):
        self.check_amount_is_positive(amount)
        transaction = self.transactions[transaction_id]

        if amount > transaction['requested_amount'] - transaction['captured_amount']:
            raise CardError('You can not capture more than was authorised and remains uncaptured')

        transaction['captured_amount'] += amount

    def refund(self, transaction_id, amount):
        self.check_amount_is_positive(amount)
        transaction = self.transactions[transaction_id]

        if amount > transaction['captured_amount']:
            raise CardError('You can not refund more than was paid')

        transaction['captured_amount'] -= amount

    def get_balance(self):
        return -sum(r['captured_amount'] for r in self.transactions)

    def get_amount_available(self):
        # This assumes amounts requested but not captured are considered unavailable
        return -sum(r['requested_amount'] for r in self.transactions)

    def get_amount_blocked(self):
        return self.get_balance() - self.get_amount_available()

    def get_amount_loaded(self):
        return -sum(r['requested_amount'] for r in self.transactions if r['requested_amount'] < 0)

class CardError(Exception):
    pass