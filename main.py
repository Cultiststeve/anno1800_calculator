import math

POPULATION_RESIDENCES = {"farmers": 10, "workers": 20,
                         "artisans": 30, "engineers": 40,
                         "explorers": -1, "technicians": -1}


class ProductionBuilding:
    def __init__(self, name: str, consumers: dict = {}, requires: dict = {}):
        """

        Args:
            name:
            consumers: number of consumers the building feeds
            requires:
        """
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
POTATO = ProductionBuilding(name="potato")
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
GRAIN = ProductionBuilding(name="grain")
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
CLAY = ProductionBuilding(name="clay")
BRICK = ProductionBuilding(name="brick",
                           requires={"clay": .5})
SAILMAKER = ProductionBuilding(name="sailmaker",
                               requires={"sheep": 1})

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
                         "clay": CLAY}

CONSTRUCTION_RES_BUILDING = {"sawmill": SAWMILL,
                             "brick": BRICK,
                             "sailmaker": SAILMAKER}

ALL_BUILDINGS = {}
ALL_BUILDINGS.update(CONSUMABLES_BUILDINGS)
ALL_BUILDINGS.update(CONSTRUCTION_RES_BUILDING)


POSSIBLE_FERTILITIES = ["hops", "wheat"]


def calculate_requirements(building_name: str, building_number: int, existing_buildings: dict):
    """
    Args:
        building_name: building to calculate suppliers for
        building_number: number of this building needed
        existing_buildings: dict to store results in

    Returns:
    """
    assert building_name in CONSUMABLES_BUILDINGS.keys() or CONSTRUCTION_RES_BUILDING.keys()
    assert building_number > 0

    for required_building in ALL_BUILDINGS[building_name].requires:
        required_producer_num = building_number * ALL_BUILDINGS[building_name].requires[required_building]
        existing_buildings[required_building] += required_producer_num
        # If this producer has its own required producers, include them
        for required_building_prechain in ALL_BUILDINGS[required_building].requires:
            existing_buildings[required_building_prechain] += required_producer_num * ALL_BUILDINGS[required_building].requires[
                required_building_prechain]
            calculate_requirements(building_name=required_building_prechain, building_number=required_producer_num, existing_buildings=existing_buildings)

    return existing_buildings


class Island:
    def __init__(self, name: str, fertility: set):
        self.name = name
        for item in fertility:
            assert item in POSSIBLE_FERTILITIES
        self.fertility = fertility

        self.population = {}
        for pop in POPULATION_RESIDENCES:
            self.population[pop] = 0
        self.constuction_res_building = {}
        for building_type in CONSTRUCTION_RES_BUILDING:
            self.constuction_res_building[building_type] = 0

    def required_production_buildings(self) -> dict:
        """

        Returns: actual building numbers required
            (can be floats)

        """
        results = {}
        for building in CONSUMABLES_BUILDINGS:
            results[building] = 0
        for building in CONSTRUCTION_RES_BUILDING:
            results[building] = 0

        # For each consumable building
        for building in CONSUMABLES_BUILDINGS.values():
            # for each consumer
            for consumer in building.consumers.keys():
                if self.population[consumer] == 0:
                    continue
                # calculate how many buildings needed to satisfy the population
                buildings_required = self.population[consumer] / building.consumers[consumer]
                assert buildings_required >= 0
                if buildings_required > 0:
                    results[building.name] += buildings_required
                    # Calculate how many chain buildings needed to feed end of chain
                    calculate_requirements(building.name, buildings_required, results)
        # for each construction resource building
        for building in CONSTRUCTION_RES_BUILDING:
            assert self.constuction_res_building[building] >= 0
            if self.constuction_res_building[building] == 0:
                continue
            results[building] += self.constuction_res_building[building]
            calculate_requirements(building, self.constuction_res_building[building], results)

        return results


    def required_residence_buildings(self) -> dict:
        results = {}
        for pop in self.population:
            results[pop] = math.ceil(self.population[pop] / POPULATION_RESIDENCES[pop])

        return results

    def display_required(self):
        res = self.required_production_buildings()
        # Round results up
        for building_name in res:
            res[building_name] = math.ceil(res[building_name])

        print("--- Required resource buildings ---")
        for item in res:
            print(f"{item} : {res[item]}")
        res = self.required_residence_buildings()
        print("--- Required residences ---")
        for item in res:
            print(f"{item} : {res[item]}")


if __name__ == "__main__":
    ditchwater = Island(name="Ditchwater", fertility={"wheat"})
    ditchwater.population["farmers"] = 8 * 10 * 10
    ditchwater.population["workers"] = 5 * 10 * 20
    ditchwater.constuction_res_building["sawmill"] = 4
    ditchwater.constuction_res_building["brick"] = 3
    ditchwater.constuction_res_building["sailmaker"] = 1
    ditchwater.display_required()
    # print(ditchwater.required_production_buildings())
    # print(ditchwater.required_residence_buildings())
