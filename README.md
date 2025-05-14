#  Tech Debt QnA API

A **RAG-based (Retrieval-Augmented Generation)** FastAPI service to answer technical debt questions using a PDF dataset and Gemini 1.5.  
It also exposes project-wise metrics extracted from the PDF, such as **code smells, refactorings, and faults** for Apache projects.

---

##  Features

- 🤖 Ask natural language questions about technical debt using Gemini + LangChain
- 📊 View project-wise metrics: code smells, faults, and refactorings
- 📎 Auto-parses and indexes `The_Technical_Debt_Dataset.pdf`
- 🧠 Uses `LangChain`, `pdfplumber`, and `Chroma` for RAG-style QnA

---

##  Project Structure

tech_debt/
├── app/
│   ├── main.py
│   ├── qa_engine.py
│   ├── metrics_parser.py
│
├── data/
│   ├── All_RAG_Project_problem_statements.pdf      #contains many problem statements that you can look into and work on
│   └── The_Technical_Debt_Dataset.pdf              #the dataset that i have used
│
├── vectorstore/        # Auto-created by Chroma
│
├── .env
├── .gitignore
├── requirements.txt
├── Dockerfile
└── README.md



---

###  Getting Started

1. Clone the repo
git clone https://github.com/shhriya/rag_tech_debt.git
cd tech_debt_api
2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate         # On Windows
3. Install dependencies
pip install -r requirements.txt
4. Create a .env file in the root:
GOOGLE_API_KEY=your_google_api_key_here
5. Run the server
cd app
uvicorn main:app --reload

Test with Swagger
Once running, open:
http://127.0.0.1:8000/docs

Test Docker locally
# Build the image
docker build -t tech-debt-api .
# Run it
docker run -p 8000:8000 --env-file .env tech-debt-api



####  API Endpoints
🧠 Ask a question
POST /ask_tech_debt
{
  "question": "What are the most common code smells?"
}


📊 Get project metrics
GET /metrics_summary/{project_name}

Example:
GET /metrics_summary/Apache Hive
📃 List available projects
GET /project_names


#####  Built With
FastAPI
LangChain
Gemini (Google Generative AI)
Chroma
pdfplumber