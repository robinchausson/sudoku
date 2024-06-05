import json
import os

class Scoreboard:
    def __init__(self, filename="scores.json"):
        self.filename = filename
        self.scores = self.load_scores()

    def load_scores(self):
        if not os.path.exists(self.filename):
            self.create_empty_file()
            return []
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []

    def create_empty_file(self):
        with open(self.filename, "w") as file:
            json.dump([], file)

    def save_scores(self):
        with open(self.filename, "w") as file:
            json.dump(self.scores, file, indent=4)

    def add_score(self, name, score, level, time):
        self.scores.append({"name": name, "score": score, 'level': level, 'time': time})
        self.save_scores()

    def get_scores(self):
        return sorted(self.scores, key=lambda x: x["score"], reverse=True)[:10]
    
    def get_best_score(self, difficulty):
        scores = self.get_scores()
        maxi=scores[0]['score']
        for score in scores:
            if score['level'] == difficulty and score['score'] > maxi:
                maxi = score['score']
        return maxi
        
    