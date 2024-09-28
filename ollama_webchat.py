#!/usr/bin/env python3

from flask import Flask, render_template_string, request, jsonify
import ollama
from ollama import Client

app = Flask(__name__)

client = Client(host='http://localhost:11434')

@app.route('/')
def index():
    return render_template_string("""
<html>
  <head>
    <!-- Add these two meta tags for responsive design -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <!-- Add a title tag to improve SEO and accessibility -->
    <title>ChatBot</title>

    <!-- Add basic CSS styles for responsiveness -->
    <style>
      /* Make the input field responsive */
      #message {
        width: 80%;
        padding: 10px;
        font-size: 16px;
        margin-bottom: 10px;
      }

      /* Make the button responsive */
      button {
        background-color: #4CAF50; /* Green */
        color: white;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        cursor: pointer;
      }

      /* Make the responses container responsive */
      #responses {
        width: 80%;
        padding: 10px;
        margin-bottom: 20px;
      }
    </style>
  </head>

  <body>
    <h1>ChatBot</h1>
    <input id="message" type="text" placeholder="Type your message...">
    <button onclick="send_message()">Send Message</button>
    <div id="responses"></div>

    <!-- Move the script tags to the head section for better performance -->
    <script src="https://cdn.jsdelivr.net/npm/axios@0.21.1/dist/axios.min.js"></script>
    <script>
      function send_message() {
        const msg = document.getElementById("message").value;
        axios.post('/chat', { message: msg })
          .then(response => {
            const responseHTML = `<p style="color:red;"> >> ${msg}</p><p>${response.data.response}</p>`;
            document.getElementById('responses').innerHTML += responseHTML;
            document.getElementById("message").content += responseHTML;
          })
          .catch(error => {
            console.error(error);
          });
      }
    </script>
  </body>
</html>
    """, _internal=True)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    message = {'role': 'user', 'content': user_input}
    response = client.chat(model='llama3.1', messages=[message])
    return jsonify({'response': response['message']['content']})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7734)
