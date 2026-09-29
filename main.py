from fastapi import FastAPI

app = FastAPI()

@app.get("/items")
async def get_all_items():
    return {"items": ["item1", "item2", "item3"]}