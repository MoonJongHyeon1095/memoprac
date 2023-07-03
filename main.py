from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

class Memo(BaseModel):
    id:str
    content:str

memos = []

app = FastAPI()


@app.post("/memos")
def create_memo(memo:Memo):
    memos.append(memo)
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
        sorted_memos = memos.copy()
    
    #key=lambda x: getattr(x, sort_by)에서 lambda x는 람다 함수를 정의하는 구문입니다. 
    #여기서 x는 sorted_memos 리스트의 각 요소를 의미하게 됩니다. 
    #따라서, key 함수는 정렬할 때 sorted_memos의 각 요소를 x로 받아와서 해당 요소의 sort_by로 지정된 속성 값을 가져오게 됩니다.
        if sorted and sort_by:
            if sort_by in Memo.__fields__:
                sorted_memos.sort(key=lambda x: getattr(x, sort_by))
                if sorted.upper() == "DESC":
                    sorted_memos.reverse()
        
        return sorted_memos

@app.put("/memos/{memo_id}")
def put_memo(req:Memo):
    print(req)
    for m in memos:
        if m.id == req.id:
            m.content = req.content
            return 'success'
    return '그런 메모 없음'

@app.delete("/memos/{memo_id}")
def delete_memo(memo_id):
    #enumerate 로 감싸야 index와 요소를 같이 뽑아준다.
    for index, memo in enumerate(memos):
        if memo.id==memo_id:
            memos.pop(index)
            return 'success'
    return '그런 메모 없음'

app.mount('/', StaticFiles(directory='static', html=True), name='static')
