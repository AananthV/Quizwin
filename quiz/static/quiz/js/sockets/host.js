import { BaseSocket } from './base.js'
import { render_slide, render_question_slides, render_choice_slides, render_answer_slide } from '../slides.js'
import { empty_container, insert_hr, get_th, get_tr, get_td, get_eval_buttons } from '../helpers.js'
import { render_round_questions, render_rounds_table } from '../rounds.js'

class HostSocket extends BaseSocket {
    constructor(room_id) {
        super(room_id, true)

        this.quiz = undefined
        this.round = undefined
        this.question = undefined
        this.participants = undefined
        this.init_buzzer()
        this.init_buttons()
    }

    init_buttons() {
        document.getElementById('next-round-button').addEventListener('click', () => {
            this.send('next_round')
        })
        document.getElementById('start-quiz-button').addEventListener('click', () => {
            this.send('start')
        })
        document.getElementById('end-quiz-button').addEventListener('click', () => {
            this.send('end')
        })
    }

    init_buzzer() {
        this.buzzer = undefined
        document.getElementById('buzzer-lock-button').addEventListener('click', () => {
            this.send('lock_buzzer')
        })
        document.getElementById('buzzer-unlock-button').addEventListener('click', () => {
            this.send('unlock_buzzer')
        })
        document.getElementById('buzzer-reset-button').addEventListener('click', () => {
            this.send('reset_buzzer')
        })
    }

    onOpen(event) {
        console.log('Connected')
        this.send('request_ping')
        setTimeout(() => {
            this.send('status')
        }, 1000)
    }

    onClose(event) {
        console.log('Disconnected')
    }

    onError(event) {
        console.log('Error: ', event)
    }

    onMessage(data) {
        console.log(data)
        switch (data.type) {
            case 'status':
                return this.on_status(data.status)
            case 'quiz.start':
                return this.on_start()
            case 'quiz.round':
                return this.on_round(data.info)
            case 'quiz.question':
                return this.on_question(data.info)
            case 'quiz.participants':                
                return this.on_participants(data.info)
            case 'buzzer.info':
                return this.on_buzzer(data.info)
        }
    }

    on_status(status) {
        this.on_quiz(status.quiz)
        this.on_round(status.round)
        this.on_question(status.question)
        this.on_participants(status.participants)
    }

    on_quiz(quiz) {
        this.quiz = quiz

        if (this.quiz.started) {
            document.getElementById('start-quiz-button').classList.add('d-none')
            if (this.quiz.ended) {
                document.getElementById('end-quiz-button').classList.add('d-none')
            } else {
                document.getElementById('end-quiz-button').classList.remove('d-none')
            }
        } else {
            document.getElementById('start-quiz-button').classList.remove('d-none')
        }

        render_quiz(quiz)
    }

    on_start() {
        document.getElementById('start-quiz-button').classList.add('d-none')
        document.getElementById('next-round-button').classList.remove('d-none')
        document.getElementById('end-quiz-button').classList.remove('d-none')
    }

    on_round(round) {
        this.round = round

        console.log(this.round.round_number, this.quiz.rounds.length);
        
        if (this.quiz.started && (this.round == undefined || this.round.round_number < this.quiz.rounds.length)) {
            document.getElementById('next-round-button').classList.remove('d-none')
        } else {
            document.getElementById('next-round-button').classList.add('d-none')
        }

        render_round(round, this.next_question.bind(this))
    }

    on_question(question) {
        this.question = question
        render_question(question)
    }

    on_participants(participants) {
        this.participants = participants
        render_participants(participants)
    }

    on_buzzer(buzzer) {
        this.buzzer = buzzer
        render_buzzer(buzzer, this.participants, this.score_question.bind(this))
    }

    score_question(user_id, correct) {
        this.send('score_question', {
            user_id: user_id,
            correct: correct
        })
    }

    next_question(question_id) {
        if (typeof question_id == 'undefined')
            this.send('next_question')
        else
            this.send('choose_question', {'question_id': question_id})
    }
}

const render_quiz = (quiz_info) => {
    const quiz_container = document.getElementById('quiz-info')
    empty_container(quiz_container)

    const title = document.createElement('h2')
    title.innerText = quiz_info.name
    quiz_container.appendChild(title)

    const password = document.createElement('h3')
    password.innerText = `Password: ${quiz_info.secret}`
    quiz_container.appendChild(password)

    insert_hr(quiz_container)

    quiz_container.appendChild(
        render_rounds_table(quiz_info.rounds)
    )


}

const render_round = (round_info, next_question) => {   
    const round_container = document.getElementById('round')
    empty_container(round_container)

    if (typeof round_info === 'undefined') {
        const not_started = document.createElement('h2')
        not_started.innerText = 'Round not started'
        round_container.appendChild(not_started)
        return
    }

    const title = document.createElement('h2')
    title.innerText = `Round${' ' + round_info.round_number}`
    round_container.appendChild(title)

    const name = document.createElement('h3')
    name.innerText = round_info.name
    round_container.appendChild(name)

    insert_hr(round_container)

    round_container.appendChild(
        render_round_questions(round_info, next_question)
    )
}

const render_question = (question_info) => {
    const question_container = document.getElementById('question')
    empty_container(question_container)

    if (typeof question_info === 'undefined') {
        const not_started = document.createElement('h2')
        not_started.innerText = 'Question not started'
        question_container.appendChild(not_started)
        return
    }

    const title = document.createElement('h2')
    title.innerText = `Question${' ' + question_info.question_number}`
    question_container.appendChild(title)

    const points = document.createElement('h3')
    points.innerText = question_info.points + ' Points'
    question_container.appendChild(points)

    insert_hr(question_container)

    question_container.appendChild(
        render_question_slides(question_info.slides)
    )

    insert_hr(question_container)

    if (question_info.type != 'N') {
        question_container.appendChild(
            render_choice_slides(question_info.choices, question_info.answer)
        )
    
        insert_hr(question_container)
    }

    question_container.appendChild(
        render_answer_slide(question_info.answer, question_info.type)
    )
}

const render_participants = (participants) => {
    const participants_container = document.getElementById('participants-tbody')
    empty_container(participants_container)

    Object.values(participants).forEach((p, i) => {
        const prow = get_tr()
        prow.appendChild(get_th(i + 1, 'row'))
        prow.appendChild(get_td(p.username))
        prow.appendChild(get_td(p.score))
        participants_container.appendChild(prow)
    })
}

const render_buzzer = (buzzer, participants, score_question) => {
    const buzzer_container = document.getElementById('buzzer-tbody')
    empty_container(buzzer_container)

    if (buzzer.locked) {
        document.getElementById('buzzer-lock-button').classList.add('d-none')
        document.getElementById('buzzer-unlock-button').classList.remove('d-none')
    } else {
        document.getElementById('buzzer-lock-button').classList.remove('d-none')
        document.getElementById('buzzer-unlock-button').classList.add('d-none')
    }

    buzzer.buzzes.forEach((b, i) => {
        const brow = get_tr()
        brow.appendChild(get_th(i + 1, 'row'))
        brow.appendChild(get_td(participants[b].username))
        if (Object.keys(buzzer.answers).length == 0) {
            // if (i == buzzer.current - 1) {
                brow.appendChild(get_td(get_eval_buttons(b, score_question)))
            // }
        } else {
            brow.appendChild(get_td(buzzer.answers[b]))
        }         
        buzzer_container.appendChild(brow)
    })
}

export { HostSocket }