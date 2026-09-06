# Self-Improving Text-to-SQL with LLMs

This repository contains the codebase for a project on NTU course: Applied deep learning 2024. The project includes two tasks about LLM benchmark, while this README focuses specifically on the **Text-to-SQL component** and the self-improvement approach developed for the project.

The Text-to-SQL system uses **Llama 3.1 8B Instruct** to generate SQL queries from natural-language questions and database schemas. It combines multiple SQL candidates, SQLite-based validation, candidate selection, and retrieval-augmented generation (RAG) to improve performance over the course of the benchmark.

## 🎥 Group Presentation

[Watch the Group Presentation on methods](https://drive.google.com/file/d/1I7ZmwCcKp15hrgGGKId2Le7qJ1QNsaE9/view?usp=drive_link)

## Overview

The goal of the Text-to-SQL system is to generate executable SQL queries for questions over relational databases.

Instead of generating only a single SQL query, the system generates multiple candidates and uses execution-based validation and candidate selection to improve reliability.

The system also incorporates a simple **self-improvement mechanism**: when a generated SQL query is evaluated as correct, the question-SQL pair is stored in a retrieval database and can be used as a few-shot example for future questions.

The overall pipeline is:

```text
Natural-language Question
          |
          v
     Database Schema
          |
          v
   RAG Example Retrieval
          |
          v
      Prompt Builder
          |
          v
 Llama 3.1 8B Instruct
          |
          v
 Generate 5 SQL Candidates
          |
          v
 SQLite Validation
          |
          v
 Candidate Selection
 (Frequency Voting / LLM)
          |
          v
    Selected SQL
          |
          v
   BIRD Evaluation
          |
          v
      Correct?
       /     \
     Yes      No
      |        |
      v        |
Store Q-SQL    |
in RAG         |
      |        |
      +--------+
```



## Self-Improvement

The self-improvement mechanism does **not** fine-tune the model or modify its weights.

Instead, the model remains fixed while the system gradually accumulates successful examples during evaluation.

When the generated SQL is correct:

1. The original question and generated SQL are recorded.
2. The pair is inserted into an in-memory RAG database.
3. Similar examples can be retrieved for future questions.
4. These examples are inserted into the prompt as few-shot demonstrations.

Therefore, the system can improve its future predictions based on previously successful solutions without performing model fine-tuning.

```text
Correct Question-SQL Pair
          |
          v
      RAG Memory
          |
          v
Retrieve Similar Examples
          |
          v
Add to Future Prompt
          |
          v
Better Context for SQL Generation
```

## Multiple Candidate Generation

For each question, the system generates **five SQL candidates**.

Each candidate is then checked using SQLite to determine whether it is syntactically executable against the provided database schema.

The candidate selection process works approximately as follows:

* If only one valid candidate exists, it is selected.
* If multiple valid candidates exist, duplicate SQL queries are counted.
* If one query appears at least three times, it is selected.
* If multiple candidates appear twice, the system uses the LLM to select between them.
* If every candidate appears only once, the LLM selects from the valid candidates.

This combines **self-consistency**, execution-based validation, and LLM-based selection.

## Retrieval-Augmented Generation

The Text-to-SQL agent uses retrieval-augmented generation to provide successful previous examples to the model.

The RAG system:

* Uses **BAAI/bge-base-en-v1.5** for text embeddings.
* Uses **FAISS** for similarity search.
* Stores previously successful **Question ??SQL** pairs.
* Retrieves similar examples for future questions.
* Uses the retrieved examples as few-shot demonstrations.

The RAG memory is currently maintained **in memory during a benchmark run** and is not persisted to disk.

## Benchmark

The Text-to-SQL component uses the **BIRD (BIg Bench for large-scale Database)** benchmark through the StreamBench project.

The benchmark evaluates whether the generated SQL produces the same execution result as the reference SQL.

The main evaluation metric is:

**Execution Accuracy (EX)**

```text
EX = Number of correctly executed queries
     -----------------------------------
          Total number of queries
```

Two SQL queries are considered correct when their execution results match.

## Model and Technologies

| Component            | Technology            |
| -------------------- | --------------------- |
| Language Model       | Llama 3.1 8B Instruct |
| Embedding Model      | BAAI/bge-base-en-v1.5 |
| Vector Search        | FAISS                 |
| Database             | SQLite                |
| Benchmark            | BIRD                  |
| Dataset Platform     | Hugging Face Datasets |
| Programming Language | Python                |

## Project Structure

The repository contains the complete original group project codebase.

The main files related to Text-to-SQL are:

```text
text-to-sql-self-improvement/
|
+-- benchmarks/
|   +-- base.py
|   +-- text_to_sql.py
|   +-- text2sql_utils/
|       +-- sqlite_interpreter.py
|       +-- string_formatter.py
|
+-- base.py
+-- execution_pipeline.py
+-- main.py
+-- medical_records.py
+-- utils.py
|
+-- README.md
+-- requirements.txt
+-- .gitignore
```

### Important Components

**`main.py`**

Contains the main agents used by the project, including:

* `ClassificationAgent`
* `LocalModelAgent`
* `SQLGenerationAgent`

The `SQLGenerationAgent` contains the main Text-to-SQL logic.

**`execution_pipeline.py`**

Controls the sequential benchmark process:

1. Load benchmark data.
2. Generate a prediction.
3. Evaluate the prediction.
4. Provide correctness feedback.
5. Update the agent's RAG memory when the prediction is correct.
6. Continue to the next question.

**`benchmarks/text_to_sql.py`**

Implements the BIRD Text-to-SQL benchmark and execution-based evaluation.

**`benchmarks/text2sql_utils/`**

Contains utilities for SQLite execution and SQL-related prompt formatting.

**`utils.py`**

Contains the RAG implementation and other utilities shared by the project.

## Installation

Clone the repository and install the required Python packages.

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd text-to-sql-self-improvement
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Then install the required dependencies:

```bash
pip install -r requirements.txt
```

## Hugging Face Authentication

The project uses Hugging Face models, including Llama 3.1 8B Instruct.

You may need to authenticate with Hugging Face before running the project:

```bash
huggingface-cli login
```

Do **not** put your Hugging Face token directly into the source code.

## Running the Text-to-SQL Benchmark

The Text-to-SQL benchmark can be run using:

```bash
python main.py --bench_name sql_generation_public --device <device> --output_path <path>
```

For example, using CUDA:

```bash
python main.py --bench_name sql_generation_public --device cuda --output_path ./output/results.csv
```

The model can optionally be loaded using 8-bit quantization:

```bash
python main.py --bench_name sql_generation_public --device cuda --output_path ./output/results.csv --use_8bit
```

## Configuration

Some important configuration parameters include:

### Candidate Generation

The system generates five SQL candidates for each question.

```text
consist_num = 5
```

### Maximum Generation Length

The default maximum number of generated tokens is:

```text
max_tokens = 1024
```

### RAG Retrieval

The RAG system retrieves similar examples from previously successful predictions.

The retrieval configuration uses FAISS similarity search and retrieves up to 16 examples.

### Sequential Learning

The benchmark is processed sequentially.

This means that examples generated earlier in the benchmark can influence later predictions if those examples were evaluated as correct.

## Important Notes

### No Fine-Tuning

The self-improvement mechanism does not perform gradient-based training or fine-tuning.

The language model's parameters remain unchanged throughout the benchmark.

Instead, improvement comes from dynamically adding successful examples to the prompt.

### In-Memory RAG

The RAG database currently exists only during the running process.

Previously learned examples are not automatically preserved between separate runs.

### Dataset and Database Files

The BIRD database files are expected to be available locally according to the benchmark configuration.

Large datasets, database files, model weights, generated outputs, and logs should generally **not** be committed to the Git repository.

## Project Context

This repository is based on a group project on LLM benchmarking.

The original project contains multiple benchmark tasks. The README focuses on the **Text-to-SQL component**, including the SQL generation agent, candidate selection, execution-based validation, and self-improvement through RAG.

## Presentation

For an overview of the complete group project:

[Watch the Group Presentation on result and discussion](https://drive.google.com/file/d/1vFMYZsYEkNyRY20cX9XDhsmY4OhuA57P/view?usp=drive_link)

## Acknowledgements

This project was developed as part of a group project on LLM benchmarking.

The Text-to-SQL component focuses on improving SQL generation through:

* Multiple candidate generation
* SQLite-based validation
* Self-consistency
* LLM-based candidate selection
* Retrieval-augmented generation
* Sequential self-improvement

## License

Add the appropriate license for this project if applicable.

