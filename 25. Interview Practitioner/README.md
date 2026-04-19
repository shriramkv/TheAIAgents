# 🤖 Interview Practice Partner

Interview Practice Partner is a conversational AI-driven application designed to help you prepare for job interviews. Built with Python and Gradio, it simulates a realistic interview environment where you can practice answering role-specific questions, receive intelligent real-time feedback, and review a comprehensive performance report.

## 🌟 Features

- **Role & Difficulty Selection**: Tailor your interview experience by selecting your target role (e.g., Software Engineer, Data Scientist, Product Manager) and desired difficulty level (Easy, Medium, Hard).
- **Resume Integration**: Upload your resume (PDF format) to get personalized interview questions based on your background and experience.
- **Voice & Text Interaction**: Submit your answers by speaking through your microphone or typing them out.
- **AI Audio Responses**: Listen to the AI interviewer's questions naturally using integrated Text-to-Speech (TTS).
- **Real-Time Feedback**: Receive constructive feedback immediately after answering each question to understand areas of improvement.
- **Comprehensive Final Report**: Obtain a detailed evaluation at the end of the interview session, highlighting strengths, weaknesses, and actionable advice.

## 🛠️ Technology Stack

- **Python**: Core programming language.
- **Gradio**: Framework for building the interactive web-based UI.
- **OpenAI API**: Powers the AI interviewer (e.g., `gpt-4o-mini` for chat completions), Speech-to-Text (Whisper), and Text-to-Speech (TTS).
- **pypdf**: Extracts text from the uploaded PDF resumes.
- **python-dotenv**: Manages environment variables.

## 🚀 Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

Ensure you have Python 3.8+ installed on your machine.
You will also need an [OpenAI API Key](https://platform.openai.com/).

### Installation

1. **Clone or Download the Repository**
   Navigate to the project directory:
   ```bash
   cd interview_practice_partner
   ```

2. **Create a Virtual Environment** (Recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables Configuration**
   Create a `.env` file in the root directory (or rename a `.env.example` if it exists) and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   MODEL_NAME=gpt-4o-mini # Optional: Default model used by the application
   ```

### Running the Application

Start the application by running the following command:

```bash
python app.py
```

The application will start a local web server. Open your web browser and navigate to the URL provided in the terminal (usually `http://127.0.0.1:7860`).

## 🎮 How to Use

1. **Configure Interview**: Select your desired "Target Role" and "Difficulty Level".
2. **Upload Resume** *(Optional)*: Click "Upload Resume" and select a PDF file of your resume to get tailored questions.
3. **Start**: Click the **🚀 Start Interview** button. The AI will introduce itself and ask its first question.
4. **Answer**: 
   - Record your audio by clicking on the Microphone icon under "Voice Answer", **OR**
   - Type your answer in the "Text Answer" box.
5. **Submit**: Click **Submit Answer**. The AI will evaluate your answer, provide real-time feedback (visible in the "Real-time Feedback" accordion), and ask the next question via text and voice.
6. **End Interview**: When you are finished, click **End Interview & Get Report** to conclude the session and view your overall evaluation.

## 📁 Project Structure

- `app.py`: Main entry point launching the Gradio interface.
- `agent.py`: Contains the `InterviewAgent` class managing API interactions and generation logic.
- `prompts.py`: Stores prompt templates for question generation and feedback.
- `requirements.txt`: Project dependencies list.
- `services/`: Contains auxiliary service modules for Audio (STT/TTS) and Report generation.
- `ui/`: Contains the Gradio controller logic and configuration constants.
- `utils.py`: Helper functions and data class definitions for session management.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📝 License

This project is open-source and available under the terms of the MIT License.
