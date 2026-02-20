class GameInResponse:
    def __init__(self,app_id,playtime_forever,rtime_last_played,playtime_2weeks,playtime_disconnected):
        self.app_id = app_id
        self.playtime_forever = playtime_forever
        self.rtime_last_played = rtime_last_played
        self.playtime_2weeks = playtime_2weeks
        self.playtime_disconnected = playtime_disconnected
        self.achievements = []
        self.achieved_count = 0
        self.achievements_total = 0

    def set_achievements(self,achievements):
        self.achievements = achievements
        for achievement in self.achievements:
            if achievement["achieved"] == 1:
                self.achieved_count+=1

    def to_dict(self):
        return {"app_id":self.app_id,
                "playtime_forever":self.playtime_forever,
                "rtime_last_played":self.rtime_last_played,
                "playtime_2weeks":self.playtime_2weeks,
                "playtime_disconnected":self.playtime_disconnected,
                "achievements":self.achievements,
                "achieved_count":self.achieved_count,
        }

class GamesResponse:
    def __init__(self, response,timestamp):
        self.response = response
        data = (response.json())["response"]
        self.game_count =data["game_count"]
        self.games :list[GameInResponse] = []
        self.update_timestamp = timestamp
        for game in data["games"]:
            appid = game["appid"]
            playtime_forever = game["playtime_forever"]
            rtime_last_played = game["rtime_last_played"]
            playtime_disconnected = game["playtime_disconnected"]
            if "playtime_2weeks" in game:
                playtime_2weeks = game["playtime_2weeks"]
            else:
                playtime_2weeks = 0

            g = GameInResponse(appid,playtime_forever,rtime_last_played,playtime_2weeks,playtime_disconnected)

            self.games.append(g)

    def to_dict(self):
        return {"game_count":self.game_count,"games": [g.to_dict() for g in self.games],"update_timestamp":self.update_timestamp}