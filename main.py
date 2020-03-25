import math


class NoFertility(Exception):
    pass


POPULATION_RESIDENCES = {"farmers": 10, "workers": 20,
                         "artisans": 30, "engineers": 40,
                         "investors": 50,
                         "explorers": 10, "technicians": 20,
                         "jornaleros": 10, "obreros": 20}


class ProductionBuilding:
    def __init__(self, name: str, consumers: dict = {}, requires: dict = {},
                 needs_fertility: str = None):
        """

        Args:
            name:
            consumers: number of consumers the building feeds
            requires:
        """
        self.needs_fertility = needs_fertility
        self.name = name
        for consumer in consumers.keys():
            assert consumer in POPULATION_RESIDENCES
        self.consumers = consumers
        self.requires = requires

    def has_requirements(self):
        if len(self.requires) > 0:
            return True
        else:
            return False


FISHERY = ProductionBuilding(name="fishery",
                             consumers={"farmers": 800, "workers": 800})
POTATO = ProductionBuilding(name="potato",
                            needs_fertility="potato")
SCHNAPPS = ProductionBuilding(name="schnapps",
                              consumers={"farmers": 600, "workers": 600,
                                         "explorers": 1333, "technicians": 1333},
                              requires={"potato": 1})
SHEEP = ProductionBuilding(name="sheep")
KNITTERS = ProductionBuilding(name="knitters",
                              consumers={"farmers": 650, "workers": 650},
                              requires={"sheep": 1})
PIG = ProductionBuilding(name="pig")
SLAUGHTERS = ProductionBuilding(name="slaughters",
                                consumers={"workers": 1000, "artisans": 750},
                                requires={"pig": 1})
GRAIN = ProductionBuilding(name="grain",
                           needs_fertility="grain")
FLOUR = ProductionBuilding(name="flour",
                           requires={"grain": 2})
BAKERY = ProductionBuilding(name="bakery",
                            requires={"flour": .5},
                            consumers={"workers": 2200 / 2, "artisans": 1650 / 2})
RENDERING = ProductionBuilding(name="rendering",
                               requires={"pig": 1})
SOAP = ProductionBuilding(name="soap",
                          requires={"rendering": 2},
                          consumers={"workers": 4800, "artisans": 3600})

LUMBERJACK = ProductionBuilding(name="lumberjack")
SAWMILL = ProductionBuilding(name="sawmill",
                             requires={"lumberjack": 1})
CLAY = ProductionBuilding(name="clay",
                          needs_fertility="clay")
BRICK = ProductionBuilding(name="brick",
                           requires={"clay": .5})
SAIL_MAKER = ProductionBuilding(name="sailmaker",
                                requires={"sheep": 1})
IRON_MINE = ProductionBuilding(name="iron_mine",
                               needs_fertility="iron_mine")
COAL_MINE = ProductionBuilding(name="coal_mine",
                               needs_fertility="coal_mine")
CHARCOAL_KILN = ProductionBuilding(name="charcoal_kiln")
FURNACE = ProductionBuilding(name="furnace",
                             requires={"charcoal_kiln": 1,
                                       "iron_mine": .5}
                             )
STEEL_WORKS = ProductionBuilding(name="steel_works",
                                 requires={"furnace": 2 / 3})
WEAPONS = ProductionBuilding(name="weapons",
                             requires={"furnace": 2 / 6})
HOPS = ProductionBuilding(name="hops",
                          needs_fertility="hops")
MALTHOUSE = ProductionBuilding(name="malthouse",
                               requires={"grain": 1 / 2})
BREWERY = ProductionBuilding(name="brewery",
                             consumers={"workers": 2600 / 2, "artisans": 1950 / 2, "obreros": 1500 / 2},
                             requires={"malthouse": 2 / 1,
                                       "hops": 3 / 2})
CATTLE = ProductionBuilding(name="cattle")
PEPPERS = ProductionBuilding(name="peppers",
                             needs_fertility="peppers")
KITCHEN = ProductionBuilding(name="kitchen",
                             requires={"cattle": 1, "peppers": 1})
CANNERY = ProductionBuilding(name="cannery",
                             requires={"kitchen": 8 / 6, "iron_mine": 1 / 6},
                             consumers={"artisans": 11700 / 6, "engineers": 7800 / 6, "technicians": 6666 / 6})
SAND = ProductionBuilding(name="sand")
GLASS = ProductionBuilding(name="glass",
                           requires={"sand": 1})
