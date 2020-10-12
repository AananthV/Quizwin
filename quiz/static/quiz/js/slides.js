import { is_element, get_tr, get_th, get_td } from './helpers.js'

const render_slide = (slide_info) => {
    switch (slide_info.type) {
        case 'T':
            return render_text(slide_info.text)
        case 'I':
            return render_image(slide_info.image)
        case 'A':
            return render_video(slide_info.audio)
        case 'V':
            return render_video(slide_info.video) 
        default:
            return ''
    }
}

const render_text = (text) => {
    const t = document.createElement('p')
    t.innerText = text
    return t
}

const render_image = (url) => {
    const i = document.createElement('img')
    i.className = 'img-thumbnail'
    i.src = url
    i.width = 200
    i.height = 200
    return i
}

const render_video = (url) => {
    const v = document.createElement('video')
    v.controls = true
    v.height = 200

    const s  = document.createElement('source')
    s.src = url
    v.appendChild(s)

    return v
}

const render_question_slides = (question_slides) => {
    const container = document.createElement('div')

    const title = document.createElement('h3')
    title.innerText = 'Slides'
    container.appendChild(title)

    const table = document.createElement('table')
    table.className = 'table table-hover'

    const thead = document.createElement('thead')
    thead.className = 'thead-dark'

    const theadrow = get_tr()
    theadrow.appendChild(get_th('#', 'col'))
    theadrow.appendChild(get_th('Info', 'col'))
    thead.appendChild(theadrow)

    table.appendChild(thead)

    const tbody = document.createElement('tbody')
    question_slides.forEach(qs => {
        const qsrow = get_tr()
        qsrow.appendChild(get_th(qs.slide_number, 'row'))
        qsrow.appendChild(get_td(render_slide(qs.slide)))
        tbody.appendChild(qsrow)
    })
    table.appendChild(tbody)

    container.appendChild(table)

    return container    
}

const render_choice_slides = (choices, answer=0) => {
    const container = document.createElement('div')

    const title = document.createElement('h3')
    title.innerText = 'Choices'
    container.appendChild(title)

    const table = document.createElement('table')
    table.className = 'table table-hover'

    const thead = document.createElement('thead')
    thead.className = 'thead-dark'

    const theadrow = get_tr()
    theadrow.appendChild(get_th('#', 'col'))
    theadrow.appendChild(get_th('Info', 'col'))
    thead.appendChild(theadrow)

    table.appendChild(thead)

    const tbody = document.createElement('tbody')
    choices.forEach(c => {
        let c_class = '';
        if (c.choice_number == answer) 
            c_class = 'table-success'

        const crow = get_tr(c_class)
        crow.appendChild(get_th(c.choice_number, 'row'))
        crow.appendChild(get_td(render_slide(c.slide)))
        tbody.appendChild(crow)
    })
    table.appendChild(tbody)

    container.appendChild(table)
 
    return container    
}

const render_answer_slide = (answer, question_type) => {
    const container = document.createElement('div')

    const title = document.createElement('h3')
    title.innerText = 'Answer'
    container.appendChild(title)

    if (question_type == 'N') {
        container.appendChild(render_slide(answer.slide))
    } else {
        container.appendChild(render_text(answer))
    }

    return container
}

export { render_slide, render_question_slides, render_choice_slides, render_answer_slide }