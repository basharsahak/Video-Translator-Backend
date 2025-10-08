from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import shutil
import os

app = FastAPI()

UPLOAD_DIR = Path("uploaded_videos")
UPLOAD_DIR.mkdir(exist_ok=True)

# Mount static files so uploaded videos are served at /uploaded_videos/{filename}
app.mount("/uploaded_videos", StaticFiles(directory=str(UPLOAD_DIR)), name="uploaded_videos")

@app.get("/")
def read_root():
    return {"message": "Hello Video Translator Backend!"}

@app.post("/upload-video/")
async def upload_video(
    request: Request,
    file: UploadFile = File(...),
    targetLang: str = Form(...)
):
    try:
        file_location = UPLOAD_DIR / file.filename
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)

        translated_languages = ["en", "zh", "fr"]
        base = str(request.base_url).rstrip("/")
        video_url = f"{base}/uploaded_videos/{file.filename}"

        return JSONResponse(
            status_code=200,
            content={
                "filename": file.filename,
                "saved_at": str(file_location),
                "available_translations": translated_languages,
                "video_url": video_url,
                "target_language": targetLang
            }
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# ⬇️ دا درې کرښې دلته په پای کې ورزیاته کړه ⬇️
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000, timeout_keep_alive=300)
