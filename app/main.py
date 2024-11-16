import os
from dotenv import load_dotenv
from fastapi import FastAPI
from app.routers import user, auth
from app.services.user_service import create_admin_user
# from app.middlewares.auth import RoleMiddleware


# Load environment variables
load_dotenv()  # This loads the .env file
app = FastAPI()

# add middleware
# app.add_middleware(RoleMiddleware)

# include routers
app.include_router(auth.auth_router, prefix="/auth", tags=["auth"])
app.include_router(user.user_router, prefix="/users", tags=["users"])


@app.on_event("startup")
async def on_startup():
    from app.core.db import init_db
    await init_db()  # Initialize the database
    
    # Check if admin user exists and create if not
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")
    if admin_email and admin_password:
        await create_admin_user(admin_email, admin_password)
    else:
        print("Admin credentials are not set in .env file")