WINDOWS = ProductionBuilding(name="windows",
                             requires={"glass": 2 / 4, "lumberjack": 1 / 4})
SEWING_MACHINE = ProductionBuilding(name="sewing_machine",
                                    requires={"furnace": 1, "lumberjack": 1 / 2},
                                    consumers={"artisans": 4200 / 2, "engineers": 2800 / 2, "obreros": 3200 / 2})
COTTON_PLANTATION = ProductionBuilding(name="cotton_plantation",
                                       needs_fertility="cotton")
COTTON_MILL = ProductionBuilding(name="cotton_mill",
                                 requires={"cotton_plantation": 2 / 1})
HUNTING_CABIN = ProductionBuilding(name="hunting_cabin",
                                   needs_fertility="furs")
FUR_DEALER = ProductionBuilding(name="fur_dealer",
                                requires={"cotton_mill": 1, "hunting_cabin": 2 / 1},
                                consumers={"artisans": 2250, "engineers": 1500})
PLANTAIN = ProductionBuilding(name="plantain",
                              needs_fertility="plantain")
FISH_OIL = ProductionBuilding(name="fish_oil")
FRIED_PLANTAIN = ProductionBuilding(name="fried_plantain",
                                    requires={"plantain": 1, "fish_oil": 1},
                                    consumers={"jornaleros": 700, "obreros": 700})
SUGAR = ProductionBuilding(name="sugar",
                           needs_fertility="sugar")
RUM = ProductionBuilding(name="rum",
                         requires={"sugar": 1, "lumberjack": .5},
                         consumers={"jornaleros": 2800 / 2, "obreros": 2800 / 2,
                                    "artisans": 2100 / 2, "engineers": 1400 / 2})
ALPACA = ProductionBuilding(name="alpaca")
PONCHO = ProductionBuilding(name="poncho",
                            requires={"alpaca": 1},
                            consumers={"jornaleros": 800, "obreros": 800})
CORN = ProductionBuilding(name="corn",
                          needs_fertility="corn")
TORTILLA = ProductionBuilding(name="tortilla",
                              requires={"cattle": 2, "corn": 2},
                              consumers={"obreros": 1400})
COFFEE_PLANTATION = ProductionBuilding(name="coffee_plantation",
                                       needs_fertility="coffee")
COFFEE_ROASTER = ProductionBuilding(name="coffee_roaster",
                                    requires={"coffee_plantation": 2},
                                    consumers={"obreros": 3400, "engineers": 1700,
                                               "investors": 1062.5, "technicians": 1666})
MARQUETRY = ProductionBuilding(name="marquetry",
                               requires={"lumberjack": 1 / 4})
TOBACCO = ProductionBuilding(name="tobacco",
                             needs_fertility="tobacco")
CIGAR = ProductionBuilding(name="cigar",
                           requires={"tobacco": 8 / 2, "marquetry": 4 / 2},
                           consumers={"obreros": 7200, "investors": 9000})
FELT = ProductionBuilding(name="felt",
                          requires={"alpaca": 1})
BOMBIN = ProductionBuilding(name="bombin",
                            requires={"felt": 1, "cotton_mill": 1},
                            consumers={"obreros": 1500})
LIMESTONE = ProductionBuilding(name="limestone",
                               needs_fertility="limestone")
CONCRETE = ProductionBuilding(name="concrete",
                              requires={"furnace": 2/4, "limestone": 2/4})
COPPER = ProductionBuilding(name="copper",
                            needs_fertility="copper")
ZINC = ProductionBuilding(name="zinc",
                          needs_fertility="zinc")
BRASS = ProductionBuilding(name="brass",
                           requires={"copper": 1/2, "zinc": 1/2})
SPECTACLE = ProductionBuilding(name="spectacle",
                               requires={"brass": 2/3, "glass": 1/3},
                               consumers={"engineers": 9000/3, "investors": 5625/3})
SALTPETER = ProductionBuilding(name="saltpeter",
                               needs_fertility="saltpeter")
DYNAMITE = ProductionBuilding(name="dynamite",
                              requires={"rendering": 4/4, "saltpeter": 8/4})
HEAVY_WEAPONS = ProductionBuilding(name="heavy_weapons",
                                   requires={"furnace": 2/4, "dynamite": 4/4})
CAOUTCHOUC = ProductionBuilding(name="caoutchouc",
                                needs_fertility="caoutchouc")
PENNY_FARTHINGS = ProductionBuilding(name="penny_farthings",
                                     requires={"caoutchouc": 1/4, "furnace": 2/4},
                                     consumers={"engineers": 6400, "investors": 4000})
