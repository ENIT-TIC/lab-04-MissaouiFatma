import requests

BASE = "http://localhost:5000"

print(">> Adding book...")
r = requests.post(BASE + "/books", json={
    "title": "Test Book",
    "author": "Author X",
    "year": 2024
})
print("POST /books:", r.status_code, r.json())

print(">> Listing books...")
r = requests.get(BASE + "/books")
print("GET /books:", r.status_code)
print(r.json())

if len(r.json()) > 0:
    book_id = r.json()[0]["id"]
    print(">> Updating book id", book_id)
    r = requests.put(BASE + f"/books/{book_id}", json={
        "title": "Updated Title",
        "author": "Updated Author",
        "year": 2025
    })
    print("PUT /books/id:", r.status_code)

    print(">> Deleting book...")
    r = requests.delete(BASE + f"/books/{book_id}")
    print("DELETE /books/id:", r.status_code)

print(">> Final list:")
print(requests.get(BASE + "/books").json())
