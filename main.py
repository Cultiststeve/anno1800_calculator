import math


class NoFertility(Exception):
    pass


POPULATION_RESIDENCES = {"farmers": 10, "workers": 20,
                         "artisans": 30, "engineers": 40,
                         "explorers": -1, "technicians": -1,
                         "jornaleros": 10,  "obreros": 20}


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
                            consumers={"workers": 2200/2, "artisans": 1650 / 2})
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
                             consumers={"workers": 2600/2, "artisans": 1950/2, "obreros": 1500/2},
                             requires={"malthouse": 2 / 1,
                                       "hops": 3/2})
CATTLE = ProductionBuilding(name="cattle")
PEPPERS = ProductionBuilding(name="peppers",
                             needs_fertility="peppers")
KITCHEN = ProductionBuilding(name="kitchen",
                             requires={"cattle": 1, "peppers": 1})
CANNERY = ProductionBuilding(name="cannery",
                             requires={"kitchen": 8/6, "iron_mine": 1/6},
                             consumers={"artisans": 11700/6, "engineers": 7800/6, "technicians": 6666/6})
SAND = ProductionBuilding(name="sand")
GLASS = ProductionBuilding(name="glass",
                           requires={"sand": 1})
WINDOWS = ProductionBuilding(name="windows",
                             requires={"glass": 2/4, "lumberjack": 1/4})
SEWING_MACHINE = ProductionBuilding(name="sewing_machine",
                                    requires={"furnace": 1, "lumberjack": 1/2},
                                    consumers={"artisans": 4200/2, "engineers": 2800/2, "obreros": 3200/2})
COTTON_PLANTATION = ProductionBuilding(name="cotton_plantation",
                                       needs_fertility="cotton")
COTTON_MILL = ProductionBuilding(name="cotton_mill",
                                 requires={"cotton_plantation": 2/1})
HUNTING_CABIN = ProductionBuilding(name="hunting_cabin",
                                   needs_fertility="furs")
FUR_DEALER = ProductionBuilding(name="fur_dealer",
                                requires={"cotton_mill": 1, "hunting_cabin": 2/1},
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
                         consumers={"jornaleros": 2800, "obreros": 2800,
                                    "artisans": 2100, "engineers": 1400})


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
                         # "cotton_plantation": COTTON_PLANTATION,
                         # "cotton_mill": COTTON_MILL,
                         # "hunting_cabin": HUNTING_CABIN,
                         # "fur_dealer": FUR_DEALER,
                         "plantain": PLANTAIN,
                         "fish_oil": FISH_OIL,
                         "fried_plantain": FRIED_PLANTAIN,
                         "sugar": SUGAR,
                         "rum": RUM
                         }

CONSTRUCTION_MATERIAL_BUILDINGS = {"sawmill": SAWMILL,
                                   "brick": BRICK,
                                   "sailmaker": SAIL_MAKER,
                                   "steel_works": STEEL_WORKS,
                                   "weapons": WEAPONS,
                                   "windows": WINDOWS}

ALL_BUILDINGS = {}
ALL_BUILDINGS.update(CONSUMABLES_BUILDINGS)
ALL_BUILDINGS.update(CONSTRUCTION_MATERIAL_BUILDINGS)

NATURAL_RESOURCES = ["coal_mine", "iron_mine", "clay", "copper_mine", "oil_field", "gold",
                     "hops", "grain", "potato", "peppers", "furs", "saltpeter", "grapes",
                     "cotton", "plantain", "sugar", "corn", "coffee", "caoutchouc"]


