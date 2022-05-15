# brick-xlsx-generator
A tool that takes a template XLSX file (included) and converts it into a Brick TTL model file.

## Installation
Create a new environment and install from github:

 ```
 poetry add git+https://github.com/wcrd/brick-xlsx-generator.git@main
 ```
 In your working file simply import the package

 ```python
 import brick_xlsx_generator as bg
 ```
An example working file is provide as 'example.py'.

## Dependencies
If you need to install dependencies run 
```buildoutcfg
poetry install
```
(you will need [Poetry](https://python-poetry.org/docs/) installed)

## Usage
1. Intitialize converter as an empty Graph
```python
g = bg.Graph()
```
This will automatically load Brick and Switch ontologies. You can pass in custom versions if you need to.

2. Process the xlsx input file to generate a populated graph model
```python
g.process(path_to_xlsx)
```
This will generate all brick relationships and process any Switch Relationships and Tags provided. See the Switch Brick Extension included to learn more.

The `process()` function can take a number of additional parameters:
```python
process(self, path_to_xlsx: str, portfolio_name: str = "example", building_name: str = "example_building", relationship_field:tuple = ("Brick", "identifier"))
```
`portfolio_name` & `building_name` define the URI components that the building entities will be created under. The building URI takes the form: `https://{portfolio_name}.com/{building_name}#` with a default prefix of `building`.\
`relationship_field`: the field in the template which entities reference each other by. In a Brick model this would always be the 'subject' field, however some flexibility is allowed for in the spreadsheet based definition, allowing entities to reference each other by 'label' rather than a uuid, for example.

3. Export Model to TTL
```python
g.export(export_mode="full")  # export_mode is optional
```
Export options available are:
* _full_: export everything
* _building_: export only building entities
* _equipment_locations_systems_: export only building entities and exclude points

## References
Parts of this code are based on code provided by the py-brickschema package.