from base import Agent
from execution_pipeline import main
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch
from utils import RAG, strip_all_lines
import random
from colorama import Fore, Style
import re
from collections import Counter
from transformers import logging as transformers_logging

transformers_logging.set_verbosity_error()
from huggingface_hub import login
login(#login with your hugging face token)

import warnings
import sqlite3
# Qwen2.5-7B-Instruct + Llama-3.1-8B-Instruct, self refine=5：{'accuracy': 0.5459183673469388}

##############################################
############# ClassificationAgent ############
##############################################

class LocalModelAgent(Agent):
    """
    A base agent that uses a local model for text generation tasks.
    """
    def __init__(self, config: dict) -> None:
        """
        Initialize the local model
        """
        super().__init__(config)
        self.llm_config = config
        self.model_name = 'meta-llama/Llama-3.1-8B-Instruct'
        if config['use_8bit']:
            quantization_config = BitsAndBytesConfig(
                load_in_8bit=True,
                llm_int8_has_fp16_weight=False
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                quantization_config=quantization_config,
                device_map=config["device"]
            )
        else:
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16,
                device_map=config["device"]
            )
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.rag = RAG(config["rag"])
        # Save the streaming inputs and outputs for iterative improvement
        self.inputs = list()
        self.self_outputs = list()
        self.model.eval()
        self.consist_num = 5
        print("consist_num: ", self.consist_num)
        
        #the 3 examples for original zero shot inferencing
        self.syntax_prompt = f"""\
SQL (Structured Query Language) is used to interact with relational databases. It allows you to retrieve, insert, update, and delete data stored in tables.

Common Commands:
1. SELECT: Retrieves data.
```sql 
SELECT column1, column2 FROM table_name WHERE condition;
```

2.INSERT: Adds data.
```sql
INSERT INTO table_name (column1, column2) VALUES (value1, value2);
```

3. DELETE: Removes data.
```sql
DELETE FROM table_name WHERE condition;
```

4. UPDATE: Modifies data.
```sql
UPDATE table_name SET column1 = value1 WHERE condition;
```

5. CREATE TABLE: Creates a new table.
```sql
CREATE TABLE table_name (
    column1 datatype,
    column2 datatype
);
```

6. DROP TABLE: Deletes a table.
```sql
DROP TABLE table_name;
```

Example SQL schema:
CREATE TABLE example_table (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    age INT
);

Example Query:
Retrieve names of people over 25:
SELECT name FROM people WHERE age > 25;
```sql
SELECT name FROM people WHERE age > 25;
```
SQL is case-insensitive but follows a readable structure. It is important to use the correct syntax to avoid errors."""

        self.initial_prompt = """\
        SQL schema: 
        CREATE TABLE "cards"  
        `(  
          id                      INTEGER           not null primary key autoincrement,  
          artist                  TEXT,  
          asciiName               TEXT,  
          availability            TEXT,  
          borderColor             TEXT,  
          convertedManaCost       REAL,  
          name                    TEXT,  
          rarity                  TEXT,  
          type                    TEXT,  
          uuid                    TEXT              not null unique  
        );

        CREATE TABLE "legalities"  
        (  
          id     INTEGER not null primary key autoincrement,  
          format TEXT,  
          status TEXT,  
          uuid   TEXT references cards (uuid)  
          on update cascade on delete cascade  
        );
        Question: Find the names of all cards that are legal in the 'Modern' format.
        ```sql 
        SELECT c.name  
        FROM cards c  
        JOIN legalities l ON c.uuid = l.uuid  
        WHERE l.format = 'Modern' AND l.status = 'Legal';
        ```
      
        SQL schema:
        CREATE TABLE "sets"  
        (  
          id               INTEGER           not null primary key autoincrement,  
          code             TEXT              not null unique,  
          name             TEXT,  
          releaseDate      DATE  
        );

        CREATE TABLE "cards"  
        (  
          id         INTEGER           not null primary key autoincrement,  
          name       TEXT,  
          setCode    TEXT,  
          rarity     TEXT,  
          uuid       TEXT              not null unique,  
          FOREIGN KEY (setCode) REFERENCES sets (code)  
        );
        Question: Get the names and release dates of sets containing rare cards.
        ```sql
        SELECT DISTINCT s.name, s.releaseDate  
        FROM sets s  
        JOIN cards c ON s.code = c.setCode  
        WHERE c.rarity = 'Rare';
        ```

        SQL schema:
        CREATE TABLE "rulings"  
        (  
            id   INTEGER not null primary key autoincrement,  
            date DATE,  
            text TEXT,  
            uuid TEXT references cards (uuid)  
            on update cascade on delete cascade  
        );

        CREATE TABLE "cards"  
        (  
            id   INTEGER           not null primary key autoincrement,  
            name TEXT,  
            uuid TEXT              not null unique  
        );
        Question: List the rulings and their dates for a card named 'Black Lotus'.
        ```sql
        SELECT r.date, r.text  
        FROM rulings r  
        JOIN cards c ON r.uuid = c.uuid  
        WHERE c.name = 'Black Lotus';
        ```"""
        

    def generate_response(self, messages: list) -> str:
        """
        Generate a response using the local model.
        """
        text_chat = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = self.tokenizer([text_chat], return_tensors="pt").to(self.model.device)

        generated_ids = self.model.generate(
            **model_inputs,
            max_new_tokens=self.llm_config["max_tokens"],
            do_sample=True
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        return self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    def update(self, correctness: bool) -> bool:
        """
        Update the agent based on the correctness of its output.
        """
        if correctness:
            question = self.inputs[-1]
            answer = self.self_outputs[-1]
            chunk = self.get_shot_template().format(question=question, answer=answer)
            self.rag.insert(key=question, value=chunk)
            return True
        return False

class SQLGenerationAgent(LocalModelAgent):
    """
    An agent that generates SQL code based on the given table schema and the user query.
    """
    @staticmethod
    def get_system_prompt() -> str:
        system_prompt = """\
        Act as a professional programmer.
        You will be given a table schema and a user query, and you need to generate the correct SQL code to answer the user query in the following format:
        ```sql\n<your_SQL_code>\n```"""
        return strip_all_lines(system_prompt)

    @staticmethod
    def get_zeroshot_prompt(table_schema: str, user_query: str, prompt: str) -> str:
        prompt = f"""\
        You are performing the text-to-SQL task. Here are some examples:
        
        {prompt}
        
        Now it's your turn.
        
        -- SQL schema:{table_schema}
        -- Using valid SQLite, answer the following question for the tables provided above.
        -- Question: {user_query}
        
        Now, generate the correct SQL code directly in the following format:
        ```sql\n<your_SQL_code>\n```"""
        return strip_all_lines(prompt)

    @staticmethod
    def get_shot_template() -> str:
        prompt = f"""\
        Question: {{question}}
        {{answer}}"""
        return strip_all_lines(prompt)

    @staticmethod
    def get_fewshot_template(table_schema: str, user_query: str) -> str:
        prompt = f"""\
        You are performing the text-to-SQL task. Here are some examples:
        
        {{fewshot_text}}
        
        Now it's your turn.
        
        -- SQL schema: {table_schema}
        -- Using valid SQLite, answer the following question for the SQL schema provided above.
        -- Question: {user_query}
        
        Now, generate the correct SQL code directly in the following format:
        ```sql\n<your_SQL_code>\n```"""
        return strip_all_lines(prompt)
    
    @staticmethod    
    def self_choose_template(table_schema: str, user_query: str, sql_code: list) -> str:
        option : str = ""  
        choice : str = "number"
        for i, code in enumerate(sql_code):
            option += f"{i+1}.\n```sql\n{code}\n```\n"
            choice += f" {i+1} or"
        choice = choice[:-2]
        
        prompt = f"""\
        You are an expert in SQL. Choose the correct SQL code based on the given schema and user query.

        Inputs:

        Schema:
        {table_schema} 
        
        User Query:
        {user_query}

        SQL Code:
        
        {option}

        Output:
        You need to choose the correct SQL code from the above options.
        
        Output format:
        sql code number: \n**<{choice}>**\n"""
        return strip_all_lines(prompt)
 
    def __call__(
        self,
        table_schema: str,
        user_query: str
    ) -> str:
        self.reset_log_info()
        prompt_zeroshot = self.get_zeroshot_prompt(table_schema, user_query, self.initial_prompt)
        prompt_fewshot = self.get_fewshot_template(table_schema, user_query)
        #cot_prompt = self.get_cot_prompt(table_schema, user_query)
    
        
        shots = self.rag.retrieve(query=user_query, top_k=self.rag.top_k) if (self.rag.insert_acc > 0) else []
        if len(shots):
            fewshot_text = "\n\n\n".join(shots).replace("\\", "\\\\")
            try:
                prompt = re.sub(pattern=r"\{fewshot_text\}", repl=fewshot_text, string=prompt_fewshot)
            except Exception as e:
                error_msg = f"Error ```{e}``` caused by these shots. Using the zero-shot prompt."
                print(Fore.RED + error_msg + Style.RESET_ALL)
                prompt = prompt_zeroshot
        else:
            print(Fore.YELLOW + "No RAG shots found. Using zeroshot prompt." + Fore.RESET)
            prompt = prompt_zeroshot
        
        #if rag has fewer than 4 shots, put them with the initail 3 examples
        if len(shots) < 4 and len(shots) != 0:
            start = "You are performing the text-to-SQL task. Here are some examples:"
            index = prompt.find(start) + len(start)
            prompt = prompt[:index-1] + "\n\n" + self.initial_prompt + prompt[index:] 
        # syntax prompt
        prompt = self.syntax_prompt + '\n\n' + prompt
        # print(prompt)
        pred_text_list = []
        sql_code_list = []
        consist_num = self.consist_num
        for i in range(consist_num):
            messages = [
                {"role": "system", "content": self.get_system_prompt()},
                {"role": "user", "content": prompt}
            ]
            pred_text_tmp = self.generate_response(messages)
            sql_code_tmp = self.parse_sql(pred_text_tmp)
            
            sql_code_state = self.validate_model_query(table_schema, sql_code_tmp)
            if sql_code_state: 
                pred_text_list.append(pred_text_tmp)
                sql_code_list.append(sql_code_tmp)
            # print(pred_text_tmp)
            if i == consist_num-1 and len(sql_code_list) == 0:
                pred_text = pred_text_tmp
                sql_code = sql_code_tmp

        
        if len(sql_code_list) == 1:
            sql_code = sql_code_list[0]
            pred_text = pred_text_list[0]
            
        elif len(sql_code_list) > 1:
            skip = []
            freq = [1] * len(sql_code_list)  
            for i in range(len(sql_code_list)):
                for j in range(i+1, len(sql_code_list)):
                    if i not in skip and sql_code_list[i] == sql_code_list[j]:
                        freq[i] += 1
                        skip.append(j)
            max_freq = max(freq)
        
            if max_freq >= 3:
                for i in range(len(freq)):
                    if freq[i] == max_freq:
                        sql_code = sql_code_list[i]
                        pred_text = pred_text_list[i]
            
            elif max_freq == 2:
                count = 0
                ind = []
                for i in range(len(freq)):
                    if freq[i] == max_freq:
                        count += 1
                        ind.append(i)
                if count == 1:
                    sql_code = sql_code_list[ind[0]]
                    pred_text = pred_text_list[ind[0]]
                
                else: 
                    choose_prompt = self.self_choose_template(table_schema, user_query, [sql_code_list[ind[0]], sql_code_list[ind[1]]])      
                    #debug
                    #print(choose_prompt)
                    #end debug
                    messages = [
                        {"role": "system", "content": self.get_system_prompt()},
                        {"role": "user", "content": choose_prompt}
                    ]
                    pred_text2 = self.generate_response(messages)
                    #print(pred_text2)
                    try:
                        choice = re.search(r"(?<=\*\*\d\*\*\n)(.*?)(?=\n)", pred_text2, re.DOTALL).group().strip()
                        # match = re.search(r"\*\*(\d+)\*\*", pred_text2)
                    except:
                        try:
                            # grab the first appear number in the text
                            choice = re.search(r"\d+", pred_text2).group().strip()
                        except:
                            print(Fore.RED + "No choice found in the response" + Style.RESET_ALL)
                            choice = "1"
                    if choice == "2":
                        pred_text = pred_text_list[1]
                        sql_code = sql_code_list[1] 
                    else:
                        pred_text = pred_text_list[0]
                        sql_code = sql_code_list[0]
                    
            else:
                choose_prompt = self.self_choose_template(table_schema, user_query, sql_code_list)
                #debug
                #print(choose_prompt)
                #end debug
                messages = [
                    {"role": "system", "content": self.get_system_prompt()},
                    {"role": "user", "content": choose_prompt}
                ]
                pred_text2 = self.generate_response(messages)
                #print(pred_text2)
                try:
                    choice = re.search(r"(?<=\*\*\d\*\*\n)(.*?)(?=\n)", pred_text2, re.DOTALL).group().strip()
                    # match = re.search(r"\*\*(\d+)\*\*", pred_text2)
                except:
                    try:
                        # grab the first appear number in the text
                        choice = re.search(r"\d+", pred_text2).group().strip()
                    except:
                        print(Fore.RED + "No choice found in the response" + Style.RESET_ALL)
                        choice = "1"
                for i in range(consist_num+1):
                    if choice == f"{i+1}":
                        pred_text = pred_text_list[i]
                        sql_code = sql_code_list[i]
                        break
                    if i == consist_num:
                        pred_text = pred_text_list[0]
                        sql_code = sql_code_list[0]
                
        self.update_log_info(log_data={
            "num_input_tokens": len(self.tokenizer.encode(self.get_system_prompt() + prompt)),
            "num_output_tokens": len(self.tokenizer.encode(pred_text)),
            "num_shots": str(len(shots)),
            "input_pred": prompt,
            "output_pred": pred_text,
        })

        self.inputs.append(user_query)
        self.self_outputs.append(f"```sql\n{sql_code}\n```")
        
        return sql_code

    @staticmethod
    def parse_sql(pred_text: str) -> str:
        """
        Parse the SQL code from the LLM's response.
        """
        pattern = r"```sql([\s\S]*?)```"
        match = re.search(pattern, pred_text)
        if match:
            sql_code = match.group(1)
            sql_code = sql_code.strip()
            return sql_code
        else:
            print(Fore.RED + "No SQL code found in the response" + Style.RESET_ALL)
            sql_code = pred_text
        return sql_code

    def get_filtered_statements(self, schema: str):
        """
        Splits the schema into individual SQL statements and handles multi-line CREATE TABLE,
        ALTER TABLE, and DROP TABLE statements. Filters out reserved objects like sqlite_sequence.
        """
        # Split the schema into statements based on CREATE TABLE, ALTER TABLE, or DROP TABLE keywords
        statements = []
        current_statement = []

        for line in schema.splitlines():
            line = line.strip()
            if not line:
                continue  # Skip empty lines

            # Detect the start of a new SQL statement
            if line.startswith(("CREATE TABLE", "ALTER TABLE", "DROP TABLE")):
                if current_statement:
                    # Add the previous statement to the list
                    statements.append(" ".join(current_statement))
                    current_statement = []
            current_statement.append(line)

        # Add the last statement, if any
        if current_statement:
            statements.append(" ".join(current_statement))

        # Filter out reserved objects (e.g., sqlite_sequence)
        filtered_statements = [
            stmt for stmt in statements if "sqlite_sequence" not in stmt.lower()
        ]
        return filtered_statements

    def validate_model_query(self, schema: str, model_query: str) -> int:
        """
        Validates the provided SQL query against the schema by:
        1. Filtering and executing the schema statements in a temporary SQLite database.
        2. Validating the provided query.
        retrun value:
        False. sql query error
        True. schema error, success
        """
        # Load the schema into an in-memory database
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()

        try:
            # Filter and execute schema statements one by one
            filtered_statements = self.get_filtered_statements(schema)
            for statement in filtered_statements:
                cursor.execute(statement)
        except Exception as e:
            #print(f"Schema Load Error: {e}")
            conn.close()
            return True  # Invalid schema

        # Validate the generated SQL query
        try:
            cursor.execute(model_query)
            result = cursor.fetchall()  # Ensure the query executes successfully
            validation_status = True
        except Exception as e:
            #print(f"Query Execution Error: {e}")
            validation_status = False

        # Finalize validation
        conn.close()
        return validation_status
        
if __name__ == "__main__":
    from argparse import ArgumentParser
    from execution_pipeline import main

    parser = ArgumentParser()
    parser.add_argument('--bench_name', type=str, default='classification_public')
    parser.add_argument('--device', type=str, default="cuda:0")
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--use_8bit', action='store_true', default=False)
    parser.add_argument('--output_path', type=str, default='./output.csv', help='path to save csv file for kaggle submission')
    parser.add_argument('--use_wandb', action='store_true')
    args = parser.parse_args()

    if args.bench_name.startswith("sql_generation"):
        max_tokens = 1024
        agent_name = SQLGenerationAgent
    else:
        raise ValueError("This repository only supports the SQL generation benchmark.")

    bench_cfg = {
        'bench_name': args.bench_name,
        'output_path': args.output_path
    }
    config = {
        'exp_name': f'self_streamicl_{args.bench_name}',
        'bench_name': bench_cfg['bench_name'],
        'max_tokens': max_tokens,
        'do_sample': False,
        'device': args.device,
        'use_8bit': args.use_8bit,
        'refine_num': 5,
        'rag': {
            'embedding_model': 'BAAI/bge-base-en-v1.5',
            'seed': 42,
            "top_k": 16,
            "order": "similar_at_top"
        }
    }
    agent = agent_name(config)
    main(agent, bench_cfg, debug=args.debug, use_wandb=args.use_wandb, wandb_name=config["exp_name"], wandb_config=config)
