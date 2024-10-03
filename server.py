from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from MachineTranslate.textTranslate import translate_text
from MachineTranslate import docxTranslate, pdfTranslate, excelTranslate, pptxTranslate
import shutil
import os


app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from your React app
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],
)


#-------------------------------------------KDS_Machinetranslate---------------------------------------------------

# Example route for text generation
@app.post("/machineTranslate/translate-text")
async def generate_text(request: dict):
    text = request.get("text") if request.get("text") else request.get("q")
    source_lang = request.get("source_lang") if request.get("source_lang") else request.get("source")
    target_lang = request.get("target_lang") if request.get("target_lang") else request.get("target")
    result = translate_text(text, source_lang, target_lang)
    print("source_lang", source_lang, "text", text, "target_lang", target_lang)
    # return {"message": f"Text received: {result}"}
    return {"translatedText": result}

#Translate Document(pdf,doc)
@app.post("/machineTranslate/translate-doc")
async def translate_doc(
        file: UploadFile = File(...), 
        source_lang: str = Form(...),  # Use Form to get it from form data
        target_lang: str = Form(...)     # Use Form to get it from form data):
    ):

    #Save file
    file_location = f"./{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)



    #Translate Docx File
    if file.filename.endswith('.docx'):
        # docxTranslate.doc()
        translated_file_path = docxTranslate.translate_docx(file_location, source_lang, target_lang)
        if os.path.exists(translated_file_path):
            headers = {"Content-Disposition": "attachment; filename=translated_doc.docx"}
            return FileResponse(translated_file_path, media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document', headers=headers)
    
    # Translate PDF File
    elif file.filename.endswith('.pdf'):
        translated_file_path = pdfTranslate.translate_pdf(file_location, source_lang, target_lang)

    # Translate PDF File
    elif file.filename.endswith('.xlsx'):
        translated_file_path = excelTranslate.translate_excel(file_location, source_lang, target_lang)
        headers = {"Content-Disposition": "attachment; filename=translated_excel.xlsx"}
        return FileResponse(translated_file_path, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', headers=headers)

    elif file.filename.endswith('.pptx'):
        translated_file_path = pptxTranslate.translate_pptx(file_location, source_lang, target_lang)
        # headers = {"Content-Disposition": "attachment; filename=translated_excel.xlsx"}
        # return FileResponse(translated_file_path, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', headers=headers)

#-----------------------------------------------------------KDS_END------------------------------------------------------------------------------------------------