frm.log.clear()

from anki.decks import DeckManager

d = DeckManager(mw.col)

pp(d.all_config())
