import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime, time, pytz, math, random
from OSRSBytes import Hiscores as HS, Items as IT, Utilities as UT

# look into HiscoresCaching module to reduce diff time

# ---- RENAME STREAMLIT VARIABLES ----
SS = st.session_state

# ---- CONFIG ----
st.set_page_config(
    page_title="Matchmaker Stats",
    page_icon="assets/icons/ContinuumXRLogo.jpg",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://www.example.com/help",
        "Report a Bug": "https://www.example.com/bug_report",
        "About": None,  # Removes the "About" menu item
    },
)

# ---- GLOBAL VARIABLES ----
USERNAME = "Conipherus"
ITEMS = IT()

# ---- GLOBAL REFRESHES ----
ITEM_UPDATE_SLEEP = 30
PROGRESS = 0
PROGRESS_INCREMENT = 0.03
PROGRESS_PLACEHOLDER = st.empty()
PROGRESS_BAR = PROGRESS_PLACEHOLDER.progress(PROGRESS)

# ---- GLOBAL LISTS ----
LOADING_STRINGS = [
    "Trimmin armor...",
    "Cuttin Yews...",
    "Buyin Gf...",
    "Sellin Trout...",
    "Buyin gp...",
]


def main():
    print("# ---- MAIN() ---- ")
    set_banner()
    # set_header()
    set_sidebar()
    check_statefulness()

    if SS.fresh_query_p1:
        print(f"Query marked as FRESH, running...")
        ninety_nine_query()

    # apply_filters()
    # apply_exclusions()
    # set_section_metrics()
    # set_section_plots()
    # set_section_dataframes()
    remove_progress_bar()


def auto_increase_progress_bar():
    global PROGRESS_BAR
    global PROGRESS
    PROGRESS = PROGRESS + PROGRESS_INCREMENT
    if isinstance(PROGRESS_INCREMENT, float):
        if PROGRESS > 0.95:
            PROGRESS = 0.95
            PROGRESS_BAR.progress(PROGRESS, text=random.choice(LOADING_STRINGS))
    else:
        if PROGRESS > 95:
            PROGRESS = 95
            PROGRESS_BAR.progress(PROGRESS, text=random.choice(LOADING_STRINGS))
    PROGRESS_BAR.progress(PROGRESS, text=random.choice(LOADING_STRINGS))


def increase_progress_bar(increment):
    global PROGRESS_BAR
    global PROGRESS
    PROGRESS = PROGRESS + increment
    print(f"PROGRESS: {PROGRESS}")
    if PROGRESS > 100:
        PROGRESS = 100
        PROGRESS_BAR.progress(PROGRESS)
        print(f"ENDING PROGRESS BAR EARLY, ALTER INCREMENT")
        remove_progress_bar()
    PROGRESS_BAR.progress(PROGRESS)


def remove_progress_bar():
    print(f"remove_progress_bar()")
    global PROGRESS_BAR
    global PROGRESS
    global PROGRESS_PLACEHOLDER
    PROGRESS = 100
    PROGRESS_BAR.progress(PROGRESS)
    time.sleep(0.5)
    PROGRESS_PLACEHOLDER.empty()


def track_progress(func):
    def wrapper(*args, **kwargs):
        auto_increase_progress_bar()
        result = func(*args, **kwargs)
        auto_increase_progress_bar()
        return result

    return wrapper


# ---- BANNER ----
@track_progress
def set_banner():
    print("set_banner()")
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.image("assets/images/banner.png", use_column_width=True)


# ---- HEADER ----
@track_progress
def set_header():
    print("set_header()")


# ---- SIDEBAR ----
@track_progress
def set_sidebar():
    st.sidebar.header("Page Filters:")


@track_progress
def check_statefulness():
    if "init_session_globals_p1" not in SS:
        SS.init_session_globals_p1 = True
    if SS.init_session_globals_p1:
        init_session_globals_p1()


# ---- APPLY EXCLUSIONS ----
@track_progress
def apply_exclusions():
    print("apply_exclusions()")


# ---- APPLY FILTERS ----
@track_progress
def apply_filters():
    print("apply_filters()")


# ---- SESSION GLOBALS ----
@track_progress
def init_session_globals_p1():
    print("init_session_globals_p1()")
    if "fresh_query_p1" not in SS:
        SS.fresh_query_p1 = True
    SS.init_session_globals_p1 = False


# ---- DATAFRAMES ----
@track_progress
def set_section_dataframes():
    print("set_dataframes()")


# ---- METRIC DELTA COLOR ----
@track_progress
def get_delta_color(delta, invert=False):
    if delta == 0:
        delta_color = "off"
    elif invert:
        delta_color = "inverse"
    else:
        delta_color = "normal"
    return delta_color


# ---- METRICS ----
@track_progress
def set_section_metrics():
    st.header("CCU Metrics", divider="blue")


# ---- PLOTS ----
@track_progress
def set_section_plots():
    print(f"set_section_plots()")


# ---- QUERIES ----
@track_progress
def ninety_nine_query():
    print(f"ninety_nine_query()")
    SS.fresh_query_p1 = False
    player = HS(USERNAME)
    attack_lvl = player.skill("attack", "level")
    print(f"Attack Level: {attack_lvl}")
    print("Is Members:", ITEMS.isMembers("rune dagger"))
    print("Item ID:", ITEMS.getItemID("rune dagger"))

    print("Sell Average:", ITEMS.getSellAverage("rune dagger"))
    print("Sell Quantity:", ITEMS.getSellQuantity("rune dagger"))

    print("Buy Average:", ITEMS.getBuyAverage("rune dagger"))
    print("Buy Quantity:", ITEMS.getBuyQuantity("rune dagger"))

    print("Shop Price:", ITEMS.getShopPrice("rune dagger"))
    print("High Alch Value:", ITEMS.getHighAlchValue("rune dagger"))
    print("Low Alch Value:", ITEMS.getLowAlchValue("rune dagger"))

    # Update all of the item info after some time has passed\
    time.sleep(ITEM_UPDATE_SLEEP)
    # cache this/player/item queries for prod
    # Look into api for passing in smaller cache times, aka I'll need to extend the Hiscores class
    # https://oldschool.runescape.wiki/w/RuneScape:Real-time_Prices
    # -- /5m /1h /timeseries
    # https://runescape.wiki/w/Application_programming_interface
    # -- hiscore_oldschool/index_lite.ws?player
    # https://runescape.wiki/api.php
    ITEMS.update()

    # Up-to-date info
    print("UPDATED Sell Average:", ITEMS.getSellAverage("rune dagger"))


if __name__ == "__main__":
    main()
