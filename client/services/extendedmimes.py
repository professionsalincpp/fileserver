import mimetypes

def guess_mimetype(filename):
    if filename.endswith('.cpp'):
        return 'text/x-c++'
    if filename.endswith('.c'):
        return 'text/x-c'
    if filename.endswith('.java'):
        return 'text/x-java'
    if filename.endswith('.py'):
        return 'text/x-python'
    if filename.endswith('.html'):
        if filename.endswith('.htm'):
            return 'text/html'
        else:
            return 'text/x-html'
    if filename.endswith('.js'):
        return 'text/x-javascript'
    if filename.endswith('.css'):
        return 'text/css'
    if filename.endswith('.json'):
        return 'text/x-json'
    if filename.endswith('.xml'):
        return 'text/xml'
    if filename.endswith('.ini'):
        return 'text/x-ini'
    if filename.endswith('.md'):
        return 'text/x-markdown'
    # print(f"Unknown file type: {filename}. Guessing type with mimetypes.guess_type: {mimetypes.guess_type(filename)[0]}")
    
    return mimetypes.guess_type(filename)[0]