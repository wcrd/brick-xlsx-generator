# XLSX Brick Model Generator

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
g.process(path_to_xlsx, portfolio_name (optional), buidling_name (optional))
```
This will generate all brick relationships and process any SwitchTags provided.

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