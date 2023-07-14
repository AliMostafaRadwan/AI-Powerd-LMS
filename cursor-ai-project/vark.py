class VarkTest:
    def __init__(self, questions):
        self.questions = questions
        self.options = ["Visual", "Auditory", "Read/Write", "Kinesthetic"]
        self.results = {
            "a": "Visual",
            "b": "Auditory",
            "c": "Read/Write",
            "d": "Kinesthetic"
        }

    def calculate_results(self, answers):
        counts = {"a": 0, "b": 0, "c": 0, "d": 0, "Visual": 0, "Kinesthetic": 0, "Read/Write": 0}
        for answer in answers:
            if answer in counts:
                counts[answer] += 1
        max_count = max(counts.values())
        results = [self.results[key] for key, value in counts.items() if value == max_count and key in self.results]
        return "/".join(results)


