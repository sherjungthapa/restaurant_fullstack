from datetime import datetime

def current_time(request):
    return {"date":datetime.now()}