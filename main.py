from fastapi import FastAPI

from app.routers import auth, account, users, categories, products, cart

app = FastAPI()

app.include_router(auth.router)
app.include_router(account.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(cart.router)

app.include_router(products.router)
