import random

# Card class
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = self.get_value()

    def get_value(self):
        values = {
            'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6,
            'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
            'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11
        }
        return values[self.rank]

    def __str__(self):
        return f"{self.rank} of {self.suit}"


# Deck class
class Deck:
    def __init__(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
                 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
        self.cards = [Card(s, r) for s in suits for r in ranks]
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()


# Hand class
class Hand:
    def __init__(self):
        self.cards = []
        self.total = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.total += card.value
        if card.rank == 'Ace':
            self.aces += 1
        self.adjust_for_ace()

    def adjust_for_ace(self):
        while self.total > 21 and self.aces:
            self.total -= 10
            self.aces -= 1

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)


# Game class
class BlackjackGame:
    def __init__(self):
        self.player_money = 1000  # Starting money

    def play_round(self):
        deck = Deck()
        player_hand = Hand()
        dealer_hand = Hand()

        print(f"\nYou have ${self.player_money}")
        while True:
            try:
                bet = int(input("Enter your bet amount: $"))
                if 0 < bet <= self.player_money:
                    break
                else:
                    print("Invalid bet amount.")
            except ValueError:
                print("Please enter a valid number.")

        # Initial deal
        for _ in range(2):
            player_hand.add_card(deck.deal_card())
            dealer_hand.add_card(deck.deal_card())

        # Show cards
        print("\nYour Hand:", player_hand, f"(Total: {player_hand.total})")
        print("Dealer shows:", dealer_hand.cards[1])

        # Player turn
        while player_hand.total < 21:
            move = input("Do you want to Hit or Stand? (h/s): ").lower()
            if move == 'h':
                player_hand.add_card(deck.deal_card())
                print("Your Hand:", player_hand, f"(Total: {player_hand.total})")
                if player_hand.total > 21:
                    print("You busted!")
                    self.player_money -= bet
                    return
            elif move == 's':
                break
            else:
                print("Invalid choice.")

        # Dealer turn
        print("\nDealer's Hand:", dealer_hand, f"(Total: {dealer_hand.total})")
        while dealer_hand.total < 17:
            dealer_hand.add_card(deck.deal_card())
            print("Dealer hits:", dealer_hand, f"(Total: {dealer_hand.total})")

        # Results
        player_total = player_hand.total
        dealer_total = dealer_hand.total

        if dealer_total > 21:
            print("Dealer busts! You win.")
            self.player_money += bet
        elif dealer_total > player_total:
            print("Dealer wins.")
            self.player_money -= bet
        elif dealer_total < player_total:
            print("You win!")
            self.player_money += bet
        else:
            print("It's a tie. Push.")

    def play_game(self):
        print("Welcome to Blackjack!")
        while self.player_money > 0:
            self.play_round()
            again = input("\nPlay another round? (y/n): ").lower()
            if again != 'y':
                break
        print(f"\nGame over. You leave with ${self.player_money}.")


# Run the game
if __name__ == "__main__":
    game = BlackjackGame()
    game.play_game()
