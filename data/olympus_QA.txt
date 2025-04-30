# Olympus_QA

**Olympus_QA** is a question-answering system focused on **mythology and folklore**. This project leverages **natural language processing (NLP)** techniques to provide accurate and informative answers to mythology-related queries.

## Features
- 🏺 **Mythology-Focused Question Answering**: Provides answers based on mythology and folklore.
- 🤖 **Natural Language Processing (NLP)**: Uses NLP models to process and generate responses.
- 🌐 **Interactive Interface**: Can be integrated into a chatbot or web app.

## Installation
### Prerequisites
Ensure you have the following installed:
- Python (>= 3.8)
- pip (Python package manager)
- virtualenv (optional but recommended)

### Steps
1. **Clone the repository**:
   ```
   git clone https://github.com/racheen/olympus_QA.git
   cd olympus_QA
2. **Create and activate a virtual environment (optional but recommended):**
    ```
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\\Scripts\\activate
    ```

3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```


## Usage
Run the application with:
```
streamlit run app.py
```
Alternatively, if it's a command-line application:

```
python main.py
```

## Deployment
If deploying on Streamlit Community Cloud:
1. Push your code to GitHub.
2. Create a requirements.txt file if not already present.
3. Specify the Python version in runtime.txt (e.g., python-3.9.18).
4. Deploy via Streamlit Cloud.