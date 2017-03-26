from __future__ import unicode_literals, absolute_import, division
from unittest import TestCase

from simple_card.card import Card, CardError


def pre_loaded_card():
    card = Card('1')
    card.load(100)
    return card

class CardTests(TestCase):
    def testAuthoriseTooMuch(self):
        card = pre_loaded_card()
        with self.assertRaises(CardError):
            card.authorise(101)

    def testCaptureTooMuch(self):
        card = pre_loaded_card()
        transaction_id = card.authorise(10)
        with self.assertRaises(CardError):
            card.capture(transaction_id, 11)

    def testReverseTooMuch(self):
        card = pre_loaded_card()
        transaction_id = card.authorise(10)
        card.capture(transaction_id, 5)
        with self.assertRaises(CardError):
            card.reverse(transaction_id, 6)

    def testRefundTooMuch(self):
        card = pre_loaded_card()
        transaction_id = card.authorise(10)
        card.capture(transaction_id, 5)
        with self.assertRaises(CardError):
             card.refund(transaction_id, 6)

    def testAuthorise(self):
        card = pre_loaded_card()
        card.authorise(10)
        self.assertEqual(card.get_balance(), 100)
        self.assertEqual(card.get_amount_available(), 90)

    def testCapture(self):
        card = pre_loaded_card()
        transaction_id = card.authorise(10)

        card.capture(transaction_id, 5)
        self.assertEqual(card.get_balance(), 95)
        self.assertEqual(card.get_amount_available(), 90)

        card.capture(transaction_id, 5)
        self.assertEqual(card.get_balance(), 90)
        self.assertEqual(card.get_amount_available(), 90)

    def testReverse(self):
        card = pre_loaded_card()
        transaction_id = card.authorise(10)
        card.reverse(transaction_id, 5)
        self.assertEqual(card.get_balance(), 100)
        self.assertEqual(card.get_amount_available(), 95)

    def testRefund(self):
        card = pre_loaded_card()
        transaction_id = card.authorise(10)

        card.capture(transaction_id, 5)
        card.refund(transaction_id, 5)
        self.assertEqual(card.get_balance(), 100)
        self.assertEqual(card.get_amount_available(), 90)