class Island:
    def __init__(self, name: str, fertility: dict, exports: dict, world: set()):
        """

        Args:
            name: name of island
            fertility: resources on island if present
                dict value is maximum number of consumers - None if unlimited
            exports: list of buildings it will export the resources from, if requested
                will not export if doesnt have fertility cap
        """
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
                            raise AssertionError(f"Cant export {export}, as it requires more fertility and this island only has {self.fertility[export]} of them")

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
                self.add_required_building(building_required=building.name, number_required=number_required)

        # for each construction resource building
        for building in CONSTRUCTION_MATERIAL_BUILDINGS:
            assert self.requested_construction_buildings[building] >= 0
            if self.requested_construction_buildings[building] == 0:
                continue  # If we dont want any of this type on island
            self.add_required_building(building, self.requested_construction_buildings[building])

    def get_imported_good(self, building_required: str, number_required: float):
        for island in self.world:
            if building_required in island.fertility:
                island.add_required_building(building_required, number_required)
                if building_required in island.exports_to and island.exports_to[building_required][1] == self.name:
                    # if island already exports that good and it has a trade route to the destination island]
                    island.exports_to[building_required][0] += number_required
                else:
                    # else add a new route
                    island.exports_to[building_required] = [number_required, self.name]
                return
        else:
            raise AssertionError(f"{building_required} is required and not present on any island.")

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
                self.get_imported_good(building_required=building_required, number_required=number_required)
                return  # Now we are importing good, dont need requirements on this island
            else:
                if self.fertility[needed_fertility] is not None:  # If there is a limit on fertility
                    if self.fertility[needed_fertility] - number_required < 0:
                        raise NoFertility(f"{self.name} requires more {needed_fertility} but none are available.")
                    else:
                        self.fertility[needed_fertility] -= number_required  # Reduce available amount

        # Add required providers
        for requirement_type in ALL_BUILDINGS[building_required].requires:
            if type(ALL_BUILDINGS[building_required].requires[requirement_type]) is dict:
                # If multiple possible requirements
                building_req_already_satisfied = 0
                for requirement_provider_building in ALL_BUILDINGS[building_required].requires[requirement_type]:
                    # For each possible provider of the requirement
                    # Check if fertility supports it (if it has a fert requirement)

                    if ALL_BUILDINGS[requirement_provider_building].needs_fertility is not None \
                            and self.fertility[requirement_provider_building] == 0:
                        continue  # No fertility for this building, try next possible provider
                    else:
                        # WE need x more, where x = (total required - already satisfied) * how many of the provider are needed to satisify one furnace
                        number_provider_required = (number_required - building_req_already_satisfied) * ALL_BUILDINGS[building_required].requires[requirement_type][requirement_provider_building]
                        try:
                            self.add_required_building(requirement_provider_building, number_provider_required)
                            break  # All of this requirement type satisifed
                        except NoFertility:
                            assert number_provider_required > 0
                            # Not enough fertility for all of them, try some
                            for try_required_num in range(math.ceil(number_provider_required) + 1, 0, -1):  # high to low
                                try:
                                    self.add_required_building(requirement_provider_building, try_required_num)
                                    # Now we have satisifed x of the required building
                                    building_req_already_satisfied += try_required_num * 1/ALL_BUILDINGS[building_required].requires[requirement_type][requirement_provider_building]
                                    assert building_req_already_satisfied < number_required
                                    break  # We could fit this many in
                                except NoFertility:
                                    pass
                            # if less than 1 building capacity left
                            spare_capacity = math.ceil(self.required_buildings[requirement_provider_building]) - self.required_buildings[requirement_provider_building]
                            if spare_capacity > 0:
                                assert 1 > spare_capacity
                                self.add_required_building(requirement_provider_building, spare_capacity)
                                building_req_already_satisfied += spare_capacity * 1/ALL_BUILDINGS[building_required].requires[requirement_type][requirement_provider_building]
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

        print(f"****** {self.name} ******")
        # Round results up
        for building_name in self.required_buildings:
            self.required_buildings[building_name] = math.ceil(self.required_buildings[building_name])
        for building_name in self.exports_to:
            self.exports_to[building_name][0] = math.ceil(self.exports_to[building_name][0])

        print("--- Required resource buildings ---")
        for item in self.required_buildings:
            if self.required_buildings[item] > 0:
                print(f"{item} : {self.required_buildings[item]}")
        res = self.required_residence_buildings()
        if len(self.exports_to) > 0:
            print("--- Trade routes ---")
            for item in self.exports_to:
                assert self.exports_to[item][0] == self.required_buildings[item]
                print(f"Export {self.exports_to[item][0]} {item} to {self.exports_to[item][1]}")
        print("--- Required residences ---")
        for item in res:
            if res[item] > 0:
                print(f"{item} : {res[item]}")
        print("\n")


if __name__ == "__main__":
    world = set()

    ditchwater = Island(name="Ditchwater", fertility={"grain": None, "potato": None, "peppers": None,
                                                      "iron_mine": 2, "coal_mine": 1, "clay": 3},
                        exports={},
                        world=world)
    ditchwater.population["farmers"] = 15 * 10 * 10  # Blocks * houses in block * residents in house
    ditchwater.population["workers"] = 13 * 10 * 20
    ditchwater.population["artisans"] = 3 * 10 * 30
    ditchwater.requested_construction_buildings["sawmill"] = 4
    ditchwater.requested_construction_buildings["brick"] = 6
    ditchwater.requested_construction_buildings["sailmaker"] = 1
    ditchwater.requested_construction_buildings["steel_works"] = 2
    ditchwater.requested_construction_buildings["weapons"] = 3
    ditchwater.requested_construction_buildings["windows"] = 1

    glanther = Island(name="Glanther", fertility={"potato": None, "hops": None, "saltpeter": None,
                                                  "iron_mine": 1, "coal_mine": 4, "copper_mine": 1},
                      exports={"hops": None},
                      world=world)
    glanther.population["farmers"] = 6 * 10 * 10


    la_isla = Island(name="La Isla", fertility={"plantain": None, "sugar": None, "corn": None, "coffee": None,
                                                "clay": 3, "oil_field": 8, "gold": 2},
                     exports={"rum": None},
                     world=world)
    la_isla.population["jornaleros"] = 6 * 10 * 10

    unsetteled_newworld = Island("unsettled", fertility={"plantain": None, "cotton": None, "corn": None, "caoutchouc": None, "coffee": None,
                                                         "clay": 3, "oil_field": 19, "gold": 2},
                                 exports={"cotton_plantation": None},
                                 world=world)

    ditchwater.display_required()
    glanther.display_required()
    la_isla.display_required()
    unsetteled_newworld.display_required()
