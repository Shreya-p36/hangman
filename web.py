import streamlit as st
import random
from words import words  # This should be a list of words in a separate file

# UI Colors
BG_COLOR = "#1A2D42"
CARD_COLOR = "#2E4156"
TEXT_PRIMARY = "#D4D8DD"
TEXT_SECONDARY = "#AAB7B7"

# Page configuration and CSS styling
st.set_page_config(page_title="Hangman", layout="centered")
st.markdown(
    f"""
    <style>
        html, body {{
            font-size: 18px;
            margin: 0;
            padding: 0;
        }}
        .stApp {{
            background-color: {BG_COLOR};
            color: {TEXT_PRIMARY};
            animation: fadeIn 1s ease-in;
        }}
        .word-box {{
            background-color: {CARD_COLOR};
            padding: 20px 30px;
            border-radius: 12px;
            font-size: 32px;
            text-align: center;
            letter-spacing: 0.4rem;
            color: {TEXT_PRIMARY};
            border: 2px solid {TEXT_SECONDARY};
            animation: popIn 0.6s ease-out;
        }}
        input {{
            font-size: 18px !important;
        }}
        button {{
            background-color: {CARD_COLOR};
            color: {TEXT_PRIMARY};
            border-radius: 8px;
            padding: 10px 16px;
            transition: background-color 0.3s ease;
        }}
        button:hover {{
            background-color: #3D5772;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}

        @keyframes popIn {{
            0% {{ transform: scale(0.8); opacity: 0; }}
            100% {{ transform: scale(1); opacity: 1; }}
        }}
         .word-box span {{
            display: inline-block;
            background-color: {CARD_COLOR};
            border-radius: 6px;
            padding: 10px 14px;
            margin: 0 4px;
            font-size: 32px;
            color: {TEXT_PRIMARY};
            animation: flipIn 0.6s ease;
            border: 2px solid {TEXT_SECONDARY};
        }}

        @keyframes flipIn {{
            0% {{ transform: rotateX(-90deg); opacity: 0; }}
            50% {{ transform: rotateX(10deg); opacity: 0.7; }}
            100% {{ transform: rotateX(0deg); opacity: 1; }}
        }}
        @media (max-width: 768px) {{
            .main {{
            background-color: #f0f0f0;
            }}
  h1 {{
    font-size: 24px;
  }}
}}

    </style>
    """,
    unsafe_allow_html=True
)

# Function to initialize the game
def initialize_game():
    st.session_state.word = get_valid_word(words)
    st.session_state.revealed = reveal_hints(st.session_state.word, 2)
    st.session_state.word_letters = set(
        letter for letter in st.session_state.word if letter not in st.session_state.revealed
    )
    st.session_state.alphabet = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    st.session_state.used_letters = set()
    st.session_state.lives = 6
    st.session_state.game_over = False

# Get a valid word
def get_valid_word(word_list):
    word = random.choice(word_list)
    while '-' in word or ' ' in word:
        word = random.choice(word_list)
    return word.upper()

# Reveal a few letters as hints
def reveal_hints(word, num_hints):
    revealed = ['_' for _ in word]
    hint_indices = random.sample(range(len(word)), num_hints)
    for index in hint_indices:
        revealed[index] = word[index]
    return revealed

# Game initialization (runs only once)
if 'word' not in st.session_state:
    initialize_game()

# Game variables from session state
word = st.session_state.word
used_letters = st.session_state.used_letters
revealed = st.session_state.revealed

st.markdown(
    "<h1 style='text-align: center; color: #D4D8DD; font-size: 50px; margin-top:'>🎩 Hangman</h1>",
    unsafe_allow_html=True
)
display_letters = set(used_letters).union(set(revealed))
word_list = [
    letter if letter in display_letters else '-'
    for letter in word
]
flipped_word = ''.join(
    f"<span>{letter}</span>" if letter in display_letters else "<span>-</span>"
    for letter in word
)
st.markdown(f"<div class='word-box'>{flipped_word}</div>", unsafe_allow_html=True)

# Show game status
st.write(f"🧠 Used letters: {', '.join(sorted(used_letters))}")
st.write(f"❤ Lives left: {st.session_state.lives}")

# Take user input
with st.form("guess_form"):
    guess = st.text_input("Guess a letter").upper()
    submitted = st.form_submit_button("Submit")
if submitted and guess:
    if guess in st.session_state.alphabet and guess not in used_letters:
        used_letters.add(guess)

        if guess in st.session_state.word_letters:
            st.session_state.word_letters.remove(guess)
            st.success("✅ Good guess!")
        else:
            st.session_state.lives -= 1
            st.error("❌ Letter not in word.")
    elif guess in used_letters:
        st.warning("⚠ You already guessed that letter.")
    else:
        st.warning("🚫 Invalid character, try again.")

# Game over condition
if st.session_state.lives == 0:
    st.error(f"💀 You died! The word was {word}!")
    st.session_state.game_over = True
    if st.button("Try Again"):
        st.session_state.clear()
        initialize_game()  # Reinitialize the game

# Game win condition
elif len(st.session_state.word_letters) == 0:
    st.success(f"🎉 You won! The word was {word}!")
    st.balloons() 
    st.session_state.game_over = True
    if st.button("Play Again"):
        st.session_state.clear()
        initialize_game()  # Reinitialize the game
