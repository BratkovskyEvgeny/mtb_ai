from pathlib import Path
from random import randrange

import streamlit as st
from src.styles.menu_styles import FOOTER_STYLES, HEADER_STYLES
from src.utils.conversation import get_user_input, show_chat_buttons, show_conversation
from src.utils.footer import show_donates, show_info
from src.utils.helpers import get_files_in_dir, get_random_img
from src.utils.lang import en, ru
from streamlit_option_menu import option_menu
from PIL import Image
import base64
from io import BytesIO
import requests

# --- PATH SETTINGS ---
current_dir: Path = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file: Path = current_dir / "src/styles/.css"
assets_dir: Path = current_dir / "assets"
icons_dir: Path = assets_dir / "icons"
img_dir: Path = assets_dir / "img"
tg_svg: Path = icons_dir / "tg.svg"

# --- GENERAL SETTINGS ---
LANG_RU: str = "Ru"
AI_MODEL_OPTIONS: list[str] = [
    "gpt-4-1106-preview",
    "gpt-4-vision-preview",
    "gpt-4",
    "gpt-4-32k",
    "gpt-3.5-turbo-1106",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-16k",
]

with open(css_file) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

with st.sidebar:
    selected_lang = option_menu(
                    menu_title=None,
                    options=[LANG_RU, ],#LANG_EN, 
                    icons=["globe2", "translate"],
                    menu_icon="cast",
                    default_index=0,
                    orientation=None,
                    styles=HEADER_STYLES)

    selected_model = st.selectbox(label="Выберите модель", options=AI_MODEL_OPTIONS, index=2)  # gpt-4 by default

# Storing The Context
if "locale" not in st.session_state:
    st.session_state.locale = en
if "generated" not in st.session_state:
    st.session_state.generated = []
if "past" not in st.session_state:
    st.session_state.past = []
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_text" not in st.session_state:
    st.session_state.user_text = ""
if "input_kind" not in st.session_state:
    st.session_state.input_kind = st.session_state.locale.input_kind_1
if "seed" not in st.session_state:
    st.session_state.seed = randrange(10**3)  # noqa: S311
if "costs" not in st.session_state:
    st.session_state.costs = []
if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = []


def main() -> None:
    c1, c2 = st.columns(2)
    with c1, c2:
        st.session_state.input_kind = c2.radio(
            label=st.session_state.locale.input_kind,
            options=(st.session_state.locale.input_kind_1, st.session_state.locale.input_kind_2),
            horizontal=True,
        )
        role_kind = c1.radio(
            label=st.session_state.locale.radio_placeholder,
            options=(st.session_state.locale.radio_text1, st.session_state.locale.radio_text2),
            horizontal=True,
        )
        match role_kind:
            case st.session_state.locale.radio_text1:
                c2.selectbox(label=st.session_state.locale.select_placeholder2, key="role",
                             options=st.session_state.locale.ai_role_options)
            case st.session_state.locale.radio_text2:
                c2.text_input(label=st.session_state.locale.select_placeholder3, key="role")

    if st.session_state.user_text:
        show_conversation()
        st.session_state.user_text = ""
    get_user_input()
    show_chat_buttons()


def run_agi():
    match selected_lang:
        case "En":
            st.session_state.locale = en
        case "Ru":
            st.session_state.locale = ru
        case _:
            st.session_state.locale = en
    st.markdown(f"<h1 style='text-align: center;'>{st.session_state.locale.title}</h1>", unsafe_allow_html=True)
    selected_footer = option_menu(
        menu_title=None,
        options=[
            #st.session_state.locale.footer_option1,
            st.session_state.locale.footer_option0,
           # st.session_state.locale.footer_option2,
        ],
        icons=["chat-square-text"],  # https://icons.getbootstrap.com/#"info-circle", "chat-square-text", "piggy-bank"
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles=FOOTER_STYLES
    )
    match selected_footer

