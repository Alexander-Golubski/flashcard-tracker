from flask import request
from models import InsCard


def get_checkboxed():
    # Get checkbox'd cards
    sel_card_ids = request.form.getlist('sel_cards')
    # Create list of card objects
    sel_cards = []
    for card_id in sel_card_ids:
        sel_cards.append(InsCard.query.get(card_id))
    return sel_cards
