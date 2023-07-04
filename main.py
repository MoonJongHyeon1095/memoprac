from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
import os
import certifi

# .env 파일 로드
load_dotenv()

ca = certifi.where()

# 환경 변수 사용
mongodb_url = os.getenv('MONGODB_URL')
# MongoDB 연결
client = MongoClient(mongodb_url, tlsCAFile=ca)
db = client["memo"]  # 클러스터안의 Database 이름
collection = db["memo"]  # Database 안의 컬렉션 이름

class Memo(BaseModel):
    id:str
    content:str

memos = []

app = FastAPI()


@app.post("/memos")
def create_memo(memo:Memo):
    datum = {
        "id": memo.id,
        "content": memo.content
    }
    result = collection.insert_one(datum)
    print(result.inserted_id)
    return 'success'

 # Query() FastAPI에서 제공하는 쿼리 매개변수의 유효성 검사 및 기본값을 설정하기 위한 도우미 함수
# Query 함수는 여러 가지 유효성 검사 기능을 제공합니다. 몇 가지 예시를 들면:
# 타입 변환: 쿼리 매개변수의 값을 원하는 타입으로 변환할 수 있습니다. 예를 들어, Query(int)는 쿼리 매개변수의 값을 정수형으로 변환합니다.
# 기본값 설정: 쿼리 매개변수에 기본값을 지정할 수 있습니다. 매개변수가 요청에 포함되지 않으면 기본값이 사용됩니다.
# 유효성 검사: 추가적인 제약 조건을 지정하여 쿼리 매개변수의 값이 유효한지 검사할 수 있습니다. 예를 들어, Query(..., gt=0)는 값을 0보다 큰 값으로 제한합니다.
@app.get("/memos")
def read_momo(sorted: str = Query(None, description="Sort order (ASC or DESC)"),
              sort_by: str = Query(None, description="Property to sort by (id, content, etc.)")):
        print('sorted:', sorted)
        print('sort_by:', sort_by)
        #sorted_memos = memos.copy()
        
        # MongoDB에서 데이터 조회
        memos = list(collection.find({}))
        
        # _id 값을 문자열로 변환
        for memo in memos:
            memo["_id"] = str(memo["_id"])
        print(memos)
        
    # #key=lambda x: getattr(x, sort_by)에서 lambda x는 람다 함수를 정의하는 구문입니다. 
    # #여기서 x는 sorted_memos 리스트의 각 요소를 의미하게 됩니다. 
    # #따라서, key 함수는 정렬할 때 sorted_memos의 각 요소를 x로 받아와서 해당 요소의 sort_by로 지정된 속성 값을 가져오게 됩니다.
        if sorted and sort_by:
            if sort_by == "id" or sort_by == "content":
                # memos.sort(key=lambda x: getattr(x, sort_by))
                memos.sort(key=lambda x: x[sort_by])
                if sorted.upper() == "DESC":
                    memos.reverse()
        
        return JSONResponse({"memos": jsonable_encoder(memos)})


            

@app.put("/memos/{memo_id}")
def put_memo(req:Memo, memo_id):
    # print(req)
    # for m in memos:
    #     if m.id == req.id:
    #         m.content = req.content
    #         return 'success'
    # return '그런 메모 없음'
    
    # ObjectId로 변환
    memo_id = ObjectId(memo_id)
    print('수정할 objectId:', memo_id)
    result = collection.find_one_and_update({"_id": memo_id}, {'$set': {'content': req.content}})
    if result is not None:
        return {"message": "success"}
    else:
        return '그런 메모 없음'

@app.delete("/memos/{memo_id}")
def delete_memo(memo_id):
    #enumerate 로 감싸야 index와 요소를 같이 뽑아준다.
    # for index, memo in enumerate(memos):
    #     if memo.id==memo_id:
    #         memos.pop(index)
    #         return 'success'
    # return '그런 메모 없음'
    
    # ObjectId로 변환
    memo_id = ObjectId(memo_id)
    print('삭제할 objectId:', memo_id)
    result = collection.delete_one({"_id": memo_id})
    if result.deleted_count == 1:
        return {"message": "success"}
    else:
        return '그런 메모 없음'

app.mount('/', StaticFiles(directory='static', html=True), name='static')
