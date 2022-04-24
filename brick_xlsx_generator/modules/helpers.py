import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Validate URIs
# TODO: Is there an official way to do this??
# RDF does not like whitespace or "/" in the URI fragment
def format_fragment(fragment):
    if isinstance(fragment, str):
        return fragment.replace(" ", "_").replace("/", "_")
    else:
        return fragment


# Validate relationships
# check pandas df has required relationships for brick model
def validate_relationships(df_headers, relationships_to_process):
    """
    Checks the pandas df has required relationships for brick model

    Params:
    df: pandas dataframe header (with relationships as column headers)
    relationships_to_process: list of tuples (relationship name, relationship datatype)
        * relationship datatype options: "", "Literal"
        * if the relationship datatype is "" then the type is assumed to be a reference to another object in the graph
    
    Returns: List of valid relationship tuples for given dataframe
    """
    relationships = []
    for relationship in relationships_to_process:
        if relationship[0] in df_headers:
            relationships.append(relationship)
        else:
            print(f"Input df does not have relationship: {relationship} defined.")
    
    return relationships

# Check column in dataframe
def column_exists(df_headers, column_name):
    return column_name in df_headers

# return first matched id by custom_field in dataframe map
# df_map must have columns subject, custom
def lookupValue(df_map, custom_value:str):
    try: 
        return df_map.loc[df_map.custom == custom_value]['subject'].values[0]
    except:
        logger.warning(f"Id not found for referenced entity: {custom_value}. Skipping.")
        return None