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


def set_learning(card_list):
    """ Set all cards in list to 'learning' (1) """
    for card in card_list:
        card.review = 1


def still_learning(card_list):
    """ Returns true if there is still a card set to 'learning' in list """
    for card in card_list:
        if card.review == 1:
            return True
    return False