MOTORS = ProductionBuilding(name="motors",
                            requires={"furnace": 2/3, "brass": 4/3})

CONSUMABLES_BUILDINGS = {"fishery": FISHERY,
                         "potato": POTATO,
                         "schnapps": SCHNAPPS,
                         "sheep": SHEEP,
                         "knitters": KNITTERS,
                         "pig": PIG,
                         "slaughters": SLAUGHTERS,
                         "grain": GRAIN,
                         "flour": FLOUR,
                         "bakery": BAKERY,
                         "rendering": RENDERING,
                         "soap": SOAP,
                         "lumberjack": LUMBERJACK,
                         "clay": CLAY,
                         "iron_mine": IRON_MINE,
                         "coal_mine": COAL_MINE,
                         "charcoal_kiln": CHARCOAL_KILN,
                         "furnace": FURNACE,
                         "hops": HOPS,
                         "malthouse": MALTHOUSE,
                         "brewery": BREWERY,
                         "cattle": CATTLE,
                         "peppers": PEPPERS,
                         "kitchen": KITCHEN,
                         "cannery": CANNERY,
                         "sand": SAND,
                         "glass": GLASS,
                         "sewing_machine": SEWING_MACHINE,
                         "cotton_plantation": COTTON_PLANTATION,
                         "cotton_mill": COTTON_MILL,
                         "hunting_cabin": HUNTING_CABIN,
                         "fur_dealer": FUR_DEALER,
                         "plantain": PLANTAIN,
                         "fish_oil": FISH_OIL,
                         "fried_plantain": FRIED_PLANTAIN,
                         "sugar": SUGAR,
                         "rum": RUM,
                         "alpaca": ALPACA,
                         "poncho": PONCHO,
                         "corn": CORN,
                         "tortilla": TORTILLA,
                         "coffee_plantation": COFFEE_PLANTATION,
                         "coffee_roaster": COFFEE_ROASTER,
                         "marquetry": MARQUETRY,
                         "tobacco": TOBACCO,
                         "cigar": CIGAR,
                         "felt": FELT,
                         "bombin": BOMBIN,
                         "limestone": LIMESTONE,
                         "copper": COPPER,
                         "zinc": ZINC,
                         "brass": BRASS,
                         "saltpeter": SALTPETER,
                         "spectacle": SPECTACLE,
                         "dynamite": DYNAMITE,
                         # "caoutchouc": CAOUTCHOUC,
                         # "penny_farthings": PENNY_FARTHINGS
                         # "filament": FILAMENT
                         }


CONSTRUCTION_MATERIAL_BUILDINGS = {"sawmill": SAWMILL,
                                   "brick": BRICK,
                                   "sailmaker": SAIL_MAKER,
                                   "steel_works": STEEL_WORKS,
                                   "weapons": WEAPONS,
                                   "windows": WINDOWS,
                                   "concrete": CONCRETE,
                                   "heavy_weapons": HEAVY_WEAPONS,
                                   "motors": MOTORS}

ALL_BUILDINGS = {}
ALL_BUILDINGS.update(CONSUMABLES_BUILDINGS)
ALL_BUILDINGS.update(CONSTRUCTION_MATERIAL_BUILDINGS)


NATURAL_RESOURCES = ["coal_mine", "iron_mine", "clay", "copper", "oil", "gold", "zinc", "limestone",
                     "hops", "grain", "potato", "peppers", "furs", "saltpeter", "grapes",
                     "cotton", "plantain", "sugar", "corn", "coffee", "caoutchouc", "tobacco", "cocoa"]


