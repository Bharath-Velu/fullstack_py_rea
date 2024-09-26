from flask import Flask, render_template, jsonify
from gtts import gTTS
import os

app = Flask(__name__)

# Dictionary to map fruit names to the image files
fruits = {
    "apple": "apple.jpg",
    "mango": "mango.jpg",
    "banana": "banana.jpg",
    "grapes": "grapes.jpg",
    "orange": "orange.jpg"
}

# Route to render the index page
@app.route('/')
def index():
    return render_template('index.html', fruits=fruits)

# Route to handle the click event and return audio for the selected fruit
@app.route('/speak/<fruit>')
def speak(fruit):
    if fruit in fruits:
        # Convert the fruit name to speech
        tts = gTTS(text=fruit.capitalize(), lang='en')
        audio_path = f'C:\\Users\\Admin\\Tutorial_fullstack\\fruit_app\\static\\audio\\{fruit}.mp3'
        tts.save(audio_path)
        
        return jsonify({"audio_url": audio_path})
    else:
        return jsonify({"error": "Fruit not found"}), 404

if __name__ == '__main__':
    if not os.path.exists('C:\\Users\\Admin\\Tutorial_fullstack\\fruit_app\\static\\audio'):
        os.makedirs('C:\\Users\\Admin\\Tutorial_fullstack\\fruit_app\\static\\audio')
    app.run(debug=True)
