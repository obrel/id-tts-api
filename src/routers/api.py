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
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Text must be more than 10 characters."
            )

        if len(data["text"]) > 200:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Text must be less than 200 characters."
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Missing text field."
        )

    if "audio_type" in data:
        audio_type = data["audio_type"]

        if audio_type not in ["wibowo", "ardi", "gadis", "JV-00264", "SU-00060"]:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid audio type."
            )
    else:
        audio_type = "wibowo"

    response = TTSService.get_response(data["text"], audio_type)

    if response != "":
        try:
            with open(response, "rb") as audio_file:
                audio_bytes = audio_file.read()

            encoded_audio = base64.b64encode(audio_bytes).decode("utf-8")
            audio_format = "wav"
            data_uri = f"data:audio/{audio_format};base64,{encoded_audio}"

            return JSONResponse(content={"audio_data": data_uri})
        except FileNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found."
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error."
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error."
        )
