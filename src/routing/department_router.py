def get_department(category):

    departments = {
        "Roads": "Road Maintenance Department",
        "Water": "Water Supply Department",
        "Electricity": "Electricity Department",
        "Drainage": "Drainage Department",
        "Sanitation": "Sanitation Department"
    }

    return departments.get(
        category,
        "General Administration"
    )