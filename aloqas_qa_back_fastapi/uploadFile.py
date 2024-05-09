import chardet
from fastapi import UploadFile, HTTPException
from io import BytesIO
from docx import Document
import PyPDF2

async def file_to_text(file: UploadFile):
    file_extension = file.filename.split('.')[-1].lower()
    # Fait 
    if file_extension == 'csv':
            csv_data = await file.read()
            encoding = chardet.detect(csv_data)['encoding']
            try:
                decoded_data = csv_data.decode(encoding)
                return decoded_data
            except UnicodeDecodeError:
                raise HTTPException(status_code=400, detail="Le fichier CSV contient des caractères qui ne peuvent pas être décodés.")

    # Fait 
    elif file_extension == 'json':
        json_data = await file.read()
        return json_data.decode()

    # Fait 
    elif file_extension == 'docx':
        doc_data = await file.read()
        # Utilisez un flux mémoire pour passer les données au Document
        doc_stream = BytesIO(doc_data)
        doc = Document(doc_stream)
        doc_text = [paragraph.text for paragraph in doc.paragraphs]
        return '\n'.join(doc_text)
    
    # Fait 
    elif file_extension == 'txt':
        txt_data = await file.read()
        return txt_data.decode()
    
    # Fait 
    elif file_extension == 'pdf':
        try:
            pdf_data = await file.read()
            # Chargez les données binaires dans un objet fitz.Document
            pdf_document = PyPDF2.PdfReader(BytesIO(pdf_data))
            text = ""
            for page_number in range(len(pdf_document.pages)):
                text += pdf_document.pages[page_number].extract_text()
            return text
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erreur de lecture du fichier PDF : {e}")

    else:
        return HTTPException(status_code=400, detail="Format de fichier non pris en charge")