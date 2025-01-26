from fastapi import FastAPI, HTTPException, Header, Depends, Request
from fastapi.responses import RedirectResponse


app = FastAPI()
CODE = "123456"
vacancies = [
        {"id": "1", "title": "Vacancy 1"},
        {"id": "2", "title": "Vacancy 2"},
        {"id": "3", "title": "Vacancy 3"},
        {"id": "4", "title": "Vacancy 4"},
        {"id": "5", "title": "Vacancy 5"},
    ]


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

@app.get("/resumes/{resume_id}/similar_vacancies")
def get_similar_vacancies(request: Request, resume_id: str, page: int = 0, per_page: int = 10):
    token = request.headers.get("Authorization")
    if not token or token != "Bearer fake_token":
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    if resume_id != "12345":
        raise HTTPException(status_code=404, detail="Resume not found")

    

    return {"resume_id": resume_id, "items": vacancies[:per_page]}

@app.post("/negotiations")
async def create_negotiation(request: Request, resume_id: int, vacancy_id: int, message: str):
    token = request.headers.get("Authorization")
    
    if not token or token != "Bearer fake_token":
        raise HTTPException(status_code=401, detail="Invalid or missing token")

    return {"resume_id": resume_id, "vacancy_id": vacancy_id, "message": message}