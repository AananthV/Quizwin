export const is_element = (element) => {
    return element instanceof Element || element instanceof HTMLDocument;  
}

export const empty_container = (container) => {
    while(container.firstChild && container.removeChild(container.firstChild));
}

export const insert_hr = (container) => {
    const hr = document.createElement('hr')
    container.appendChild(hr)
}

export const get_tr = (className = '') => {
    const tr = document.createElement('tr')
    tr.className = className
    return tr
}

export const get_th = (content, scope = '') => {
    const th = document.createElement('th')
    th.scope = scope

    if (is_element(content))
        th.appendChild(content)
    else
        th.innerHTML = content

    return th
}

export const get_td = (content) => {
    const td = document.createElement('td')

    if (is_element(content))
        td.appendChild(content)
    else
        td.innerHTML = content

    return td
}

export const get_eval_buttons = (user_id, score_question) => {
    const container = document.createElement('div')

    const p = document.createElement('button')
    p.className = 'btn badge badge-success mr-2'
    p.innerText = '✓'

    const n = document.createElement('button')
    n.className = 'btn badge badge-danger'
    n.innerText = '✗'

    p.addEventListener('click', () => {
        score_question(user_id, true)
        p.remove()
        n.remove()
    })
    n.addEventListener('click', () => {
        score_question(user_id, false)
        p.remove()
        n.remove()
    })

    container.appendChild(p)
    container.appendChild(n)

    return container
}

export const get_radio_choice = (choice_number) => {
    const label = document.createElement('label')
    label.className = 'labl'

    const radio = document.createElement('input')
    radio.type = 'radio'
    radio.name = 'choice-radio-input'
    radio.value = choice_number
    label.appendChild(radio)

    const clickable = document.createElement('div')
    clickable.className = 'list-group-item border'
    clickable.innerText = String.fromCharCode(choice_number + 64)
    label.appendChild(clickable)

    return label
}

export const get_order_choice = (choice_number) => {
    const li = document.createElement('li')
    li.setAttribute('data-id', choice_number)
    li.className = 'list-group-item mb-2 border'
    li.innerText = String.fromCharCode(choice_number + 64)
    return li 
}