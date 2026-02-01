# 🧾 AI-powerd Scientific Paper Search Tool

A LangChain + Streamlit app for finding scientific papers that match a user's description. The Ollama LLM converts input into Google Scholar search query, Scholarly retrives results and the LLM filters the most relevant papers based on abstract similarity to the user's description.

## 🚀 Features
- Streamlit-based web UI (https://streamlit.io)
- Uses locally installed LLM via Ollama (https://github.com/ollama/ollama)
- Retriving scientific papers via Scholarly (https://github.com/scholarly-python-package/scholarly)
- LangChain for chaining Ollama with Scholarly (https://github.com/langchain-ai/langchain)

## ⚙️ Requirements
- Python 3.11+
- Ollama installed and running locally
- installed libraries from requirements.txt 
- chosen proxy service for Scholarly, eg. Scraper API (https://www.scraperapi.com)

## 🧰 Usage
### Installing
git clone https://github.com/S2ym0d/PaperHunt.git

cd PaperHunt

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

### Setting up PROXY
In the source code app.py in the CONFIG PROXY part set up desired proxy service for Scholarly


### Running the app
streamlit run app.py
