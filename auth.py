from fastapi import FastAPI, HTTPException, Header, Depends, Request
from fastapi.responses import RedirectResponse

app = FastAPI()
CODE = "123456"

# Функция для авторизации
@app.get("/authorize")
async def authorize_user(response_type: str, client_id: str, state: str, redirect_uri: str):
    
    redirect_url = f"{redirect_uri}?code={CODE}&state={state}"
    return RedirectResponse(url=redirect_url)

@app.get("/resumes/mine")
async def get_resume_id(request: Request):
    authorization = request.headers.get("Authorization")
    
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or incorrect")
    
    token = authorization.split(" ")[1]
    
    if token != CODE:
        raise HTTPException(status_code=403, detail="Invalid or expired token")
    
    return {"resume_id": 123456}