class Island:
    def __init__(self, name: str, world: set(),
                 fertility: dict = {}, electrified_buildings: dict = {}, exports: dict = {}):
        """

        Args:
            name: name of island
            fertility: resources on island if present
                dict value is maximum number of consumers - None if unlimited
            exports: list of buildings it will export the resources from, if requested
                will not export if doesnt have fertility cap
        """
        self.electrified_buildings = electrified_buildings
        self.world = world
        self.world.add(self)
        self.name = name
        for item in fertility:
            try:
                assert item in NATURAL_RESOURCES
            except AssertionError:
                raise AssertionError(f"{item} not in {NATURAL_RESOURCES}.")
            try:
                assert fertility[item] >= 0
            except TypeError:
                assert fertility[item] is None
        self.fertility = fertility
        self.exports = exports
        for export in self.exports:
            if export in self.fertility:  # if export requires fertility
                if self.fertility[export] is not None:  # if it has a limit
                    if self.exports[export] is None:
                        raise AssertionError(f"Cant export unlimited {export}, as this island only has {self.fertility[export]} of them")
                    else:
                        try:
                            assert self.exports[export] <= self.fertility[export]
                        except AssertionError:
                            raise AssertionError(
                                f"Cant export {export}, as it requires more fertility and this island only has {self.fertility[export]} of them")

        self.population = {}
        for pop in POPULATION_RESIDENCES:
            self.population[pop] = 0
        self.requested_construction_buildings = {}
        for building_type in CONSTRUCTION_MATERIAL_BUILDINGS:
            self.requested_construction_buildings[building_type] = 0

        self.required_buildings = {}
        self._reset_required_builings()
        self.exports_to = {}  # dict of what this island will export, and to where
        # "good": [number, "island"]

    def _reset_required_builings(self):
        self.required_buildings = {}
        for building in ALL_BUILDINGS:
            self.required_buildings[building] = 0

    def apply_item_modifier_percentage(self, type_pop_affected: str, number_buildings_affected: int, percentage_increase: int):
        assert type_pop_affected in POPULATION_RESIDENCES
        assert 100 >= percentage_increase >= 0
        self.population[type_pop_affected] += POPULATION_RESIDENCES[type_pop_affected] * number_buildings_affected * (percentage_increase / 100)

    def apply_item_modifier_absolute(self, type_pop_affected: str, number_buildings_affected: int, absolute_increase: int):
        raise NotImplemented

    def calculate_required_production_buildings(self) -> dict:
        """

        Returns: actual building numbers required
            (can be floats)

        """
        # self._reset_required_builings()
        # For each consumable building
        for building in CONSUMABLES_BUILDINGS.values():
            # for each consumer
            for consumer in building.consumers.keys():
                if self.population[consumer] == 0:
                    continue  # No need to do any calculations if no pop on this island
                number_required = self.population[consumer] / building.consumers[consumer]
                self.add_required_building(building_required=building.name, number_required=number_required * GLOBAL_CONSUMPTION_MODIFIER)

        # for each construction resource building
        for building in self.requested_construction_buildings:
            if 0 < (ammount_requested := self.requested_construction_buildings[building]):
                self.add_required_building(building, ammount_requested)

        # Special case - coal mines. Prefer coal mines if present
        if "coal_mine" in self.fertility:
            assert self.fertility["coal_mine"] is not None
            if self.fertility["coal_mine"] > 0:
                if self.fertility["coal_mine"] * 2 <= self.required_buildings["charcoal_kiln"]:  # if more kilns than can be replaced
                    self.required_buildings["coal_mine"] = self.fertility["coal_mine"]
                    self.required_buildings["charcoal_kiln"] -= 2 * self.required_buildings["coal_mine"]
                    assert self.required_buildings["charcoal_kiln"] >= 0
                else:  # If more coal mines than required
                    self.required_buildings["coal_mine"] = self.required_buildings["charcoal_kiln"] / 2
                    self.required_buildings["charcoal_kiln"] = 0

        self.modify_for_powered_buildings()

    def get_imported_good(self, building_required: str, number_required: float):
        for exporter_island in self.world:
            if exporter_island == self:
                continue  # Cant import from self
            if building_required in exporter_island.exports:
                try:
                    exporter_island.add_required_building(building_required, number_required)
                except NoFertility:  # Cant export from this island, not enough fertility left
                    continue
                # Add to exports list
                if building_required in exporter_island.exports_to:
                    # if island already exports that good
                    if self.name in exporter_island.exports_to[building_required]:
                        # and it has a trade route to the destination island]
                        exporter_island.exports_to[building_required][self.name] += number_required
                    else:
                        # but not to this island
                        exporter_island.exports_to[building_required][self.name] = number_required
                else:
                    # else add a new route
                    exporter_island.exports_to[building_required] = {self.name: number_required}
                # Building export has been added, return without raising an error
                return
        else:
            raise NoFertility(f"{building_required} is required on {self.name} and not exported in sufficient quantity from any exporter island.")

    def add_required_building(self, building_required: str, number_required: float):
        """
        Adds providers for required building, then adds required building itself

        Args:
            building_required: Building needed
            number_required:

        Returns: None
            raises NoFertiltiy error if not able to add required building

        """
        assert building_required in ALL_BUILDINGS.keys()
        assert number_required > 0

        # Check any requirements for fertility requirements
        required_ferts = do_producers_have_fert_requirements(building_name=building_required)
        for fert in required_ferts:  # Do we have the fertility
            if fert not in self.fertility:
                try:  # If we cant produce, try to import this good
                    self.get_imported_good(building_required=building_required, number_required=number_required)
                    return
                except NoFertility:
                    break  # Cant import this good, see if we can make here and import requirements
        # else we have all the required fertilises for producers, so produce locally

        # Add required providers
        for requirement_type in ALL_BUILDINGS[building_required].requires:
            number_provider_required = number_required * ALL_BUILDINGS[building_required].requires[requirement_type]
            self.add_required_building(requirement_type, number_provider_required)

        # If building has a fertility requirement
        needed_fertility = ALL_BUILDINGS[building_required].needs_fertility
        if needed_fertility is not None:
            if needed_fertility in self.fertility:  # If we have
                if self.fertility[needed_fertility] is not None:  # If there is a limit on fertility
                    if self.fertility[needed_fertility] < number_required:  # If we need more than island can provide
                        # Import the difference
                        extra_required = number_required - self.fertility[needed_fertility]
                        extra_required = math.ceil(extra_required*10)/10
                        assert extra_required > 0
                        self.get_imported_good(building_required, extra_required)
                        number_required -= extra_required
            else:  # None on this island, import all
                self.get_imported_good(building_required, number_required)
                return

        # Add these buildings to required (now we have all requirements)
        if needed_fertility is not None:
            if self.fertility[needed_fertility] is not None:  # If there is a limit on fertility
                self.fertility[needed_fertility] -= number_required
                assert self.fertility[needed_fertility] >= 0
        self.required_buildings[building_required] += number_required

    def required_residence_buildings(self) -> dict:
        results = {}
        for pop in self.population:
            results[pop] = math.ceil(self.population[pop] / POPULATION_RESIDENCES[pop])
        return results

    def display_required(self) -> None:

        print(f"****** {self.name} ******")
        # Round results up
        for building_name in self.required_buildings:
            self.required_buildings[building_name] = math.ceil(self.required_buildings[building_name])
        for building_name in self.exports_to:
            total_exported = 0
            for island_to in self.exports_to[building_name]:
                total_exported += self.exports_to[building_name][island_to]  # Double check we are not exporting more than production capacity
                self.exports_to[building_name][island_to] = math.ceil(self.exports_to[building_name][island_to])
            try:
                assert total_exported <= self.required_buildings[building_name]
            except AssertionError:
                raise AssertionError(
                    f"{self.name} is trying to export {total_exported} {building_name} but only produces {self.required_buildings[building_name]}")

        print("--- Required resource buildings ---")
        for item in self.required_buildings:
            if self.required_buildings[item] > 0:
                print(f"{item} : {self.required_buildings[item]}")
        res = self.required_residence_buildings()
        if len(self.exports_to) > 0:
            print("--- Trade routes ---")
            for item in self.exports_to:
                for island_to in self.exports_to[item]:
                    print(f"Export {self.exports_to[item][island_to]} {item} to {island_to}")

        print("--- Required residences ---")
        for item in res:
            if res[item] > 0:
                print(f"{item} : {res[item]}")
        print("\n")

    def modify_for_powered_buildings(self):
        for building in self.electrified_buildings:
            assert building in ALL_BUILDINGS
            assert self.electrified_buildings[building] > 0
            assert self.required_buildings[building] > 0
            self.required_buildings[building] -= self.electrified_buildings[building]
            if self.required_buildings[building] < 1:
                self.required_buildings[building] = 1  # Always need 1


