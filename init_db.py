
# FILE: init_db.py
from backend.database import create_db_and_tables, create_prompt_table
print("Initializing databases...")
create_db_and_tables()
create_prompt_table()
print("Done.")
