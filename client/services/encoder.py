import base64

class Encoder:
    encodings_map = {
        "text/plain": "utf-8",
        "*/*": "utf-8",
             
        # Images
        "image/bmp": "base64",
        "image/png": "base64",
        "image/jpeg": "base64",
        "image/gif": "base64",
        "image/pdf": "base64",
        "image/tiff": "base64",
        "image/x-icon": "base64",
        "image/x-ms-bmp": "base64",
        "image/x-xbitmap": "base64",
        "image/x-xbm": "base64",
        "image/x-xpixmap": "base64",
        "image/x-xwindowdump": "base64",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "base64",
        "application/vnd.ms-excel": "base64",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "base64",
    }
    @classmethod
    def encode(cls, data: str, mimetype: str) -> bytes:
        encoding = cls.get_encoding(mimetype)
        if encoding == "base64":
            try:
                return base64.b64decode(data.encode("utf-8"))
            except Exception as e:
                return f"Error encoding base64 data: {e}".encode("utf-8")
        return data.encode(encoding, errors="replace")
    
    @classmethod
    def decode(cls, data: bytes, mimetype: str) -> str:
        encoding = cls.get_encoding(mimetype)
        if encoding == "base64":
            try:
                return base64.b64encode(data).decode("utf-8")
            except Exception as e:
                return f"Error decoding base64 data: {e}"
        decoded = data.decode(encoding, errors="replace")
        return decoded

    @classmethod
    def get_encoding(cls, mimetype: str) -> str:
        return cls.encodings_map.get(mimetype, "utf-8")