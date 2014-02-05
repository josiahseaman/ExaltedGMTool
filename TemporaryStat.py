class RulesError(AssertionError):
    pass


class TemporaryStat():
    def __init__(self, name, permanent, tempLevel=None):
        self.name = name
        self.permanent = permanent
        self.temporary = self.permanent if tempLevel is None else tempLevel

    def __repr__(self):
        return self.name + ": " + str(self.temporary) + " of " + str(self.permanent)

    def __isub__(self, amount):  # operator -=
        if self.temporary < amount:
            raise RulesError("You don't have enough " + self.name + " to do that.")
        self.temporary = self.temporary - amount
        if self.permanent > 1:
            print(self.name, str(self.temporary), "remaining of", str(self.permanent))
        return self

    def __iadd__(self, amount):# operator +=
        self.temporary = min(self.temporary + amount, self.permanent)
        return self #TODO Add overflow check for Limit

    def __eq__(self, other):# operator ==
        try:
            return self.temporary == other.temporary
        except:
            return self.temporary == other

    def amountSpent(self):
        return self.permanent - self.temporary


class HealthLevel(TemporaryStat):
    #TODO: this will need to eventually have 3 states: bashing, lethal, aggravated.  Apply Damage Push down rules
    """Characters have a list of health levels.  Once they run to the end of the list they are at least incapacitated.
    Along side this is a list of associated wound penalties.  Also damage stacking."""

    def __init__(self, name, permanent, temp=None, penalties=[0,-1,-1,-2,-2,-4,-20]):
        TemporaryStat.__init__(self, name, permanent, temp)
        self.penalties = []
        self.penalties = penalties

    def __isub__(self, other):
        TemporaryStat.__isub__(self, other)
        if self.temporary <= 0:
            raise ValueError()
        return self

    def empty(self):
        self.temporary = 0

    def woundPenalty(self):
        if self.temporary == self.permanent: return 0  # undamaged state
        return self.penalties[self.permanent - self.temporary - 1]  # minus one because penalties[0] is for 1 damage

    def oxBody(self, purchases=1):
        for p in purchases:
            self.permanent += 3
            self.temporary += 3
            self.penalties.insert(self.penalties.index(-1), -1)
            self.penalties.insert(self.penalties.index(-2), -2)
            self.penalties.insert(self.penalties.index(-2), -2)