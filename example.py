import brick_xlsx_generator as bg
import os

# xlsx path
document_filepath = r"PATH TO FILE"

# rdf model namespacing
PORTFOLIO = "example_portfolio"
BUILDING_NAME = "example_building"

# initialise converter
g = bg.Graph()
# process input file to generate graph model
g.process(document_filepath, PORTFOLIO, BUILDING_NAME)
# export graph model to TTL file
g.export()                          # export full model
g.export(export_mode="building")    # export buidling entities only