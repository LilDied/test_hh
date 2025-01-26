from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

app = FastAPI()


# Функция для авторизации
@app.get("/authorize")
def authorize_user(response_type: str, client_id: str, state: str, redirect_uri: str):
    code = "123456"  

    redirect_url = f"{redirect_uri}?code={code}&state={state}"
    return RedirectResponse(url=redirect_url)