import os
import tempfile
from functools import reduce

from tinydb import TinyDB, Query
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost:27017/') # I could provide the MongoDB Atlas URL, but I'll run the MongoDB containerized
db = client['student_database']
students_collection = db.students

# db_dir_path = tempfile.gettempdir()
# db_file_path = os.path.join(db_dir_path, "students.json")
# student_db = TinyDB(db_file_path)

def add(student=None):
    # Convert student object to dict and use custom student_id as _id
    student_dict = student.to_dict()
    student_dict["_id"] = student.student_id

    # Check if a student with the given _id already exists
    if students_collection.count_documents({"_id": student_dict["_id"]}) > 0:
        return 'already exists', 409

    # Insert the student document with a custom _id
    students_collection.insert_one(student_dict)
    return student.student_id


# def add(student=None):
#     queries = []
#     query = Query()
#     queries.append(query.first_name == student.first_name)
#     queries.append(query.last_name == student.last_name)
#     query = reduce(lambda a, b: a & b, queries)
#     res = student_db.search(query)
#     if res:
#         return 'already exists', 409

#     doc_id = student_db.insert(student.to_dict())
#     student.student_id = doc_id
#     return student.student_id

def get_by_id(student_id=None, subject=None):
    student = students_collection.find_one({"_id": student_id})
    if not student:
        return 'not found', 404
    student['student_id'] = student['_id']
    del student['_id']
    return student


# def get_by_id(student_id=None, subject=None):
#     student = student_db.get(doc_id=int(student_id))
#     if not student:
#         return 'not found', 404
#     student['student_id'] = student_id
#     print(student)
#     return student

def delete(student_id=None):
    result = students_collection.delete_one({"_id": student_id})
    if result.deleted_count == 0:
        return 'not found', 404
    return student_id


# def delete(student_id=None):
#     student = student_db.get(doc_id=int(student_id))
#     if not student:
#         return 'not found', 404
#     student_db.remove(doc_ids=[int(student_id)])
#     return student_id