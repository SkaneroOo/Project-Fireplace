CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS Users (
    id TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    discriminator TEXT NOT NULL,
    avatar TEXT,
    joined DATETIME DEFAULT CURRENT_TIMESTAMP,
    mail TEXT NOT NULL,
    password TEXT NOT NULL
)
"""

CREATE_SERVER_TABLE = """
CREATE TABLE IF NOT EXISTS general (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT NOT NULL,
    message TEXT NOT NULL
)
"""

CREATE_MESSAGE = """
INSERT INTO {} (user, message) VALUES ("{}", "{}")
"""

FETCH_CHANNEL = """
SELECT * FROM {} LIMIT 50
"""

HTML = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            function appendMessage(data) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                console.log(data)
                var content = document.createTextNode(data.user + ": " + data.message)
                message.appendChild(content)
                messages.appendChild(message)
            }
            fetch("http://localhost:8000/fetch/global/general")
            .then(response => response.json())
            .then(data => data.forEach(appendMessage))
            var ws = new WebSocket("ws://localhost:8000/ws/global/general");
            ws.onmessage = function(event) {
                var data = JSON.parse(event.data)
                appendMessage(data.p)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""