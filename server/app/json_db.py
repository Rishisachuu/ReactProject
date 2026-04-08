import json
import os
import uuid
from datetime import datetime

class JsonDB:
    def __init__(self, file_path):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        directory = os.path.dirname(self.file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump({}, f)

    def _read_data(self):
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def _write_data(self, data):
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4, default=str)

    def get_collection(self, collection_name):
        return Collection(self, collection_name)

class Collection:
    def __init__(self, db, name):
        self.db = db
        self.name = name

    def find_one(self, query):
        data = self.db._read_data()
        docs = data.get(self.name, [])
        for doc in docs:
            match = True
            for k, v in query.items():
                if k == '_id':
                    if str(doc.get('_id')) != str(v):
                        match = False
                        break
                elif doc.get(k) != v:
                    match = False
                    break
            if match:
                return doc
        return None

    def insert_one(self, document):
        data = self.db._read_data()
        if self.name not in data:
            data[self.name] = []
        
        if '_id' not in document:
            document['_id'] = str(uuid.uuid4())
        
        # Convert datetime objects to strings
        for k, v in document.items():
            if isinstance(v, datetime):
                document[k] = v.isoformat()
        
        data[self.name].append(document)
        self.db._write_data(data)
        
        class InsertResult:
            def __init__(self, inserted_id):
                self.inserted_id = inserted_id
        
        return InsertResult(document['_id'])

    def update_one(self, query, update_data):
        data = self.db._read_data()
        docs = data.get(self.name, [])
        
        found_index = -1
        for i, doc in enumerate(docs):
            match = True
            for k, v in query.items():
                if k == '_id':
                    # Handle both string and ObjectId-like strings
                    if str(doc.get('_id')) != str(v):
                        match = False
                        break
                elif doc.get(k) != v:
                    match = False
                    break
            if match:
                found_index = i
                break
        
        if found_index != -1:
            doc = docs[found_index]
            if '$set' in update_data:
                for k, v in update_data['$set'].items():
                    if isinstance(v, datetime):
                        doc[k] = v.isoformat()
                    else:
                        doc[k] = v
            
            data[self.name][found_index] = doc
            self.db._write_data(data)
            
            class UpdateResult:
                def __init__(self, modified_count):
                    self.modified_count = modified_count
            
            return UpdateResult(1)
        
        class UpdateResult:
            def __init__(self, modified_count):
                self.modified_count = modified_count
        
        return UpdateResult(0)
