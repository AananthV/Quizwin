import { Sortable } from '../libs/sortable.core.js'

import { BaseSocket } from './base.js'
import { empty_container, get_radio_choice, get_order_choice } from '../helpers.js'

class ParticipantSocket extends BaseSocket {
    constructor(room_id, user_id) {
        super(room_id, false)
        this.user_id = user_id
        
        this.question = undefined
        this.init_buzzer()
    }

    init_buzzer() {
        this.buzzer = {
            locked: false,
            buzzed: false
        }

        const buzzer = document.getElementById('buzzer')
        buzzer.addEventListener('click', (event) => {
            if (!this.buzzer.locked && !this.buzzer.buzzed) {
                this.send('buzz')
            }
        })

        const choice_submit_button = document.getElementById('choice-submit-button')
        choice_submit_button.addEventListener('click', (event) => {
            const checked = document.querySelector('input[name="choice-radio-input"]:checked')
            
            if (checked != null) {
                this.send('answer', {answer: checked.value})
            }
        })

        const order_sortable = document.getElementById('order-sortable')
        const sortable = Sortable.create(order_sortable)
        const order_submit_button = document.getElementById('order-submit-button')
        order_submit_button.addEventListener('click', (event) => {
            this.send('answer', {answer: sortable.toArray().join(',')})
        })
    }

    onOpen(event) {
        console.log('Connected')
        this.send('status')
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
            case 'buzzer.info':
                return this.on_buzzer(data.info)
            case 'quiz.question':
                return this.on_question(data.info)
        }
    }

    on_status(status) {
        this.on_question(status.question)
    }

    on_question(question) {
        this.question = question
        this.render()
    }

    on_buzzer(buzzer_info) {
        this.buzzer.locked = buzzer_info.locked        
        this.buzzer.buzzed = buzzer_info.buzzes.includes(this.user_id)
        this.render()
    }

    render() {
        hide_answering()
        if (typeof this.question === 'undefined') {
            return render_buzzer(this.buzzer)
        }
        switch (this.question.type) {
            case 'C':
                return render_mcq_choices(this.question.choices, this.buzzer)
            case 'O':
                return render_order_choices(this.question.choices, this.buzzer)
            default:
                return render_buzzer(this.buzzer)
        }
    }
}

const hide_answering = () => {
    document.getElementById('buzzer').classList.add('d-none')
    document.getElementById('order-container').classList.add('d-none')
    document.getElementById('choice-container').classList.add('d-none')
}

const render_buzzer = (buzzer_info) => {    
    const buzzer = document.getElementById('buzzer')
    buzzer.classList.remove('d-none')
    if (buzzer_info.locked) {
        buzzer.className = 'locked'
        buzzer.innerText = 'locked'
    } else if (buzzer_info.buzzed) {        
        buzzer.className = 'buzzed'
        buzzer.innerText = 'buzzed'
    } else {
        buzzer.className = 'unlocked'
        buzzer.innerText = 'buzz'
    }
}

const render_mcq_choices = (choices, buzzer_info) => {
    const choice_container = document.getElementById('choice-container')
    choice_container.classList.remove('d-none')

    const choice_list = document.getElementById('choices')
    empty_container(choice_list)

    for (let c = 1; c <= choices; c++) {
        choice_list.appendChild(get_radio_choice(c))        
    }

    if (buzzer_info.locked || buzzer_info.buzzed) {
        document.getElementById('choice-submit-button').disabled = true
    } else {
        document.getElementById('choice-submit-button').disabled = false
    }
}

const render_order_choices = (choices, buzzer_info) => {
    const order_container = document.getElementById('order-container')
    order_container.classList.remove('d-none')

    const order_sortable = document.getElementById('order-sortable')
    empty_container(order_sortable)

    for (let c = 1; c <= choices; c++) {
        order_sortable.appendChild(get_order_choice(c))
    }

    if (buzzer_info.locked || buzzer_info.buzzed) {
        document.getElementById('order-submit-button').disabled = true
    } else {
        document.getElementById('order-submit-button').disabled = false
    }
}

export { ParticipantSocket }