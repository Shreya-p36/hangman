import random
from words import words

def get_valid_word(word_list):
    word = random.choice(word_list)
    while '-' in word or ' ' in word:
        word = random.choice(word_list)
    return word.upper()

def reveal_hints(word, num_hints):
    hint_indices = random.sample(range(len(word)), num_hints)
    return set(word[i] for i in hint_indices)

def hangman():
    lives = 6
    num_hints = 2

    word = get_valid_word(words)
    hint_letters = reveal_hints(word, num_hints)

    used_letters = set(hint_letters)
    word_letters = set(word) - used_letters
    alphabet = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    print("🎩 Welcome to Hangman!")
    print("Hint letters:", " ".join(hint_letters))

    while len(word_letters) > 0 and lives > 0:
        print("\nUsed letters:", " ".join(sorted(used_letters)))
        display = [letter if letter in used_letters else '-' for letter in word]
        print("Current word:", " ".join(display))
        print(f"Lives left: {lives}")

        user_letter = input("Guess a letter: ").upper()

        if len(user_letter) != 1 or not user_letter.isalpha():
            print("❌ Please enter a single alphabet letter.")
            continue

        if user_letter in used_letters:
            print("⚠ You already guessed that letter.")
            continue

        used_letters.add(user_letter)

        if user_letter in word_letters:
            word_letters.remove(user_letter)
            print("✅ Correct!")
        else:
            lives -= 1
            print("❌ Wrong guess!")

    if lives == 0:
        print(f"\n💀 You lost! The word was: {word}")
    else:
        print(f"\n🎉 You won! The word was: {word}")

if __name__ == "__main__":
    hangman()
