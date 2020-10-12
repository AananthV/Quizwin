class BaseSocket {
    constructor(room_id, host=false) {
        this.room_id = room_id
        this.host = host

        this.protocol = (location.protocol == "https:") ? 'wss://' : 'ws://'        

        this.websocket = new WebSocket(
            this.protocol
            + window.location.host
            + '/ws'
            + (host ? '/host' : '/participate')
            + '/' + room_id + '/'
        )
        
        this.websocket.addEventListener('open', (event) => {
            this.onOpen(event)
        })

        this.websocket.addEventListener('close', (event) => {
            this.onClose(event)
        })

        this.websocket.addEventListener('error', (event) => {
            this.onError(event)
        })

        this.websocket.addEventListener('message', (event) => {
            const data = JSON.parse(event.data);
            this.onMessage(data)
        })
    }

    send(command, data) {        
        if (typeof data == 'undefined') {
            data = {}
        }
        
        data['command'] = command
        this.websocket.send(JSON.stringify(data))
    }

    onOpen(event) {
        console.log('Connected')
    }

    onClose(event) {
        console.log('Disconnected')
    }

    onError(event) {
        console.log('Error: ', event)
    }

    onMessage(data) {
        console.log(data)
    }
}

export { BaseSocket };