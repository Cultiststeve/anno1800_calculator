import math

POPULATION_RESIDENCES = {"farmers": 10, "workers": 20,
                         "artisan": 30, "engineer": 40,
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

PRODUCTION_BUILDINGS = {"fishery": FISHERY,
                        "potato": POTATO,
                        "schnapps": SCHNAPPS,
                        "sheep": SHEEP,
                        "knitters": KNITTERS}

def calculate_requirements(building_name: str, building_number: int, existing_buildings: dict):
    """
    
    Args:
        building_name: building to calculate suppliers for
        building_number: number of this building needed
        existing_buildings: dict to store results in

    Returns:

    """
    assert building_name in PRODUCTION_BUILDINGS.keys()
    assert building_number > 0

    for required_building in PRODUCTION_BUILDINGS[building_name].requires:
        required_producer_num = building_number * PRODUCTION_BUILDINGS[building_name].requires[required_building]
        existing_buildings[required_building] += required_producer_num
        # If this producer has its own required producers, include them
        if len(PRODUCTION_BUILDINGS[required_building].consumers) > 0:
            calculate_requirements(building_name=building_name, building_number=required_producer_num, existing_buildings=existing_buildings)

    return existing_buildings


    

class Island:
    def __init__(self, name: str):
        self.name = name
        self.population = {}
        for pop in POPULATION_RESIDENCES:
            self.population[pop] = 0

    def required_production_buildings(self) -> dict:
        results = {}
        for building in PRODUCTION_BUILDINGS:
            results[building] = 0

        # For each building
        for building in PRODUCTION_BUILDINGS.values():
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

        # Round results up
        for building_name in results:
            results[building_name] = math.ceil(results[building_name])
        return results

    def required_residence_buildings(self) -> dict:
        results = {}
        for pop in self.population:
            results[pop] = math.ceil(self.population[pop] / POPULATION_RESIDENCES[pop])

        return results


ditchwater = Island(name="Ditchwater")
ditchwater.population["farmers"] = 400
ditchwater.population["workers"] = 200
print(ditchwater.required_production_buildings())
print(ditchwater.required_residence_buildings())
