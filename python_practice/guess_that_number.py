from typing import Final
import random

lower_limit: Final[int]= 0
upper_limit: Final[int]= 100
random_number: int = random.randint(lower_limit, upper_limit)
guess_limit = 3
guess_count = 0


def bot_message(msg: str) -> None:
    print(f"Bot: {msg}")

bot_message('Welcome to Guess that Number!')
bot_message(f'Guess a number between {lower_limit} and {upper_limit}. You have {guess_limit} guesses.')

while guess_count < guess_limit:
    user_guess = input('Your guess: ')
    try:
        user_guess_int = int(user_guess)
    except ValueError:
        bot_message('Please enter a valid integer.')
        continue

    guess_count += 1

    if user_guess_int < lower_limit or user_guess_int > upper_limit:
        bot_message(f'Your guess is out of bounds! Please guess between {lower_limit} and {upper_limit}.')
    elif user_guess_int < random_number:
        bot_message('Too low!')
    elif user_guess_int > random_number:
        bot_message('Too high!')
    else: 
        user_guess_int == random_number
        bot_message(f'Congratulations! You guessed the number {random_number} correctly!')

    if guess_count == guess_limit:
        bot_message(f'😢 You used all {guess_limit} guesses. The number was {random_number}. Try again!')
        break
