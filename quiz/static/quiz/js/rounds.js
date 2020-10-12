import { get_tr, get_th, get_td } from "./helpers.js"

const render_board_round = (categories, choose_question) => {
    const container = document.createElement('div')

    const num_categories = document.createElement('h3')
    num_categories.innerText = categories.length + ' Categories'
    container.appendChild(num_categories)

    const table = document.createElement('table')
    table.className = 'table table-hover'

    const tbody = document.createElement('tbody')
    categories.forEach(c => {
        const crow = get_tr()
        crow.appendChild(get_th(c.name, 'row'))
        c.questions.forEach(q => {            
            if (!q.done) {
                const qbtn = document.createElement('button')
                qbtn.className = 'btn btn-outline-info'
                qbtn.onclick = () => { choose_question(q.id); qbtn.classList.add('d-none');}
                qbtn.innerText = q.points
                crow.appendChild(get_td(qbtn))
            } else {
                crow.appendChild(get_td(''))
            }
        })
        tbody.appendChild(crow)
    });
    table.appendChild(tbody)

    container.appendChild(table)

    return container
}

const render_sequential_round = (questions, next_question) => {
    const container = document.createElement('div')

    const num_questions = document.createElement('h3')
    num_questions.innerText = questions.length + ' Questions'
    container.appendChild(num_questions)

    const next_button = document.createElement('button')
    next_button.className = 'btn btn-info'
    next_button.innerText = 'Next Question'
    next_button.onclick = () => { next_question() }
    container.appendChild(next_button)

    return container
}

const render_round_questions = (round_info, next_question) => {
    switch (round_info.type) {
        case 'S':
            return render_sequential_round(round_info.questions, next_question)
        case 'B':
            return render_board_round(round_info.categories, next_question)
        default:
            return ''
    }
}

const render_rounds_table = (rounds) => {
    const container = document.createElement('div')

    const title = document.createElement('h3')
    title.innerText = rounds.length + ' Rounds'
    container.appendChild(title)

    const table = document.createElement('table')
    table.className = 'table table-hover'

    const thead = document.createElement('thead')
    thead.className = 'thead-dark'

    const theadrow = get_tr()
    theadrow.appendChild(get_th('#', 'col'))
    theadrow.appendChild(get_th('Name', 'col'))
    thead.appendChild(theadrow)

    table.appendChild(thead)

    const tbody = document.createElement('tbody')
    rounds.forEach(r => {
        const rrow = get_tr()
        rrow.appendChild(get_th(r.round_number, 'row'))
        rrow.appendChild(get_td(r.name))
        tbody.appendChild(rrow)
    })
    table.appendChild(tbody)

    container.appendChild(table)
 
    return container       
}

export { render_round_questions, render_rounds_table }