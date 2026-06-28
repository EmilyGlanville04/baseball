from dataclasses import dataclass

@dataclass
class Teams:
    ID:int
    year:int
    teamCode: str
    divID:str
    div_ID:int
    teamRank:int
    games:int
    gamesHome:int
    wins:int
    losses:int
    divisionWinnner:int
    leagueWinner:int
    worldSeriesWinnner:int
    runs:int
    hits:int
    homeruns:int
    stolenBases:int
    hitsAllowed:int
    homerunsAllowed:int
    name:int
    park:int


    def __hash__(self):
        return hash(self.ID)

    def __str__(self):
        return self.teamCode

    def __eq__(self, other):
        return self.ID==other.ID