import streamlit as st
import random
from words import words

# ---------------- UI COLORS ----------------
BG_COLOR = "#1A2D42"
CARD_COLOR = "#2E4156"
TEXT_PRIMARY = "#D4D8DD"
TEXT_SECONDARY = "#AAB7B7"

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Hangman", layout="centered")

st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: {BG_COLOR};
            color: {TEXT_PRIMARY};
        }}
        .word-box {{
            background-color: {CARD_COLOR};
            padding: 20px;
            border-radius: 12px;
            font-size: 32px;
            text-align: center;
            letter-spacing: 0.4rem;
            border: 2px solid {TEXT_SECONDARY};
        }}
        .word-box span {{
            display: inline-block;
            background-color: {CARD_COLOR};
            border-radius: 6px;
            padding: 10px 14px;
            margin: 0 4px;
            font-size: 32px;
            border: 2px solid {TEXT_SECONDARY};
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- GAME LOGIC ----------------
def get_valid_word(word_list):
    word = random.choice(word_list)
    while "-" in word or " " in word:
        word = random.choice(word_list)
    return word.upper()

def reveal_hints(word, num_hints=2):
    indices = random.sample(range(len(word)), num_hints)
    return {word[i] for i in indices}

def initialize_game():
    word = get_valid_word(words)
    hints = reveal_hints(word)

    st.session_state.word = word
    st.session_state.hints = hints
    st.session_state.used_letters = set(hints)
    st.session_state.word_letters = set(word) - set(hints)
    st.session_state.lives = 6
    st.session_state.game_over = False

# ---------------- INIT ----------------
if "word" not in st.session_state:
    initialize_game()

# ---------------- UI ----------------
st.markdown(
    "<h1 style='text-align:center;'>🎩 Hangman</h1>",
    unsafe_allow_html=True
)

# Display word
display_letters = st.session_state.used_letters
word_display = "".join(
    f"<span>{letter}</span>" if letter in display_letters else "<span>-</span>"
    for letter in st.session_state.word
)
st.markdown(f"<div class='word-box'>{word_display}</div>", unsafe_allow_html=True)

st.write(f"🧠 Used letters: {', '.join(sorted(display_letters))}")
st.write(f"❤ Lives left: {st.session_state.lives}")

# ---------------- INPUT ----------------
with st.form("guess_form"):
    guess = st.text_input("Guess a letter", max_chars=1).upper()
    submitted = st.form_submit_button("Submit")

if submitted and not st.session_state.game_over:
    if not guess or not guess.isalpha():
        st.warning("🚫 Enter a single alphabet letter.")
    elif guess in st.session_state.used_letters:
        st.warning("⚠ You already guessed that letter.")
    else:
        st.session_state.used_letters.add(guess)
        if guess in st.session_state.word_letters:
            st.session_state.word_letters.remove(guess)
            st.success("✅ Correct guess!")
        else:
            st.session_state.lives -= 1
            st.error("❌ Wrong guess.")

# ---------------- GAME END ----------------
if st.session_state.lives == 0:
    st.error(f"💀 You lost! The word was **{st.session_state.word}**")
    st.session_state.game_over = True

elif len(st.session_state.word_letters) == 0:
    st.success(f"🎉 You won! The word was **{st.session_state.word}**")
    st.balloons()
    st.session_state.game_over = True

# ---------------- RESET ----------------
if st.session_state.game_over:
    if st.button("🔄 Play Again"):
        st.session_state.clear()
        initialize_game()