def do_producers_have_fert_requirements(building_name: str) -> set:
    """
    Calculate any fertility requirements of the building given + and producers for it

    Args:
        building_name: building to calculate

    Returns: dict of fert requirements

    """
    assert building_name in ALL_BUILDINGS
    fert_requirements = set()

    for producer in ALL_BUILDINGS[building_name].requires:
        fert_requirements |= do_producers_have_fert_requirements(producer)

    if ALL_BUILDINGS[building_name].needs_fertility is not None:
        # If this building has a fert req, add it
        fert_requirements.add(ALL_BUILDINGS[building_name].needs_fertility)
    return fert_requirements


GLOBAL_CONSUMPTION_MODIFIER = .8 * 1.15  # Newspaper * newspaper prop modifier

if __name__ == "__main__":
    world = set()

    ditchwater = Island(name="Ditchwater", fertility={"grain": None, "potato": None, "peppers": None,
                                                      "iron_mine": 2, "coal_mine": 1, "clay": 3,
                                                      "zinc": 1, "copper": 1, "limestone": 2, "oil": 4},
                        exports={"schnapps": None, "brewery": None, "sewing_machine": None, "bakery": None},
                        world=world,
                        electrified_buildings={"steel_works": 2, "furnace": 5,
                                               "fur_dealer": 2, "sewing_machine": 2, "concrete": 2,
                                               "windows": 1, "iron_mine": 2, "coal_mine": 1,
                                               "spectacle": 1, "glass": 1, "brass": 1, "cannery": 1, "kitchen": 1})
    ditchwater.population["farmers"] = 16 * 10 * 10  # Blocks * houses in block * residents in house
    ditchwater.population["workers"] = 14 * 10 * 20
    ditchwater.population["artisans"] = 3 * 10 * 30
    ditchwater.population["engineers"] = 4 * 10 * 40
    # ditchwater.apply_item_modifier_percentage("farmers", , 20)
    ditchwater.apply_item_modifier_percentage("workers", 23, 20)
    ditchwater.apply_item_modifier_percentage("artisans", 23, 20)
    ditchwater.apply_item_modifier_percentage("engineers", number_buildings_affected=46, percentage_increase=20)

    ditchwater.requested_construction_buildings["sawmill"] = 2
    ditchwater.requested_construction_buildings["brick"] = 4
    ditchwater.requested_construction_buildings["sailmaker"] = 1
    ditchwater.requested_construction_buildings["steel_works"] = 1
    ditchwater.requested_construction_buildings["weapons"] = 1
    ditchwater.requested_construction_buildings["windows"] = 1
    ditchwater.requested_construction_buildings["concrete"] = 2
    ditchwater.requested_construction_buildings["heavy_weapons"] = 1
    ditchwater.requested_construction_buildings["motors"] = 1



    glanther = Island(name="Glanther", fertility={"potato": None, "hops": None, "saltpeter": None,
                                                  "iron_mine": 1, "coal_mine": 4, "copper": 1},
                      exports={"hops": None, "copper": 1, "saltpeter": None},
                      world=world)
    glanther.population["farmers"] = 6 * 10 * 10

    skidbjerg = Island(name="Skidbjerg", fertility={"hops": None, "peppers": None, "furs": None,
                                                    "clay": 1, "iron_mine": 2, "coal_mine": 2, "zinc": 2},
                       exports={"hunting_cabin": None,
                                "iron_mine": 2,
                                "zinc": 2
                                },
                       world=world)
    skidbjerg.population["farmers"] = 6 * 10 * 10
    skidbjerg.population["workers"] = 5 * 20 * 10
    skidbjerg.requested_construction_buildings["sawmill"] = 1
    skidbjerg.requested_construction_buildings["brick"] = 1

    # *** New world ***
    la_isla = Island(name="La Isla", fertility={"plantain": None, "sugar": None, "corn": None, "coffee": None,
                                                "clay": 3, "oil": 8, "gold": 2},
                     exports={"rum": None, "fried_plantain": None, "tortilla": None, "coffee_roaster": None},
                     world=world)
    la_isla.population["jornaleros"] = 7 * 10 * 10
    la_isla.population["obreros"] = 8 * 20 * 10
    la_isla.requested_construction_buildings["sawmill"] = 1
    la_isla.requested_construction_buildings["brick"] = 1

    fechiques = Island("Fechiques", fertility={"sugar": None, "cotton": None, "cocoa": None, "coffee": None, "tobacco": None,
                                               "clay": 5, "oil": 11},
                       exports={"cotton_mill": None, "tobacco": None},
                       world=world)
    fechiques.population["jornaleros"] = 5 * 10 * 10
    fechiques.population["obreros"] = 3 * 20 * 10

    crown_falls = Island("Crown Falls", fertility={"potato": None, "grain": None, "hops": None, "grapes": None,
                                                   "clay": 4, "iron_mine": 9, "coal_mine": 7, "zinc": 3, "copper": 4, "limestone": 3, "oil": 5},
                         exports={},
                         world=world)
    crown_falls.population["farmers"] = 7 * 10 * 10
    crown_falls.requested_construction_buildings["sawmill"] = 2

    for island in world:
        island.calculate_required_production_buildings()

    ditchwater.display_required()
    glanther.display_required()
    skidbjerg.display_required()
    la_isla.display_required()
    fechiques.display_required()
    crown_falls.display_required()
