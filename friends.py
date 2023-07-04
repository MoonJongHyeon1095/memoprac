from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import certifi
from bson import ObjectId

# .env 파일 로드
load_dotenv()

ca = certifi.where()

# 환경 변수 사용
mongodb_url = os.getenv('MONGODB_URL')
# MongoDB 연결
client = MongoClient(mongodb_url, tlsCAFile=ca)
db = client["friends"]  # 클러스터안의 Database 이름
collection = db["friends"]  # Database 안의 컬렉션 이름

app = FastAPI()

# 친구 추가
@app.post('/friends')
def add_friend(name: str, phone_number: str):
    friend = {
        "name": name,
        "phone_number": phone_number
    }
    result = collection.insert_one(friend)
    print(f"Inserted friend : {result.inserted_id}")

# 친구 조회
@app.get('/friends')
def list_friends():
    friends = list(collection.find())
    # _id 값을 문자열로 변환
    for friend in friends:
        friend["_id"] = str(friend["_id"])
    print(friends)
    return JSONResponse({"friends": jsonable_encoder(friends)})

# 친구 삭제
@app.delete('/friends')
def delete_friend(friend_id):
    collection.delete_one({"_id": friend_id})
    # ObjectId로 변환
    friend_id = ObjectId(friend_id)
    print('삭제할 objectId:', friend_id)
    result = collection.delete_one({"_id": friend_id})
    if result.deleted_count == 1:
        return {"message": "success"}
    else:
        return '그런 친구 없음'

# 이름으로 친구 검색
@app.get('/friends/{name}')
def search_friend_by_name(name: str):
    friends = list(collection.find({"name": name}))
    for friend in friends:
        friend["_id"] = str(friend["_id"])
    print(friends)
    return JSONResponse({"friends": jsonable_encoder(friends)})
