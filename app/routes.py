from fastapi import APIRouter, HTTPException
from app.schemas import ProcessRequest, ProcessResponse
from app.services.llm_service import generate_response
from app.utils.validator import validate_action
router = APIRouter()
@router.post("/process", response_model=ProcessResponse)
def process_text(request: ProcessRequest):
    try:
        action = request.action.strip().lower()
        text = request.text.strip()
        validate_action(action)
        print("ACTION:", action)
        result = generate_response(text, action)
        return ProcessResponse(result=result)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        print("ERROR:", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")
