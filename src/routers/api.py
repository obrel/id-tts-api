from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import JSONResponse
from src.services.tts import TTSService
import base64

router = APIRouter()

@router.post("/speech")
async def generate_speech(request: Request):
    data = await request.json()

    if "text" in data:
        if len(data["text"]) < 10:
            return HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Text must be more than 10 characters."
            )

        if len(data["text"]) > 200:
            return HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Text must be less than 200 characters."
            )
    else:
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Missing text field."
        )

    response = TTSService.get_response(data["text"])

    if response != "":
        try:
            with open(response, "rb") as audio_file:
                audio_bytes = audio_file.read()

            encoded_audio = base64.b64encode(audio_bytes).decode("utf-8")
            audio_format = "wav" 
            data_uri = f"data:audio/{audio_format};base64,{encoded_audio}"

            return JSONResponse(content={"audio_data": data_uri})
        except FileNotFoundError:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found."
            )
        except Exception as e:
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error."
            )
    else:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error."
        )
