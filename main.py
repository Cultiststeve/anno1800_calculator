import math


class NoFertility(Exception):
    pass


POPULATION_RESIDENCES = {"farmers": 10, "workers": 20,
                         "artisans": 30, "engineers": 40,
                         "explorers": -1, "technicians": -1,
                         "obreros": -1}


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
                            consumers={"workers": 1100, "artisans": 1650 / 2})
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
                             requires={"charcoal": {"coal_mine": .5, "charcoal_kiln": 1},
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
                             consumers={"workers": 2600, "artisans": 1950,
                                        "obreros": 1500},
                             requires={"malthouse": 2 / 1,
                                       "hops": 2 / 3})

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
                         "brewery": BREWERY}

CONSTRUCTION_MATERIAL_BUILDINGS = {"sawmill": SAWMILL,
                                   "brick": BRICK,
                                   "sailmaker": SAIL_MAKER,
                                   "steel_works": STEEL_WORKS}

ALL_BUILDINGS = {}
ALL_BUILDINGS.update(CONSUMABLES_BUILDINGS)
ALL_BUILDINGS.update(CONSTRUCTION_MATERIAL_BUILDINGS)

NATURAL_RESOURCES = ["coal_mine", "iron_mine", "clay", "copper_mine",
                     "hops", "grain", "potato", "peppers", "furs", "saltpeter", "grapes"]


