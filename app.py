import streamlit as st
import random
import string
from typing import List


def add_food_key_to_session(key):
    print("Running add_food_key_to_session()", key)
    food_input_keys: List = st.session_state["food_input_keys"]
    food_input_keys.append(key)
    st.session_state["food_input_keys"] = food_input_keys


def remove_food_input_key(key):
    print("Running remove_food_input_key()", key)
    food_input_keys: List = st.session_state["food_input_keys"]
    food_input_keys.remove(key)
    st.session_state["food_input_keys"] = food_input_keys


def food_input(key):
    print("Running food_input()", key)
    food = st.text_input("Favorite Food", key=key)
    if food:
        st.write(food)


@st.experimental_fragment()
def add_food_container(key):
    print("Running add_food_container()", key)
    container = st.empty()
    with container.expander("Food Details", expanded=True):
        food_input(key)
        remove_food_popover = st.popover("Remove this food?")
        is_remove_food = remove_food_popover.checkbox(
            "Confirm", key=f"remove-{key}")

        if is_remove_food:
            remove_food_input_key(key)
            container.empty()


def render_food_containers():
    print("Running render_food_containers()")
    food_input_keys: List = st.session_state["food_input_keys"]
    for key in food_input_keys:
        add_food_container(key)


@st.experimental_fragment()
def manage_food_button_and_containers():
    print("Running manage_food_button_and_containers()")
    if st.button("Add Favorite Food"):
        key = get_new_key()
        add_food_key_to_session("food-" + key)
    render_food_containers()
    print("Session State:", st.session_state, "\n")


def get_new_key(k=4):
    key = "".join(random.choices(
        string.ascii_lowercase + string.digits, k=k))
    return key


def run_full_script():
    print("Running run_full_script")
    if "script_run_counter" not in st.session_state:
        st.session_state["script_run_counter"] = 1
    else:
        st.session_state["script_run_counter"] += 1
    if "food_input_keys" not in st.session_state:
        st.session_state["food_input_keys"] = []

    stats_container = st.container()
    st.divider()

    if st.button("Reset Counter"):
        st.session_state["script_run_counter"] = 1
    if st.button("Reset form"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.session_state["script_run_counter"] = 1
        st.session_state["food_input_keys"] = []

    manage_food_button_and_containers()
    with stats_container:
        if st.session_state["script_run_counter"] > 1:
            st.title(":red[Full Script Run -- You Lose!]")
            print("\n", "Full Script Run -- You Lose!", "\n")
        st.write(
            f'#### Full Script Run Counter: {st.session_state["script_run_counter"]}')
        st.write(
            "Goal: allow users to dynamically add/edit/delete food inputs without a full script rerun.")
    st.divider()
    with st.expander("Session State", expanded=False):
        st.json(st.session_state)


run_full_script()
