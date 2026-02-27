import mimetypes
import os

# Расширения и соответствующие им MIME-типы (приоритетные)
CUSTOM_MIMETYPES = {
    '.py':   'text/x-python',
    '.java': 'text/x-java',
    '.c':    'text/x-c',
    '.cpp':  'text/x-c++',
    '.html': 'text/html',          
    '.htm':  'text/html',
    '.js':   'text/x-javascript',  
    '.json': 'text/x-json',
    '.xml':  'text/xml',      
    '.ini':  'text/x-ini',
    '.md':   'text/markdown',
    '.css':  'text/css',
    '.ico':  'image/x-icon',
}

def guess_mimetype(filename: str) -> str:
    """
    Определяет MIME-тип файла по его имени.
    Сначала проверяет расширение по словарю CUSTOM_MIMETYPES,
    затем использует mimetypes.guess_type().
    В случае неудачи возвращает 'application/octet-stream'.
    """
    # Получаем расширение файла (в нижнем регистре)
    _, ext = os.path.splitext(filename)
    ext = ext.lower()

    # 1. Проверка по пользовательскому словарю
    if ext in CUSTOM_MIMETYPES:
        return CUSTOM_MIMETYPES[ext]

    # 2. Стандартное определение через mimetypes
    mime_type, _ = mimetypes.guess_type(filename)
    if mime_type:
        return mime_type

    # 3. Резервный тип
    return 'application/octet-stream'