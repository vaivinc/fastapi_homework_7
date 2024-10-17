from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field, field_validator, EmailStr
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    return RedirectResponse("/docs")


class User(BaseModel):
    name: str = Field(min_length=2)
    password: str = Field(min_length=2)
    surname: str = Field(min_length=2)
    email: EmailStr

    @field_validator("name", "surname")
    @classmethod
    def name_surname(cls, v: str):
        if not v.isalpha():
            raise ValueError("name or surname can only have letters")
        if len(v) < 2:
            raise ValueError("len of name or surname not have  2 letters")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("password must have minimum 8 letters")
        if not any(ch.isupper() for ch in v):
            raise ValueError("password must have one capital letter")
        if not any(ch.islower() for ch in v):
            raise ValueError("password must have one small letter")
        if all(ch.isalnum() for ch in v):
            raise ValueError("password must have one special character")
        if not any(ch.isdigit() for ch in v):
            raise ValueError("password must have one number")
        return v


@app.post("/register/")
async def register_user(user: User):
    return user


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
