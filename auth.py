from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class AuthRequest(BaseModel):
    grant_type: str
    username: str = None
    password: str = None
    client_id: str = None
    client_secret: str = None


fake_user_db = {
    "test_user": {
        "password": "123456",
        "client_id": "my_app_id",
        "client_secret": "my_secret"
    }
}


@app.post("/authorize")
def authorize_user(auth_data: AuthRequest):
    # Проверка на отсутствие обязательных полей
    if not auth_data.grant_type:
        raise HTTPException(status_code=400, detail="grant_type обязателен")
    
    if auth_data.grant_type == "password":
        if not auth_data.username or not auth_data.password:
            raise HTTPException(status_code=400, detail="Для password-авторизации необходимо указать username и password")
        
        user = fake_user_db.get(auth_data.username)
        if not user or user["password"] != auth_data.password:
            raise HTTPException(status_code=401, detail="Неверные логин или пароль")
        return {"access_token": "fake_token_123", "token_type": "bearer"}

    elif auth_data.grant_type == "client_credentials":
        if not auth_data.client_id or not auth_data.client_secret:
            raise HTTPException(status_code=400, detail="Для client_credentials необходимо указать client_id и client_secret")
        
        if auth_data.client_id == "my_app_id" and auth_data.client_secret == "my_secret":
            return {"access_token": "client_fake_token_456", "token_type": "bearer"}
        raise HTTPException(status_code=401, detail="Неверные client_id или client_secret")

    raise HTTPException(status_code=400, detail="Неверный grant_type")