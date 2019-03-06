# Record and remember the works forged by brokkr.py
from tinydb import TinyDB, Query
import os

def record(works):
    mimisbrunnr = TinyDB(os.getenv('APPDATA')+r'\mtga-project-vue\db.json')
    memories = mimisbrunnr.table('matches')
    
    query = Query()
    
    for key in works:
        # check if key is already a match id in the database
        q = memories.search(query.matchId==key)
        if not q:
            memories.insert(works[key])
        
    # return mimisbrunnr