import tkinter as tk
from tkinter import messagebox
import random

class BlackjackGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Blackjack")

        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []

        self.create_ui()
        self.start_game()

    def create_ui(self):
        self.player_label = tk.Label(self.master, text="Player's Hand:")
        self.player_label.grid(row=0, column=0, columnspan=2, pady=5)

        self.dealer_label = tk.Label(self.master, text="Dealer's Hand:")
        self.dealer_label.grid(row=1, column=0, columnspan=2, pady=5)

        self.result_label = tk.Label(self.master, text="")
        self.result_label.grid(row=2, column=0, columnspan=2, pady=5)

        self.hit_button = tk.Button(self.master, text="Hit", command=self.hit)
        self.hit_button.grid(row=3, column=0, padx=5)

        self.stand_button = tk.Button(self.master, text="Stand", command=self.stand)
        self.stand_button.grid(row=3, column=1, padx=5)

        self.restart_button = tk.Button(self.master, text="Restart", command=self.restart_game)
        self.restart_button.grid(row=4, column=0, columnspan=2, pady=10)

    def create_deck(self):
        ranks = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        deck = [{'rank': rank, 'suit': suit} for rank in ranks for suit in suits]
        random.shuffle(deck)
        return deck

    def deal_card(self, hand):
        card = self.deck.pop()
        hand.append(card)
        return card

    def start_game(self):
        self.deck = self.create_deck()
        self.player_hand = [self.deal_card(self.player_hand), self.deal_card(self.player_hand)]
        self.dealer_hand = [self.deal_card(self.dealer_hand), self.deal_card(self.dealer_hand)]

        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)
        self.result_label.config(text="")

        self.update_ui()

    def hit(self):
        self.deal_card(self.player_hand)
        self.update_ui()

        if self.calculate_hand_value(self.player_hand) > 21:
            self.end_game("Bust! You lose.")

    def stand(self):
        while self.calculate_hand_value(self.dealer_hand) < 17:
            self.deal_card(self.dealer_hand)
            self.update_ui()

        player_score = self.calculate_hand_value(self.player_hand)
        dealer_score = self.calculate_hand_value(self.dealer_hand)

        if dealer_score > 21 or player_score > dealer_score:
            result = "You win!"
        elif player_score < dealer_score:
            result = "You lose."
        else:
            result = "It's a tie!"

        self.end_game(result)

    def restart_game(self):
        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)
        self.result_label.config(text="")
        self.start_game()

    def calculate_hand_value(self, hand):
        value = sum([self.get_card_value(card['rank']) for card in hand])
        num_aces = sum(1 for card in hand if card['rank'] == 'A')

        while value > 21 and num_aces:
            value -= 10
            num_aces -= 1

        return value

    def get_card_value(self, rank):
        if rank in ['J', 'Q', 'K']:
            return 10
        elif rank == 'A':
            return 11
        else:
            return int(rank)

    def update_ui(self):
        player_hand_text = ', '.join([f"{card['rank']} of {card['suit']}" for card in self.player_hand])
        dealer_hand_text = ', '.join([f"{card['rank']} of {card['suit']}" for card in self.dealer_hand])

        self.player_label.config(text=f"Player's Hand: {player_hand_text} (Value: {self.calculate_hand_value(self.player_hand)})")
        self.dealer_label.config(text=f"Dealer's Hand: {dealer_hand_text} (Value: {self.calculate_hand_value(self.dealer_hand)})")

    def end_game(self, message):
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.result_label.config(text=message)

if __name__ == "__main__":
    root = tk.Tk()
    game = BlackjackGame(root)
    root.mainloop()


