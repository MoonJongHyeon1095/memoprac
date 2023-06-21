from fastapi import FastAPI
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

@app.get("/memos")
def read_momo():
    return memos

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
