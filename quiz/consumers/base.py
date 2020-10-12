from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

class QuizConsumer(JsonWebsocketConsumer):

    def disconnect(self, close_code):
        '''
        Disconnect host from quiz room
        '''
        if (hasattr(self, 'quiz_group_name')):
            # Disconnect from quiz_group
            self.leave_room(broadcast=close_code is not None)

    # Helpers

    def transmit(self, target_channel, data):
        async_to_sync(self.channel_layer.send)(
            target_channel,
            data
        )

    def broadcast(self, data):
        async_to_sync(self.channel_layer.group_send)(
            self.quiz_group_name,
            data
        )

    # Dispatchers

    def join_room(self, room_id):
        self.quiz_group_name = f'quiz_{room_id}'

        # Notify other users that we're in baby
        self.broadcast({
            'type': 'room.join',
            'user_id': self.user.id,
            'username': self.user.username,
            'channel_name': self.channel_name
        })

        # Add to room group
        async_to_sync(self.channel_layer.group_add)(
            self.quiz_group_name,
            self.channel_name
        )

    def leave_room(self, broadcast=True):
        # Leave group
        async_to_sync(self.channel_layer.group_discard)(
            self.quiz_group_name,
            self.channel_name
        )

        if broadcast:
            # Notify others that we out
            self.broadcast({
                'type': 'room.leave',
                'user_id': self.user.id,
                'username': self.user.username
            })

    # Handler

    # Ping

    def ping_request(self, event):
        '''
        Called when a ping request is received
        '''
        pass

    def ping_ping(self, event):
        '''
        Called when a pind is received
        '''
        pass

    # Rooms

    def room_join(self, event):
        '''
        Called when a user joins a room
        '''
        pass

    def room_leave(self, event):
        '''
        Called when a user leaves a room
        '''
        pass

    def room_reject(self, event):
        self.close(code=1000)

    def room_accept(self, event):
        self.send_json({
            'type': 'room.accept',
            'user_id': event['user_id']
        })

    # Quiz

    def quiz_start(self, event):
        '''
        Called when quiz has started
        '''
        self.send_json({
            'type': 'quiz.start'
        })

    def quiz_end(self, event):
        '''
        Called when quiz has ended
        '''
        self.send_json({
            'type': 'quiz.end'
        })

    def quiz_round(self, event):
        '''
        Called when a new round starts
        '''
        pass

    def quiz_question(self, event):
        '''
        Called when a new question starts
        '''
        pass

    def quiz_answer(self, event):
        '''
        Called when a participant answers
        '''
        pass


    # Buzzer

    def buzzer_info(self, event):
        '''
        Triggered when host sends buzzer update
        '''
        self.send_json(event)


    def buzzer_buzz(self, event):
        '''
        Called when a participant buzzes
        '''
        pass

    def buzzer_lock(self, event):
        '''
        Called when host locks buzzer
        '''
        pass

    def buzzer_unlock(self, event):
        '''
        Called when host unlocks buzzer
        '''
        pass