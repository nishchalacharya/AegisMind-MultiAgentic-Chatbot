"""
Long-Term Memory - Persisent facts about the user 
Stored in SQLite database so it survives across sessions
"""

import sqlite3 
from pathlib import Path 
from typing import List,Dict,Optional 
from datetime import datetime 


class LongTermMemory:
    """  
    Stores persistent facts about users in SQLite.
    Each fact is a simple key-value pair tied to a user_id.
    """

    def __init__(self,db_path: str = "data/memory.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True , exist_ok=True)
        self._init_db()


    def _init_db(self):
        """ create the facts table if it doesn't exist """
        conn =  sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS facts(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       user_id TEXT NOT NULL,
                       fact_key TEXT NOT NULL,
                       fact_value TEXT NOT NULL ,
                       created_at TEXT NOT NULL,
                       UNIQUE(user_id,fact_key)
                       )
                       """
                       )
        conn.commit()
        conn.close()
        print(f"Initialized Long-Term Memory database at {self.db_path}")

    
    def store_fact(self,user_id:str ,key: str , value: str):
        """
        Store or update a fact about the user in the database.
        
        Args: 
            user_id: Identifier for the user 
            key: The fact's key (e.g. "name" ,  "favorite_color")
            value: The  actual fact's value 
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO facts(user_id,fact_key,fact_value,created_at) 
                       VALUES(?,?,?,?)
                       ON CONFLICT(user_id,fact_key)
                       DO UPDATE SET fact_value = excluded.fact_value, created_at= excluded.created_at
                       """,(user_id,key,value , datetime.now().isoformat()))
        
        conn.commit()
        conn.close()

        print(f"stored fact: {key} = {value} for user {user_id}")


    def get_fact(self,user_id:str, key:str) -> Optional[str]: 
        """Retrieve a specific fact """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
                       SELECT fact_value
                       FROM facts 
                       WHERE user_id = ? AND fact_key = ? 
                       """,(user_id,key))
        
        row = cursor.fetchone()
        conn.close()

        return row[0] if row else None 
    

    def get_all_facts(self,user_id: str) -> Dict[str,str]:
        """Retrieve all known facts about a user"""
        conn =  sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
                       SELECT fact_key, fact_value 
                       FROM facts 
                       WHERE user_id = ? 
                       """,(user_id,))
        rows = cursor.fetchall()
        conn.close()

        return {key:value for key,value in rows}
    

    def delete_fact(self,user_id:str , key:str): 
        """ Delete a specific fact about a user """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
                       DELETE from facts 
                       WHERE user_id = ? AND fact_key = ?
                       """,(user_id,key))
        conn.commit()
        conn.close()
        print(f"Deleted fact: {key} for user {user_id}")


# Test the long term memory 

if __name__ == "__main__":
    memory = LongTermMemory(db_path="data/test_memory_db")

    # Store some facts 
    memory.store_fact("nishchal","name","Nishchal Sharma")
    memory.store_fact("nishchal","favorite_color","blue")
    memory.store_fact("nishchal","hobby","coding")
    memory.store_fact("nishchal","location","Nepal")


    # Retrieve a  single fact 
    name = memory.get_fact("nishchal","name")
    print(f"Retrieved name: {name}")


    # Retrieve all facts 
    all_facts =  memory.get_all_facts("nishchal")
    print("All facts about nishchal:")  
    for key,value in all_facts.items():
        print(f"  {key}: {value}")


    # update an existing fact (should overwrite , not duplicate )
    memory.store_fact("nishchal","favorite_color","green")
    updated_color = memory.get_fact("nishchal","favorite_color")
    print(f"Updated favorite color: {updated_color}")





        



