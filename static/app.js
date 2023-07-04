async function deleteMemo(event) {
  const id = event.target.dataset.id;

  const res = await fetch(`/memos/${id}`, {
    method: "DELETE",
  });
  readMemo();
}

async function editMemo(event) {
  const id = event.target.dataset.id;
  const editInput = prompt("수정 입력");

  const res = await fetch(`/memos/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id,
      content: editInput,
    }),
  });
  readMemo();
}

function displayMemos(memo) {
  const ul = document.querySelector("#memo-ul");
  const li = document.createElement("li");
  li.innerText = `[id: ${memo.id}]-----[content: ${memo.content}]`;

  const editBtn = document.createElement("button");
  editBtn.innerText = "수정";
  editBtn.addEventListener("click", editMemo);
  editBtn.dataset.id = memo._id;

  const delBtn = document.createElement("button");
  delBtn.innerText = "삭제";
  delBtn.addEventListener("click", deleteMemo);
  delBtn.dataset.id = memo._id;

  li.appendChild(editBtn);
  li.appendChild(delBtn);
  ul.appendChild(li);
}

async function readMemo() {
  const res = await fetch("/memos");
  const jsonRes = await res.json();
  const ul = document.querySelector("#memo-ul");
  ul.innerHTML = "";
  console.log(jsonRes.memos);
  jsonRes.memos.forEach((memo) => displayMemos(memo));
}

async function createMemo(value) {
  console.log(value);
  const res = await fetch("/memos", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    // mode: "no-cors",
    body: JSON.stringify({
      id: new Date().getTime(),
      content: value,
    }),
  });

  const jsonRes = await res.json();
  console.log(jsonRes);

  readMemo();
}

function handleSubmit(event) {
  event.preventDefault();
  const input = document.querySelector("#memo-input");
  createMemo(input.value);
  input.value = "";
}

const form = document.querySelector("#memo-form");
form.addEventListener("submit", handleSubmit);

readMemo();
