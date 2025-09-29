#  Import Flask and SocketIO
from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my-secret-key'

# Create SocketIO app (this adds WebSocket support to Flask)
socketio = SocketIO(app)

# Simple HTML page with JavaScript to test our WebSocket
HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>My First WebSocket App</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.0/socket.io.js"></script>
</head>
<body>
    <h1>WebSocket Test</h1>
    <div id="messages"></div>
    
    <input type="text" id="messageInput" placeholder="Type a message...">
    <button onclick="sendMessage()">Send</button>
    
    <script>
        // Connect to our WebSocket server
        const socket = io();
        
        // When we receive a message from the server
        socket.on('message_response', function(data) {
            const messages = document.getElementById('messages');
            messages.innerHTML += '<p><strong>Server says:</strong> ' + data.message + '</p>';
        });
        
        // Function to send a message
        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value;
            if (message) {
                // Send message to server
                socket.emit('send_message', {message: message});
                
                // Show what we sent
                const messages = document.getElementById('messages');
                messages.innerHTML += '<p><strong>You:</strong> ' + message + '</p>';
                
                input.value = '';  // Clear the input
            }
        }
        
        // Send message when Enter key is pressed
        document.getElementById('messageInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>
'''

# Regular route to serve our HTML page
@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

# WebSocket event handler
# This runs when someone sends a 'send_message' event
@socketio.on('send_message')
def handle_message(data):
    print(f"Received message: {data['message']}")
    
    # Send a response back to the client
    emit('message_response', {
        'message': f"I got your message: '{data['message']}'"
    })

# WebSocket event for when someone connects
@socketio.on('connect')
def handle_connect():
    print('Someone connected to the WebSocket!')
    emit('message_response', {'message': 'Welcome! You are connected!'})

# WebSocket event for when someone disconnects
@socketio.on('disconnect')
def handle_disconnect():
    print('Someone disconnected from the WebSocket!')

# Run the app with SocketIO
if __name__ == '__main__':
    print("Starting WebSocket app...")
    print("Open your browser and go to: http://localhost:5000")
    socketio.run(app, debug=True)
