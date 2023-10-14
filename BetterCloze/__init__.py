# import the main window object (mw) from aqt
from aqt import mw

# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect

# import all of the Qt GUI library
from aqt.qt import *
from aqt import gui_hooks
from anki.cards import Card
import random
import re


def installed_successfully() -> None:
    # show a message box
    showInfo(
        "BetterCloze is successfully installed!\n In order to use BetterCloze correctly, create two clones of "
        'the Cloze note type with names "Process" and "Properties" respectively.'
    )


# create a new menu item, "test"
action = QAction("BetterCloze", mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, installed_successfully)
# and add it to the tools menu
mw.form.menuTools.addAction(action)


def multi_replace(rep: dict, text: str) -> str:
    # use these three lines to do the replacement
    rep = dict((re.escape(k), v) for k, v in rep.items())
    # Python 3 renamed dict.iteritems to dict.items so use rep.items() for latest versions
    pattern = re.compile("|".join(rep.keys()))
    return pattern.sub(lambda m: rep[re.escape(m.group(0))], text)


def properties_cards(text: str, card: Card, kind: str) -> str:
    if card.note_type()["name"] == "Properties":
        lines = re.findall(r"<span.*?>.*?</span>", text)
        to_randomise = []
        for line in lines:
            if 'class="cloze' in line:
                to_randomise.append(line)
        before = [line for line in to_randomise]
        random.shuffle(to_randomise)

        return multi_replace(dict(zip(before, to_randomise)), text)
    return text


def get_current_answer_index(lines):
    for i, line in enumerate(lines):
        if 'class="cloze"' in line:
            return i


def process_cards(text: str, card: Card, kind: str) -> str:
    if card.note_type()["name"] == "Process":
        lines = re.findall(r"<span.*?>.*?</span>", text)
        current_answer = get_current_answer_index(lines)
        if current_answer < len(lines) - 1:
            return multi_replace(
                {line: "" for line in lines[current_answer + 1 :]}, text
            )
    return text


gui_hooks.card_will_show.append(properties_cards)
gui_hooks.card_will_show.append(process_cards)
