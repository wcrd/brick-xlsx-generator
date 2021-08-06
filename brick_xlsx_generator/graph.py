import rdflib
import logging
import os.path
import pkgutil
import io
import pandas as pd
from datetime import datetime
from .relationships import (
    BRICK_RELATIONSHIPS,
    SWITCH_RELATIONSHIPS
)
from .modules import helpers, triple_generator as tg, sparql_queries as sq

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Graph(rdflib.Graph):
    def __init__(self, load_brick: bool = True, load_switch: bool = True, brick_version: str = "1.2", switch_version: str = "1.1"):
        self._ontology_versions = {
            'brick_version': brick_version,
            'switch_version': switch_version
        }
        self._building = {}
        self._namespaces = {}
        super().__init__()

        if load_brick:
            # get ontology data from package
            data = pkgutil.get_data(
                __name__, f"ontologies/Brick/{brick_version}/Brick.ttl"
            ).decode()
            # wrap in StringIO to make it file-like
            self.parse(source=io.StringIO(data), format="turtle")

        if load_switch:
            # get ontology data from package
            data = pkgutil.get_data(
                __name__, f"ontologies/Switch/{switch_version}/Brick-SwitchExtension.ttl"
            ).decode()
            # wrap in StringIO to make it file-like
            self.parse(source=io.StringIO(data), format="turtle")

        self.generate_namespaces()

    def generate_namespaces(self):
        # generate callable Namespace objects from Graph
        namespaceURIs = dict(self.namespaces())
        # create namespace objects to make querying easier
        self._namespaces = {name: rdflib.Namespace(URI) for name, URI in namespaceURIs.items()}

    def load_ontology(self, ontology_name: str, ontology_version: str, path_to_ontology: str):
        # get ontology data from path
        if os.path.isfile(path_to_ontology):
            self.parse(path_to_ontology, format=rdflib.util.guess_format(path_to_ontology))
            self._ontology_versions[ontology_name] = ontology_version
        else:
            logger.error(f"File not found at specified path: {path_to_ontology}")

    def process(self, path_to_xlsx: str, portfolio_name: str = "example", building_name: str = "example_building"):
        if not os.path.isfile(path_to_xlsx):
            logger.error(f"File not found at specified path: {path_to_xlsx}")
            return

        logger.info("Loading file...")
        # load sheets for: Locations, Equipment, Points
        xlFile = pd.ExcelFile(path_to_xlsx)
        df_locations = pd.read_excel(xlFile, sheet_name="locations", header=[0, 1], dtype=str)
        df_equipment = pd.read_excel(xlFile, sheet_name="equipment", header=[0, 1], dtype=str)
        df_points = pd.read_excel(xlFile, sheet_name="points", header=[0, 1], dtype=str)

        # tidy dfs
        logger.info("Clearing nulls.")
        df_locations.fillna(0, inplace=True)
        df_equipment.fillna(0, inplace=True)
        df_points.fillna(0, inplace=True)
        logger.info("Removing non-valid chars.")
        df_locations.replace({u'\xa0': u' '}, regex=True, inplace=True)
        df_equipment.replace({u'\xa0': u' '}, regex=True, inplace=True)
        df_points.replace({u'\xa0': u' '}, regex=True, inplace=True)

        logger.info("File load completed.")

        # NAMESPACES
        logger.info("Generating building namespace...")
        BUILDING = rdflib.Namespace(f"https://{portfolio_name}.com/{building_name}#")
        self._namespaces['building'] = BUILDING
        self.bind('building', BUILDING)
        self._namespaces['ref'] = BUILDING  # used for relative relationship references
        META = rdflib.Namespace("https://meta.com#") # temporary namespace to hold the metadata items that are used for tags. TODO: Update this.
        self._namespaces['meta'] = META
        self.bind('meta', META)
        self._building = {
            'portfolio': portfolio_name,
            'building': building_name
        }
        logger.info("Namespace generation complete.")

        # PROCESS EXCEL DATA & GENERATE TRIPLES
        logger.info("Processing Building Model data...")
        logger.info("Processing Locations...")
        triples_locations = tg.process_df(df_locations, self._namespaces, "Brick", BRICK_RELATIONSHIPS)
        triples_locations.extend(tg.process_df(df_locations, self._namespaces, "Switch", SWITCH_RELATIONSHIPS))

        logger.info("Processing Equipment...")
        triples_equipment = tg.process_df(df_equipment, self._namespaces, "Brick", BRICK_RELATIONSHIPS)
        triples_equipment.extend(tg.process_df(df_equipment, self._namespaces, "Switch", SWITCH_RELATIONSHIPS))

        logger.info("Processing Points...")
        triples_points = tg.process_df(df_points, self._namespaces, "Brick", BRICK_RELATIONSHIPS)
        triples_points.extend(tg.process_df(df_points, self._namespaces, "Switch", SWITCH_RELATIONSHIPS))
        logger.info("Building model data successfully processed.")

        # ADD TRIPLES TO GRAPH
        logger.info("Adding Entities to model...")
        for triple in [*triples_locations, *triples_equipment, *triples_points]:
            self.add(triple)
        logger.info(f"{len(triples_locations)} location triples added.")
        logger.info(f"{len(triples_equipment)} equipment triples added.")
        logger.info(f"{len(triples_points)} point triples added.")

        logger.info("Generating inverse relationships...")
        self.update(sq.generate_inverse_relationships())

        # Process Extensions
        logger.info("Processing model extensions.")
        # SwitchTags
        logger.info("Processing SwitchTags")
        logger.info("Processing Equipment tags")
        tg.process_tags(self, df_equipment, self._namespaces)
        logger.info("Processing Location tags")
        tg.process_tags(self, df_locations, self._namespaces)
        logger.info("Processing Point tags")
        tg.process_tags(self, df_points, self._namespaces)

        logger.info("Entities successfully added to model.")
        logger.info("Processing complete.")

    def export(self, export_mode: str = "full", export_path: str = os.path.join(os.getcwd(), "output")):
        """
        Serialises a graph model to a TTL file and saves to given path
        Can generate a full, building entity only, or building equipment only model.

        :param export_path: dir to save ttl file. Defaults to CWD/output.
        :param export_mode: options = ["full", "building", "equipment_locations_systems"]
        :return:
        """
        # check path is OK
        if not os.path.exists(export_path):
            os.mkdir(export_path)

        # GENERATE TIMESTAMP FOR FILENAMES
        now = datetime.now()
        timestamp_str = now.strftime("%Y%m%d_%H%M%S")

        if export_mode == "full":
            logger.info("Exporting full brick model...")
            filename = f"{timestamp_str}_M_{self._building['portfolio']}_{self._building['building']}.ttl"
            self.serialize(os.path.join(export_path, filename), format='turtle')
            logger.info(f"Export complete. See file: {filename}")

        elif export_mode == "building":
            logger.info("Exporting building entities only brick model...")

            logger.info("Generating new graph...")
            g = rdflib.Graph()
            g.bind("brick", self._namespaces['brick'])
            g.bind("building", self._namespaces['building'])
            g.bind("switch", self._namespaces['switch'])

            for item in self.query(sq.query_all_triples_in_namespace(), initBindings={'namespace': self._namespaces['building']}):
                g.add(item)

            logger.info("Exporting graph...")
            filename = f"{timestamp_str}_B_{self._building['portfolio']}_{self._building['building']}.ttl"
            g.serialize(os.path.join(export_path, filename), format='turtle')
            logger.info(f"Export complete. See file: {filename}")

        elif export_mode == "equipment_locations_systems":
            logger.info("Exporting equipment, location, system entities brick model...")

            logger.info("Generating new graph...(this can take a few minutes)")
            g = rdflib.Graph()
            g.bind("brick", self._namespaces['brick'])
            g.bind("building", self._namespaces['building'])
            g.bind("switch", self._namespaces['switch'])
            for item in self.query(sq.query_equipment_and_location_triples_in_namespace(self._namespaces), initBindings={'namespace': self._namespaces['building']}):
                g.add(item)

            logger.info("Exporting graph...")
            filename = f"{timestamp_str}_B_{self._building['portfolio']}_{self._building['building']}_noPoints.ttl"
            g.serialize(os.path.join(export_path, filename), format='turtle')
            logger.info(f"Export complete. See file: {filename}")
        else:
            logger.info(f"Provided export mode: {export_mode} is not supported.")

    def test(self):
        print(os.getcwd())
        return os.getcwd()


