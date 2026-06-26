from datetime import datetime


def generate_complaint_id(last_id):

    year = datetime.now().year

    return f"CMP{year}{last_id:04d}"