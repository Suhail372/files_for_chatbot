# School-Info-Chatbot
## Description
This project is a chatbot designed to provide information about schools based on location. It leverages sentence embeddings, FAISS for similarity search, and a language model for generating responses. The user can choose between two locations, Hyderabad and Bangalore, and the chatbot will provide relevant information based on the selected location.

## Disclaimer
The data used in this project was sourced from yellowslate.com. We do not claim any ownership over the data and it is used solely for educational and learning purposes. This project is not intended for commercial use. If you are the owner of the data and have any concerns, please contact us at suhailazad372@gmail.com to have the data removed.

## Features
- Location-based school information
- Uses sentence embeddings for vector search
- Integrates with a language model for generating responses
- Interactive interface with Streamlit
- Tunnel the Streamlit app using ngrok for public access


## How to Run the Project

### Prerequisites

The project requires the following packages. You can install them by running `pip install -r requirements.txt` in command prompt:
- Python 3.x
- Sentence Transformers
- FAISS-GPU
- Streamlit
- Pyngrok

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Suhail372/files_for_chatbot
    ```
2. Navigate to the project directory:
    ```sh
    cd files_for_chatbot
    ```
3. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Navigate to the project directory:
    ```sh
    cd /content/files_for_chatbot
    ```
2. Start the ngrok tunnel:
    ```python
    from pyngrok import ngrok
    ngrok.set_auth_token('YOUR_NGROK_AUTH_TOKEN')  # Optional
    public_url = ngrok.connect("http://localhost:8501")
    print(f" * ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:8501\"")
    ```
3. Run the Streamlit app:
    ```sh
    streamlit run /content/files_for_chatbot/Chatbot_logic_main.py.py &
    ```
## Contact

For any questions or suggestions, feel free to reach out to [suhailazad372@gmail.com].
