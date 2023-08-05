#from . import player_stats
import datanba.player_stats as datanba
name = "nba_player"
data = datanba.AllOfBasketball(["2018-19"])
data.gather()
data.get_player_json("players.json")
