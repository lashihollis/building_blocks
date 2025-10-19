import pandas as pd
import random

# Load affirmations CSV
affirmation = pd.read_csv('affirmations.csv')

def main():
    print("🌟 Welcome to the Motivation App! 🌟")
    
    while True:
        # Print menu
        print("\nMenu:")
        print("1. Get quote")
        print("2. Exit App")
        
        # Get user input
        user_input = input("Choose a menu option: ")
        
        # Handle exit
        if user_input == "2":
            print("Have a beautiful day. Goodbye 👋")
            break
        
        # Handle getting a random quote
        elif user_input == "1":
            quote = random.choice(affirmation['quote'])
            print("\n✨ Your affirmation: ✨")
            print(quote)
        
        # Handle invalid input
        else:
            print("Please choose a valid option from the menu.")

# Run the app
if __name__ == "__main__":
    main()
