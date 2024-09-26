from gtts import gTTS
import speech_recognition as sr
from pydub import AudioSegment
import mysql.connector
from transformers import pipeline

# Change the config details as per your machine 

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'tutorial'
}


# Step 1: Convert passage to audio
def text_to_speech(text, filename="output.mp3"):
    tts = gTTS(text)
    tts.save(filename)
    print(f"Audio file saved as {filename}")


# Step 2: Convert audio file back to text (Speech-to-Text)
def audio_to_text(audio_file):
    recognizer = sr.Recognizer()
    # Convert MP3 to WAV
    audio = AudioSegment.from_mp3(audio_file)
    wav_filename = "output.wav"
    audio.export(wav_filename, format="wav")
    
    with sr.AudioFile(wav_filename) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        print(f"Converted Text: {text}")
        return text


# Step 3: Extract key points from the text using prompt 
def extract_key_points(text):
    print("Starting Key Points Extraction...")
    
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    
    key_points = summarizer(text, max_length=100, min_length=50, do_sample=False)
    
    extracted_points = [point['summary_text'] for point in key_points]
    print(f"Extracted Key Points: {extracted_points}")
    return extracted_points


# Step 4: Store Extracted Points in Database
def store_points_in_db(points):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS KeyPoints (
                      id INT AUTO_INCREMENT PRIMARY KEY,
                      point TEXT)""")
    
    for point in points:
        cursor.execute("INSERT INTO KeyPoints (point) VALUES (%s)", (point,))
    
    conn.commit()
    print("Key Points stored in database.")
    cursor.close()
    conn.close()

def process_text(text):
    print("Starting Text-to-Speech Conversion...")
    text_to_speech(text)  
    
    print("Starting Speech-to-Text Conversion...")
    converted_text = audio_to_text("output.mp3") 
    
    print("Starting Key Points Extraction...")
    key_points = extract_key_points(converted_text)  

    print("Storing Key Points in Database...")
    store_points_in_db(key_points) 

if __name__ == "__main__":
    passage = """Computers have become an integral part of modern society, influencing almost every aspect of our daily lives. A computer is an electronic device capable of performing complex calculations at remarkable speeds, processing large amounts of data, and solving problems that would be impossible for a human to solve manually. They come in various forms, including personal computers, laptops, tablets, and smartphones, and serve a variety of purposes from entertainment to education to business.

    At the heart of a computer is its central processing unit (CPU), often referred to as the "brain" of the computer. The CPU executes instructions from software programs and coordinates the activities of all other hardware components. Computers also have memory, which stores data and instructions temporarily or permanently. Random Access Memory (RAM) is volatile memory used for temporary storage of data while the computer is running, whereas storage devices like hard drives and solid-state drives (SSD) provide long-term data storage.

    The modern computer system is also equipped with input and output devices. Input devices like keyboards, mice, and touchscreens allow users to interact with the computer, while output devices such as monitors, printers, and speakers enable the computer to present data to the user. Software, which includes operating systems and applications, is the medium through which users perform tasks on a computer. An operating system, such as Windows, macOS, or Linux, manages the computer’s resources and allows hardware and software to communicate effectively.

    Networking is another key area in computing. With the advent of the internet, computers have gained the ability to connect to other devices across the globe, allowing for the exchange of information and communication in real-time. This has revolutionized many industries, including communication, business, healthcare, and education, making the world more interconnected.

    Additionally, computers have enabled the development of technologies such as artificial intelligence (AI), machine learning, and automation, all of which continue to shape the future of innovation. AI systems, for example, leverage the power of computers to simulate human intelligence, allowing machines to learn, make decisions, and even improve over time. This has significant implications for industries such as healthcare, where AI is used for diagnostics, or manufacturing, where automation is reducing the need for human labor in repetitive tasks.

    Despite their many advantages, computers also pose challenges, including concerns about privacy, security, and the digital divide. The rise of cyber-attacks and data breaches has highlighted the need for robust cybersecurity measures to protect sensitive information stored on computers. Additionally, while computers have transformed many sectors, not everyone has access to them or the internet, which can perpetuate inequality in education and economic opportunities.

    In conclusion, computers are powerful tools that have revolutionized the way we live and work. From their hardware components to the software that drives them, and their ability to connect to a global network, computers will continue to play a pivotal role in shaping the future of technology and society."""

    # Run the entire process on the provided passage
    process_text(passage)
