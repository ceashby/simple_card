from __future__ import unicode_literals, absolute_import, division
from django.shortcuts import render
from simple_card.api_views import get_card


def transactions(request):
    card_number = request.GET.get('card_number')
    try:
        card = get_card(card_number)
    except TypeError:
        return render(request, 'invalid_card.html')

    return render(request, 'transactions.html', {
        'transactions': [t for t in card.transactions if t['captured_amount']],
        'available': card.get_amount_available(),
        'balance': card.get_balance(),
        'card_number': card_number
    })

def home(request):
    return render(request, 'home.html')

