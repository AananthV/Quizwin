class Buzzer:
    def __init__(self):
        self.buzzes = []
        self.answers = {}
        self.current = 1
        self.locked = False

    def reset(self):
        self.buzzes.clear()
        self.answers.clear()
        self.current = 1
        self.locked = False  
    
    def state(self):
        return {
            'buzzes': self.buzzes,
            'answers': self.answers,
            'current': self.current,
            'locked': self.locked,
        }

    def buzz(self, user_id):
        if self.locked == True:
            return
        if user_id in self.buzzes:
            return

        self.buzzes.append(user_id)

    def answer(self, user_id, answer):
        if self.locked == True:
            return
        if user_id in self.buzzes:
            return
        
        self.buzzes.append(user_id)
        self.answers[user_id] = answer

    def buzzed(self, user_id):
        return user_id in self.buzzes

    def next_buzz(self):
        if self.current == len(self.buzzes) - 1:
            return
        self.current += 1
    
    def lock(self):
        self.locked = True
    
    def unlock(self):
        self.locked = False   


        