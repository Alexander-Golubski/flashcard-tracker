# Third Party Imports
from flask import request
import random
# Local imports
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


def shuffle_cards(card_list):
    """ Shuffle cards, but put the first card on the bottom """
    random.shuffle(card_list)
    first_card = card_list[0]
    card_list.append(first_card)
    card_list.remove(card_list[0])
    card = card_list[0]

    return card


def random_card(card_list, cohort, user_id):
    """ get a random card id from a list of cards """
    card_id_list = []
    for card in card_list:
        card_id_list.append(card.id)
    start_card_index = random.randrange(1, cohort.total_cards(user_id))
    start_card_id = card_id_list[start_card_index]
    return start_card_id
