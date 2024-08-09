# Test-1 for RAG pipeline

This includes scripts for transforming model specifications into a unified schema, querying a vector database, and scraping web data. The following instructions will guide you through setting up the environment and installing the necessary dependencies.

## Requirements

Make sure you have Python installed. You can download Python from the [official website](https://www.python.org/).

## Installation

1. Clone the repository or download the project files to your local machine.

2. Create a virtual environment (optional but recommended):

    ```bash
    python -m venv env
    ```

3. Activate the virtual environment:

    - On Windows:
      ```bash
      .\env\Scripts\activate
      ```
    Note: If this script cannot be loaded then most probably you would need to change Powershell's execution policy.
    Open powershell and type in the following command which will make policy change for the current user. 
      ```bash
      Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
      ```

    - On macOS and Linux:
      ```bash
      source env/bin/activate
      ```

4. Install the required libraries using the `requirements.txt` file:

    ```bash
    pip install -r requirements.txt
    ```

## Libraries

The following libraries will be installed:

- `langchain_google_genai`
- `langchain`
- `chromadb`
- `sentence-transformers`
- `requests`
- `beautifulsoup4`

## Usage

After installing the dependencies, you can run the scripts provided in the project.

### To test this:

Run the script and you can change the query in the file:

```bash
python test_1/vector_embeddings.py
