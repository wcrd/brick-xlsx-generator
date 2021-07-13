from collections import namedtuple

# Define relationships of interest for this model
Rel = namedtuple("Rel", ['name', 'datatype', 'namespace'])

# Switch Relationships of interest
SWITCH_RELATIONSHIPS = [
    Rel("hasObjectPropertyId", "Literal", "switch")
    # Rel("hasLocationUuid", "Literal", "switch"),
    # Rel("locationLabel", "Literal", "switch"),
    # Rel("locationType", "Literal", "switch"),
    # Rel("locationDisplayName", "Literal", "switch"),
    # Rel("locationNumber", "Literal", "switch"),
    # Rel("locationDescription", "Literal", "switch"),
    # Rel("floorNum", "Literal", "switch"),
    # Rel("hasEquipmentUuid", "Literal", "switch"),
    # Rel("equipmentLabel", "Literal", "switch"),
    # Rel("equipmentType", "Literal", "switch"),
    # Rel("equipmentDisplayName", "Literal", "switch"),
    # Rel("hasSensorUuid", "Literal", "switch"),
    # Rel("pointName", "Literal", "switch"),
    # Rel("sensorDisplayName", "Literal", "switch"),
]

# Brick Relationships of interest (relationships, datatype (if not reference), namespace (if not brick))
BRICK_RELATIONSHIPS = [
    Rel("label", "Literal", "rdfs"),
    Rel("hasUuid", "Literal", "brick"),
    Rel("feeds", "ref", "brick"),
    Rel("isFedBy", "ref", "brick"),
    Rel("hasPart", "ref", "brick"),
    Rel("isPartOf", "ref", "brick"),
    Rel("hasLocation", "ref", "brick"),
    Rel("isLocationOf", "ref", "brick"),
    Rel("hasInputSubstance", "brick", "brick"),
    Rel("hasOutputSubstance", "brick", "brick"),
    Rel("hasUnit", "Literal", "brick"),
    Rel("isPointOf", "ref", "brick")
]
