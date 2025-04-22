import streamlit as st
import csv
import random
import math

# Load data
characters = []
with open("Celebbs.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        char = {
            "name": row["Name"],
            "is_actor": 1 if "Actor" in row["Profession"] or "Actress" in row["Profession"] else 0,
            "is_singer": 1 if "Singer" in row["Profession"] or "Songwriter" in row["Profession"] else 0,
            "is_politician": 1 if "Politician" in row["Profession"] else 0,
            "is_entrepreneur": 1 if "Entrepreneur" in row["Profession"] else 0,
            "is_athlete": 1 if "Player" in row["Profession"] or "Athlete" in row["Profession"] else 0,
            "is_male": 1 if row["Gender"] == "Male" else 0,
            "under_30": 1 if int(row["Age"]) < 30 else 0,
            "over_50": 1 if int(row["Age"]) > 50 else 0,
            "is_alive": 1 if row["Status"] == "Alive" else 0,
            "is_american": 1 if row["Nationality"] == "American" else 0,
            "is_indian": 1 if row["Nationality"] == "Indian" else 0,
            "is_punjabi": 1 if row["Birth_State"] == "Punjab" else 0,
            "is_marathi": 1 if row["Birth_State"] == "Maharashtra" else 0
        }
        characters.append(char)

# Define questions
questions = {
    "Q1": {"text": "Is your character an actor or actress?", "key": "is_actor"},
    "Q2": {"text": "Is your character a singer or songwriter?", "key": "is_singer"},
    "Q3": {"text": "Is your character a politician?", "key": "is_politician"},
    "Q4": {"text": "Is your character an entrepreneur?", "key": "is_entrepreneur"},
    "Q5": {"text": "Is your character an athlete?", "key": "is_athlete"},
    "Q6": {"text": "Is your character male?", "key": "is_male"},
    "Q7": {"text": "Is your character under 30 years old?", "key": "under_30"},
    "Q8": {"text": "Is your character over 50 years old?", "key": "over_50"},
    "Q9": {"text": "Is your character alive?", "key": "is_alive"},
    "Q10": {"text": "Is your character American?", "key": "is_american"},
    "Q11": {"text": "Is your character Indian?", "key": "is_indian"},
    "Q12": {"text": "Are you thinking of a Punjabi Character?", "key": "is_punjabi"},
    "Q13": {"text": "May be your character belongs to Maharashtra, right?", "key": "is_marathi"}
}

# Streamlit app
st.title("Lets Play - Guess Who!")

# Initialize session state
if "game_state" not in st.session_state:
    st.session_state.game_state = {
        "asked": [],
        "answers": [],
        "possibilities": characters.copy(),
        "guess_made": False
    }

def calculate_entropy(possibilities):
    if not possibilities:
        return 0
    total = len(possibilities)
    return -sum((count / total) * math.log2(count / total) for count in [len(possibilities)] if count > 0)

def information_gain(possibilities, question_key):
    total = len(possibilities)
    if total <= 1:
        return 0
    yes_count = sum(1 for c in possibilities if c[question_key] == 1)
    no_count = total - yes_count
    if yes_count == 0 or no_count == 0:
        return 0
    yes_entropy = calculate_entropy([c for c in possibilities if c[question_key] == 1])
    no_entropy = calculate_entropy([c for c in possibilities if c[question_key] == 0])
    current_entropy = calculate_entropy(possibilities)
    return current_entropy - (yes_count / total * yes_entropy + no_count / total * no_entropy)

# Game logic
if not st.session_state.game_state["guess_made"]:
    remaining_questions = [q for q in questions.keys() if q not in st.session_state.game_state["asked"]]
    
    if not remaining_questions or len(st.session_state.game_state["possibilities"]) == 0:
        if st.session_state.game_state["possibilities"]:
            guess = st.session_state.game_state["possibilities"][0]["name"]
            st.success(f"My guess: {guess}!")
            if len(st.session_state.game_state["possibilities"]) > 1:
                st.write(f"Debug: Multiple possibilities: {[c['name'] for c in st.session_state.game_state['possibilities']]}")
        else:
            st.error("I give up! No possibilities left.")
        st.session_state.game_state["guess_made"] = True
    else:
        # Pick best question
        best_question_id = max(
            remaining_questions,
            key=lambda q: information_gain(st.session_state.game_state["possibilities"], questions[q]["key"]),
            default=remaining_questions[0]
        )
        question_text = questions[best_question_id]["text"]
        trait_key = questions[best_question_id]["key"]

        st.write(f"Remaining possibilities: {len(st.session_state.game_state['possibilities'])}")
        st.write(question_text)

        # Buttons for Yes/No
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Yes"):
                st.session_state.game_state["asked"].append(best_question_id)
                st.session_state.game_state["answers"].append(1)
                st.session_state.game_state["possibilities"] = [
                    c for c in st.session_state.game_state["possibilities"]
                    if c[trait_key] == 1
                ]
                if len(st.session_state.game_state["possibilities"]) == 1:
                    st.success(f"My guess: {st.session_state.game_state['possibilities'][0]['name']}!")
                    st.session_state.game_state["guess_made"] = True
                st.rerun()  # Rerun to refresh the page
        with col2:
            if st.button("No"):
                st.session_state.game_state["asked"].append(best_question_id)
                st.session_state.game_state["answers"].append(0)
                st.session_state.game_state["possibilities"] = [
                    c for c in st.session_state.game_state["possibilities"]
                    if c[trait_key] == 0
                ]
                if len(st.session_state.game_state["possibilities"]) == 1:
                    st.success(f"My guess: {st.session_state.game_state['possibilities'][0]['name']}!")
                    st.session_state.game_state["guess_made"] = True
                st.rerun()

# Reset button
if st.session_state.game_state["guess_made"]:
    if st.button("Play Again"):
        st.session_state.game_state = {
            "asked": [],
            "answers": [],
            "possibilities": characters.copy(),
            "guess_made": False
        }
        st.rerun()