class Island:
    def __init__(self, name: str, fertility: dict, exports: dict):
        """

        Args:
            name: name of island
            fertility: resources on island if present
                dict value is maximum number of consumers - None if unlimited
            exports: list of buildings it will export the resources from, if requested
                will not export if doesnt have fertility cap
        """
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
                try:
                    assert self.exports[export] <= self.fertility[export]
                except AssertionError:
                    raise AssertionError(f"Cant export {export}, as it requires a fertility and this island only has {self.fertility[export]} of them")

        self.population = {}
        for pop in POPULATION_RESIDENCES:
            self.population[pop] = 0
        self.requested_construction_buildings = {}
        for building_type in CONSTRUCTION_MATERIAL_BUILDINGS:
            self.requested_construction_buildings[building_type] = 0

        self.required_buildings = {}
        for building in ALL_BUILDINGS:
            self.required_buildings[building] = 0
        self.exports_to = {}  # List of what this island will export, and to where
        # "island_to": {"good: number of buildings exporting}

    def calculate_required_production_buildings(self) -> dict:
        """

        Returns: actual building numbers required
            (can be floats)

        """
        # For each consumable building
        for building in CONSUMABLES_BUILDINGS.values():
            # for each consumer
            for consumer in building.consumers.keys():
                if self.population[consumer] == 0:
                    continue  # No need to do any calculations if no pop on this island

                number_required = self.population[consumer] / building.consumers[consumer]
                self.add_required_building(building_required=building.name, number_required=number_required)

        # for each construction resource building
        for building in CONSTRUCTION_MATERIAL_BUILDINGS:
            assert self.requested_construction_buildings[building] >= 0
            if self.requested_construction_buildings[building] == 0:
                continue  # If we dont want any of this type on island
            self.add_required_building(building, self.requested_construction_buildings[building])

    def add_required_building(self, building_required: str, number_required: float):
        """
        Adds providers for required building, then adds required building itself

        Args:
            building_required: Building needed
            number_required:

        Returns:

        """
        # calculate how many buildings needed to satisfy the population
        assert building_required in ALL_BUILDINGS.keys()
        assert number_required > 0

        if ALL_BUILDINGS[building_required].needs_fertility is not None:  # If building has a fertility requirement
            needed_fertility = ALL_BUILDINGS[building_required].needs_fertility
            try:
                assert needed_fertility in self.fertility
            except AssertionError:
                raise AssertionError(f"{needed_fertility} is not in {self.fertility}.")
            if self.fertility[needed_fertility] is not None:  # If there is a limit on fertility
                if self.fertility[needed_fertility] - number_required < 0:
                    raise NoFertility(f"{self.name} requires more {needed_fertility} but none are available.")
                else:
                    self.fertility[needed_fertility] -= number_required  # Reduce available amount

        # Add required providers
        for requirement_type in ALL_BUILDINGS[building_required].requires:
            if type(ALL_BUILDINGS[building_required].requires[requirement_type]) is dict:
                # If multiple possible requirements
                previous_requirement_satified = 0
                for requirement_provider_building in ALL_BUILDINGS[building_required].requires[requirement_type]:
                    # For each possible provider of the requirement
                    # Check if fertility supports it (if it has a fert requirement)

                    if ALL_BUILDINGS[requirement_provider_building].needs_fertility is not None \
                            and self.fertility[requirement_provider_building] == 0:
                        continue  # No fertility for this building, try next possible provider
                    else:
                        number_provider_required = (number_required - previous_requirement_satified) * ALL_BUILDINGS[building_required].requires[requirement_type][requirement_provider_building]
                        try:
                            self.add_required_building(requirement_provider_building, number_provider_required)
                            break  # All of this requirement type satisifed
                        except NoFertility:
                            assert number_provider_required > 1
                            # Not enough fertility for all of them, try some
                            for try_required_num in range(math.ceil(number_provider_required) + 1, 0, -1):  # high to low
                                try:
                                    self.add_required_building(requirement_provider_building, try_required_num)
                                    previous_requirement_satified = try_required_num * 1/ALL_BUILDINGS[building_required].requires[requirement_type][requirement_provider_building]
                                    break  # We could fit this many in
                                except NoFertility:
                                    pass
                            # Now for loop will goo to next requirement
                else:
                    raise NoFertility(f"Island does not have fertility for any providers for {requirement_type}")
            else:
                # only one possible requirement, calculate number type
                number_provider_required = number_required * ALL_BUILDINGS[building_required].requires[requirement_type]
                self.add_required_building(requirement_type, number_provider_required)
        # Add these buildings to required (now we have all requirements)
        self.required_buildings[building_required] += number_required

    def required_residence_buildings(self) -> dict:
        results = {}
        for pop in self.population:
            results[pop] = math.ceil(self.population[pop] / POPULATION_RESIDENCES[pop])

        return results

    def display_required(self) -> None:
        self.calculate_required_production_buildings()

        print(f"*** {self.name} ***")
        # Round results up
        for building_name in self.required_buildings:
            self.required_buildings[building_name] = math.ceil(self.required_buildings[building_name])

        print("--- Required resource buildings ---")
        for item in self.required_buildings:
            if self.required_buildings[item] > 0:
                print(f"{item} : {self.required_buildings[item]}")
        res = self.required_residence_buildings()
        print("--- Required residences ---")
        for item in res:
            if res[item] > 0:
                print(f"{item} : {res[item]}")


if __name__ == "__main__":
    ditchwater = Island(name="Ditchwater", fertility={"grain": None, "potato": None, "peppers": None,
                                                      "iron_mine": 2, "coal_mine": 0, "clay": 3})
    ditchwater.population["farmers"] = 10 * 10 * 10
    ditchwater.population["workers"] = 7 * 10 * 20
    ditchwater.requested_construction_buildings["sawmill"] = 4
    ditchwater.requested_construction_buildings["brick"] = 6
    ditchwater.requested_construction_buildings["sailmaker"] = 1
    ditchwater.requested_construction_buildings["steel_works"] = 1
    ditchwater.requested_construction_buildings["weapons"] = 1
    ditchwater.display_required()

    glanther = Island(name="Glanther", fertility={"potato": None, "hops": None, "saltpeter": None,
                                                  "iron_mine": 1, "coal_mine": 4, "copper_mine": 1})
    glanther.population["farmers"] = 6 * 10 * 10
    glanther.display_required()
