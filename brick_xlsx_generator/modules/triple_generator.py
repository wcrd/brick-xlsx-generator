import rdflib 
from . import helpers


# Create rdf triples from input dataframes (locations and equipment)
def process_df(df, namespaces:dict, multiIndexHeader:str, relationships_to_process:list):
    print(f"Processing {multiIndexHeader} relationships.")
    triples = []
    
    # validate input df has a valid identifier column (this is used for entity definition).
    # Df must have this column
    if helpers.validate_relationships(df['Brick'].columns, [("identifier", "Literal", "")]) == []:
        print("No valid identifier column found. Aborting.")
        return

    # validate input df has all relationships
    relationships = helpers.validate_relationships(df[multiIndexHeader].columns, relationships_to_process)

    for idx, row in df.iterrows():

        # set identifier name & class
        identifier = helpers.format_fragment(row['Brick']['identifier'])
        entity_class = helpers.format_fragment(row['Brick']['class'])

        # define entity
        if entity_class == 0:
            continue
        elif "switch:" in entity_class:
            triples.append((namespaces['building'][identifier], rdflib.RDF.type, namespaces['switch'][entity_class.replace("switch:", "")]))
        else:
            triples.append((namespaces['building'][identifier], rdflib.RDF.type, namespaces['brick'][entity_class]))

        for relationship in relationships:
            # prepare data
        
            data = row[multiIndexHeader][relationship.name]
            if data == 0 or data == "" or not data: continue
            data = [x.strip() for x in data.split("|")]

            if relationship.datatype == "Literal":
                for item in data:
                    triples.append( (namespaces['building'][identifier], namespaces[relationship.namespace][relationship.name], rdflib.Literal( item )) )
            elif relationship.datatype == "brick":
                for item in data:
                    if "switch:" in item:
                        # target is from switch namespace
                        triples.append((namespaces['building'][identifier], namespaces[relationship.namespace][relationship.name], namespaces["switch"][helpers.format_fragment(item.replace("switch:", ""))]))
                    else:
                        # continue as normal
                        triples.append((namespaces['building'][identifier], namespaces[relationship.namespace][relationship.name], namespaces[relationship.datatype][helpers.format_fragment(item)]))
            else:
                for item in data:
                    triples.append((namespaces['building'][identifier], namespaces[relationship.namespace][relationship.name], namespaces[relationship.datatype][helpers.format_fragment(item)]))

    return triples
