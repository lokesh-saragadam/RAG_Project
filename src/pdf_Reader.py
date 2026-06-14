from pypdf import PdfReader

def extract_pdf(paths:list):
    texts = []
    for path in paths:
        text = []
        reader = PdfReader(path)
        for page in reader.pages:
            text.append(page.extract_text(0))
        texts.append(text)
    return texts
