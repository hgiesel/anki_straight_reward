frm.log.clear()
for config in mw.col.decks.all_config():
  config.pop('straightReward', None)
  mw.col.decks.update_config(config)
  pp(config)
