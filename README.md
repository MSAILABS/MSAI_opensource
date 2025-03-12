# MSAI_opensource

## Open Source AI Agent & RAG Platform

Welcome to our open source AI Agent and Retrieval Augmented Generation (RAG) platform! This project is designed for tech enthusiasts and developers eager to build innovative, AI-driven applications with dynamic, context-aware capabilities.

Overview
Our platform is built on a robust microservices architecture, ensuring scalability, flexibility, and modularity. The system consists of four key services working together to deliver a comprehensive AI experience:

1. **_Backend Service_**<br>
   Tech Stack: FastAPI, PyTorch, Sqlalchemy<br>
   Role: Serves as the middleware between the frontend and the AI agent, extracts text from files and save data into sqlite database. It processes incoming requests, integrates deep learning models, and orchestrates communication between services.
2. **_Agents Service_**<br>
   Tech Stack: FastAPI, llama-index, lanceDB<br>
   Role: Manages AI agents and implements RAG (Retrieval Augmented Generation). This service retrieves contextually relevant information to enhance AI response generation, ensuring accurate and informed outputs.
3. **_UI Service_**<br>
   Tech Stack: Next.js, TailwindCSS<br>
   Role: Provides an intuitive interface for interacting with the chatbot and managing records. Users can upload documents (PDF, Word, TXT) to create records for context-specific responses, or choose a mode for more general answers.
4. **_RabbitMQ Service_**<br>
   Role: Acts as the messaging backbone. AI agents publish their "thoughts" (internal processing details) to a RabbitMQ queue. The backend then consumes these messages and, using server-sent events, relays them to the UI in real time, offering transparency into the AI's reasoning process.
   <br/>

## Getting Started

Explore the repository, follow the setup instructions, and dive into our contribution guidelines to start using or enhancing the platform. We welcome feedback and collaboration to help evolve this innovative project.

Happy coding!

## Run Application Using Docker

1. **Install Docker:**  
   Ensure Docker is installed on your machine.

2. **Install Node v20:**  
   Make sure Node.js version 20.18.1 is installed on your machine.

3. **Clone the Repository:**  
   Clone the project repository to your local environment.

4. **Install UI Dependencies:**  
   Open the `ui` folder in your terminal and run:

   ```bash
   cd ui
   npm install
   ```

   _Note: Docker requires the `.next` folder for the application to run._

5. **Configure the UI Service:**  
   In the `ui` folder, create a `.env` file. This file can be left blank if no variables are needed.

6. **Configure the Agents Service:**  
   In the `agents` folder, create a `.env` file and add the following variables for using the Ollama service locally:

   - `OLLAMA_ENDPOINT` (example: `"http://localhost:11434"`)
   - `OLLAMA_LLM` (example: `"deepseek-r1:32b"`)
   - `OLLAMA_EMBED` (example: `"all-minilm"`)

7. **Build and Run Containers:**  
   From the repository root in your terminal, execute:

   ```bash
   docker-compose up --build
   ```

   This command builds the Docker images and starts the containers.

8. **Access the Application:**  
   Once the containers are running, open your browser and navigate to [http://localhost:3000](http://localhost:3000) to access the UI and run the application.

---

## Run Application Natively on Your OS

1. **Install Python 3.11:**  
   Ensure that Python 3.11 is installed on your system.

2. **Install Node v20:**  
   Make sure Node.js version 20.18.1 is installed on your machine.

3. **Install Ollama:**  
   Install the Ollama service and pull the required LLM and embedding models.

4. **Clone the Repository:**  
   Clone the project repository to your local environment.

5. **Create a Python Virtual Environment for Agents:**  
   In the `agents` folder, create a virtual environment by running:

   ```bash
   python3 -m venv venv
   ```

6. **Activate the Virtual Environment:**

   - On Linux/macOS:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\scripts\activate
     ```

7. **Install Python Dependencies (Agents):**  
   With the virtual environment activated, install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

8. **Set Up the Backend:**  
   Repeat steps 5–7 within the `backend` folder:

   - Create a virtual environment.
   - Activate it.
   - Install dependencies using the `requirements.txt` file.

9. **Install UI Dependencies:**  
   Open the `ui` folder in your terminal and run:

   ```bash
   npm install
   ```

10. **Configure the Agents Service:**  
    In the `agents` folder, create a `.env` file and add the following variables for using the Ollama service locally:

    - `OLLAMA_ENDPOINT` (example: `"http://localhost:11434"`)
    - `OLLAMA_LLM` (example: `"deepseek-r1:32b"`)
    - `OLLAMA_EMBED` (example: `"all-minilm"`)

11. **Change URL's in Backend and Agents Service**

    - open file `\MSAI_opensource\backend\core\configurations.py`.
    - change `rabbitmq` and `agents` to `localhost` (reason for this is that we needed to the names are responsible for connecting services inside docker network.).
    - open file `\MSAI_opensource\agents\AI\agents\utilities.py`.
    - change `rabbitmq` to `localhost` on line 10.

12. **Run RabbitMQ Queue locally**  
    you can run RabbitMQ easily using docker. Make sure you have docker installed and run terminal command

    ```bash
    docker run -itd --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:4.0-management
    ```

13. **Run Services**

    - Run ui using terminal command on ui folder path

    ```bash
    npm run dev
    ```

    - Run backend using terminal command on backend folder path after activating virtual environment

    ```bash
    python main.py
    ```

    - Run agents using terminal command on agents folder path after activating virtual environment

    ```bash
    python main.py
    ```

---

Follow these steps to set up and run the project either using Docker or natively on your operating system.
