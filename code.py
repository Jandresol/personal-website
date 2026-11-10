# jasmine.py

class Problem:
    def __init__(self, name):
        self.name = name

    def listen_to_communities(self):
        return "context"

    def respect_the_evidence(self):
        return "data"

    def map_the_institutions(self):
        return "constraints"


class System:
    def __init__(self, effective, useful, thoughtful):
        self.values = {
            "effective": effective,
            "useful": useful,
            "thoughtful": thoughtful,
        }

    def fit(self, context, data, constraints):
        return {
            "built_with": [context, data, constraints],
            "values": self.values,
        }


class Jasmine:
    focus = ["AI", "ML", "systems", "health", "education", "access"]
    operating_mode = "building"

    def build_with_intent(self, problem):
        context = problem.listen_to_communities()
        data = problem.respect_the_evidence()
        constraints = problem.map_the_institutions()

        return System(
            effective=True,
            useful=True,
            thoughtful=True,
        ).fit(context, data, constraints)


jasmine = Jasmine()
jasmine.build_with_intent(Problem("tools for complex, human systems"))


