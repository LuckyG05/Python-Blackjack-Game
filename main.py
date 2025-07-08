import random
#-Card class-
# This class represent a single playing card.
class Card:
    def __init__(self, suit, rank):
        #when a new card is created it needs a suit(type)
        self.suit = suit    #store the card's suit
        self.rank = rank     # store the card's rank and its value
    def __str__(self):
        #special method that defines what happens when we try to print a card object
        return f"{self.rank['rank']} of {self.suit}"   # for example k of hearts (where k is value of rank)

#-DECK CLASS-
#this class represent a full deck of 52 playing cards.
class Deck:
    def __init__(self):
        self.cards = [] # this list hold all the cards object in the deck
        suits = ["spades", "clubs", "hearts", "diamonds"]
        #Ace (A) is initially given a value of 11, which can be adjusted later if needed.
        ranks = [
            {"rank" : "A", "Value": 11}, 
            {"rank" : "2", "Value": 2}, 
            {"rank" : "3", "Value": 3}, 
            {"rank" : "4", "Value": 4}, 
            {"rank" : "5", "Value": 5}, 
            {"rank" : "6", "Value": 6}, 
            {"rank" : "7", "Value": 7}, 
            {"rank" : "8", "Value": 8}, 
            {"rank" : "9", "Value": 9}, 
            {"rank" : "10", "Value": 10}, 
            {"rank" : "J", "Value": 10}, # jack
            {"rank" : "Q", "Value": 10}, # queen
            {"rank" : "K", "Value": 10}, # king
        ]
        # create all 52 cards by combining each suit with each rank
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank)) # add all created cards into deck
    def shuffle(self):
        # randomly rearranges the cards in the deck
        if len(self.cards)>1: #only shuffle when there is more than 1 card
            random.shuffle(self.cards)
    
    def deal(self, number):
        #deals a specific no of cards from the top of the deck
        cards_dealt = []   #list to store the cards that are dealt.
        for x in range(number):
            if len(self.cards)>0:     # check if cards are left in the deck
                card = self.cards.pop()    # remove & get the last card from the deck
                cards_dealt.append(card)
        return cards_dealt
    
#-HAND CLASS-
class Hand:
    def __init__(self, dealer=False):
        self.cards = [] # list to store the card objects in the hand
        self.value = 0   #calculated total value in hand
        self.dealer = dealer   # # dealer=True indicates it's the dealer's hand

    def add_card(self, card_list):
        # adds one or more cards to the current hand
        self.cards.extend(card_list)

    def calculate_value(self):
        # Calculate total value of cards in hand, handling Ace's flexibility value.
        self.value = 0
        has_ace = False  # flag to check if there is ace
        for card in self.cards:
            card_value = int(card.rank["Value"])  ## Get the numerical value of the card
            self.value += card_value
            if card.rank["rank"] == "A":
                has_ace = True
        # Blackjack rule: If there's an Ace and the total value is over 21,
        # change the Ace's value from 11 to 1 (by subtracting 10)
        if has_ace and self.value > 21:
            self.value -= 10
    
    def get_value(self):
        # returns the current calculated value of hand
        self.calculate_value()  #always recalculate for up-to-date value
        return self.value
    
    def is_blackjack(self):
        # check if hand has the value of exactly 21
        return self.get_value() == 21
    
    def display(self, show_all_dealer_cards=False):
        # Determines if it's "Dealer's hand" or "Your hand"
        print(f'''{"Dealer's" if self.dealer else "Your"} hand: ''')
        for index , card in enumerate(self.cards):
            if index == 0 and self.dealer and not show_all_dealer_cards and not self.is_blackjack():
                print("hidden")   #Print "hidden" for the dealer's first card
            else:
                print(card)
        if not self.dealer:
            print("value: ", self.get_value())
        print()  #blank line

#-GAME CLASS_
# This class manage the overall flow and logic of the blackjackk game
class Game:
    def play(self):
        game_no = 0    #counter for current game being played
        games_to_play = 0   #Total no. of game user want to play
        
        while games_to_play <= 0:
            try:
                games_to_play = int(input("How many games do you want to play? "))
            except ValueError:
                print("You must enter a number!")
            except Exception as e:
                print(f"An unexpected error occured: {e}")

        # Main game loop:
        while game_no < games_to_play:
            game_no += 1  #increment game counter for each new game
            # create a new deck for each game and shuffle it
            deck = Deck()
            deck.shuffle()
            # Initialize new hand for player and dealer
            player_hand = Hand()
            dealer_hand = Hand(dealer=True)

            # Deal 2 initial cards to both player and dealer
            for i in range(2):
                #pop 1 card from deck & add it to P/D's hand
                player_hand.add_card(deck.deal(1))
                dealer_hand.add_card(deck.deal(1))
            
            print("\n" + "*"*30)
            print(f"Game {game_no} of {games_to_play}")
            print("*" * 30)
            player_hand.display()
            dealer_hand.display()
            
            # Check for immediate winners (e.g., initial Blackjack or busts)
            if self.check_winner(player_hand, dealer_hand):
                continue           #if a winner is found, skip to next game
            choice = ""            #to store player's choice
            # Loop until the player stands of busts(hand value>= 21).
            while player_hand.get_value() < 21 and choice not in ["s", "stand"]:
                choice = input("Please choose 'Hit' or 'stand' :").lower()
                print()

                while choice not in ["h", "s", "hit", "stand"]:
                    choice = input("please enter 'Hit' or 'Stand' (or H/S): ").lower()
                    print()

                if choice in ["hit", "h"]:
                    player_hand.add_card(deck.deal(1))    #deal one card to the player
                    player_hand.display()     #display updated player hand

            #check for winner again after player's turn
            if self.check_winner(player_hand, dealer_hand):
                continue
            player_hand_value = player_hand.get_value()
            dealer_hand_value = dealer_hand.get_value()

            #-Dealer's Turn-
            # Dealer must hit until their hand value is 17 or more
            while dealer_hand_value < 17:
                dealer_hand.add_card(deck.deal(1))      #deal one card to the dealer
                dealer_hand_value = dealer_hand.get_value()    #update dealer hand value

            # Display the dealer's hand with all cards revealed
            dealer_hand.display(show_all_dealer_cards=True)

            if self.check_winner(player_hand, dealer_hand):
                continue

            #-final result-
            print("Final Result")
            print("Your Hand: ", player_hand_value)
            print("Dealer' Hand: ", dealer_hand_value)
            self.check_winner(player_hand, dealer_hand, True)
        print("\n Thanks for playing!")

    def check_winner(self, player_hand, dealer_hand, game_over=False):
        #determine the winner of round based on blackjack rules
        if not  game_over:
            if player_hand.get_value() >21:
                print("You busted. Dealer wins! 😭")
                return True
            elif dealer_hand.get_value() >21:
                print("Dealer busted. You win! 😀")
                return True
            elif dealer_hand.is_blackjack() and player_hand.is_blackjack():
                print("Both players have Blackjack! It's a Tie! 😑")
                return True 
            elif player_hand.is_blackjack():
                print("You have Blackjack! You win! 😀")
                return True
            elif dealer_hand.is_blackjack():
                print("Dealer has Blackjack. Dealer wins! 😭")
                return True
        else:
            if player_hand.get_value()> dealer_hand.get_value():
                print("You win! 😀")
            elif player_hand.get_value() == dealer_hand.get_value():
                print("It's a Tie! 😑")
            else:
                print("Dealer wins. 😭")
            return True
        return False        ## No winner determined yet, game continues
    
#__main___
g = Game()
g.play()