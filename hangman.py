import random
from words import words


def get_valid_word(words):
    word=random.choice(words)
    while '-' in word or ' ' in word:
        word=random.choice(words);
        
    return word.upper()
def hangman():
    num_hints=2
    word=get_valid_word(words)
    display=reveal_hints(word,num_hints)
    word_letters=set(word)
    alphabet=set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    used_letters=set(); #what user guessed
     
    lives=6
    #getting user input 
    while len(word_letters)>0 and lives>0:
        #letters used: 
        print('you have used these letters: ',''.join(used_letters))
    
        word_list=[letter if letter in used_letters else '-' for letter in word ]
        print('current word',''.join(word_list))
        
        user_letter =input("guess a letter: ").upper()
        if user_letter in alphabet-used_letters: 
            used_letters.add(user_letter)
            if user_letter in word_letters:
                word_letters.remove(user_letter)
            else:
                lives =lives-1
                print('letter is not in a word.')
                print(f"You have {lives} lives remaining.")
        elif user_letter in used_letters:
            print("you have already guessed this letter, try another one")
        
        else:
            print("invalid character,try again");   
    #gets here when the leb(word_letters)==0 or when lives==0 
    if lives == 0:
        print("you died ,sorry,the word was ",word)
    else:
        print('you have guessed the word: ',word,'!!!!')
    

def reveal_hints(words, num_hints):
    revealed = ['_' for _ in words]
    hint_indices = random.sample(range(len(words)), num_hints)
    for index in hint_indices:
        revealed[index] = words[index]
    return revealed

hangman()
