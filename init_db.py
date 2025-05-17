# init_db.py
from backend.database import create_db_and_tables, create_prompt_table,create_model_table
print("Initializing databases...")
create_db_and_tables()
create_prompt_table()
create_model_table()
print("Done.")

