from __future__ import unicode_literals, absolute_import, division
import json_tricks as json
import redis
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from functools32 import wraps
from simple_card.card import Card


'''
Example api usage
curl 127.0.0.1:8000/api/create_card/    -d '{"card_number":1234}'
curl 127.0.0.1:8000/api/load/           -d '{"card_number": 1234, "amount":100}'

curl 127.0.0.1:8000/api/authorise/      -d '{"card_number": 1234, "transaction_id":2, "amount":20}'
curl 127.0.0.1:8000/api/capture/        -d '{"card_number": 1234, "transaction_id":2, "amount":20}'
curl 127.0.0.1:8000/api/refund/         -d '{"card_number": 1234, "transaction_id":2, "amount":20}'
curl 127.0.0.1:8000/api/reverse/        -d '{"card_number": 1234, "transaction_id":2, "amount":20}'
'''


def request(function):
    @wraps(function)
    @require_POST
    @csrf_exempt
    def wrapped_function(request):
        try:
            json_data = json.load(request)
            result = function(**json_data)
            if result is None:
                result = 'Success'
            return HttpResponse(json.dumps(result), content_type='application/json')
        except Exception, e:
            print
            return HttpResponse(json.dumps(unicode(e)), content_type='application/json', status=500)
    return wrapped_function


# Gets card, executes request then saves card
def card_request(function):
    @wraps(function)
    @request
    def wrapped_function(**kwargs):
        card = get_card(kwargs.pop('card_number'))
        result = function(card, **kwargs)
        save_card(card)
        return result
    return wrapped_function


cache = redis.StrictRedis(host='localhost')


def get_card(card_number):
    return Card(**json.loads(cache.get(card_number)))

def save_card(card):
    cache.set(card.number, json.dumps(vars(card)))

@request
def create_card(card_number):
    card = Card(card_number)
    save_card(card)
    return card_number

@card_request
def load(card, amount):
    return card.load(amount)

@card_request
def authorise(card, amount):
    return card.authorise(amount)

@card_request
def reverse(card, transaction_id, amount):
    return card.reverse(transaction_id, amount)

@card_request
def capture(card, transaction_id, amount):
    return card.capture(transaction_id, amount)

@card_request
def refund(card, transaction_id, amount):
    return card.refund(transaction_id, amount)

@card_request
def get_blocked_balance(card):
    return card.get_amount_blocked()

@card_request
def get_available(card):
    return card.get_amount_available()