def get_recommendation(category):

    recommendations = {

        "Roads":
        """Based on the reported issue, the affected road section should be inspected by the maintenance department.
        Repair work is recommended to prevent accidents and ensure smooth traffic movement.
        Priority should be given to heavily damaged areas to improve public safety.""",

        "Water":
        """Technical staff should inspect the water supply infrastructure for possible leaks or disruptions.
        Necessary repairs should be carried out to restore normal water supply.
        Preventive measures are recommended to minimize future interruptions.""",

        "Electricity":
        """Electrical maintenance personnel should investigate the reported issue.
        Immediate attention is advised to ensure public safety and restore uninterrupted power supply.
        The affected infrastructure should be monitored after repair work is completed.""",

        "Drainage":
        """The drainage system should be inspected for leaks or blockages.
        Necessary cleaning and repair work are recommended to avoid water accumulation and health hazards.
        Maintenance personnel should monitor the affected area after restoration.""",

        "Sanitation":
        """Immediate waste collection and cleaning operations are recommended.
        Proper disposal should be carried out to maintain hygiene and prevent unpleasant odors.
        The affected area should be inspected after cleaning to ensure cleanliness."""
    }

    return recommendations.get(
        category,
        "No recommendation available."
    )