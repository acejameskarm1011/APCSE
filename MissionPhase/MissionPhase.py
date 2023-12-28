class MissionPhase:
    weather = "BAD"
    def __init__(self, Phase) -> None:
        self.Phase = Phase
    @classmethod
    def changeweather(cls, text):
        cls.weather = text


class subphase(MissionPhase):
    pass


CLIMB = MissionPhase('CLIMB')
climb = subphase("climb")

print(climb.weather)
CLIMB.changeweather("Good")
print(climb.weather)