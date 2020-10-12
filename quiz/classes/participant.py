from quiz.models import User, Score

class Participants:
    def __init__(self, quiz_id):
        self.quiz_id = quiz_id
        self.participants = {}

    def info(self):
        return self.participants

    def get_user(self, user_id):
        return self.participants[user_id]

    def add_user(self, user_id):
        user = User.objects.get(pk=user_id)
        user_score, _ = Score.objects.get_or_create(quiz_id=self.quiz_id, user_id=user_id)
        
        self.participants[user.id] = {
            'username': user.username,
            'score': user_score.score,
        }

    def update_score(self, user_id):
        if user_id not in self.participants.keys():
            # Return Exception
            return
        user_score = Score.objects.get(quiz_id=self.quiz_id, user_id=user_id)
        
        self.participants[user_id]['score'] = user_score.score

    def remove_user(self, user_id):
        del self.participants[user_id]

    def exists(self, user_id):
        return user_id in self.participants.keys()