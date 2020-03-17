import math

POPULATION_TYPES = ["farmers", "workers",
                    "explorers", "technicians"]


class ProductionBuilding:
    def __init__(self, name: str, consumers: dict):
        self.name = name
        for consumer in consumers.keys():
            assert consumer in POPULATION_TYPES
        self.consumers = consumers


FISHERY = ProductionBuilding(name="fishery",
                             consumers={"farmers": 80, "workers": 40})
SCHNAPPS_DISTILLERY = ProductionBuilding(name="schnapps",
                                         consumers={"farmers": 60, "workers": 30,
                                                    "explorers": 133.3, "technicians": 66.7})

PRODUCTION_BUILDINGS = [FISHERY, SCHNAPPS_DISTILLERY]


class Island:
    def __init__(self, name:str):
        self.name = name
        self.population = {}
        for pop in POPULATION_TYPES:
            self.population[pop] = 0

    def calculate_production_buildings(self) -> dict:
        results = {}
        for building in PRODUCTION_BUILDINGS:
            results[building.name] = 0

        for building in PRODUCTION_BUILDINGS:
            for consumer in building.consumers.keys():
                results[building.name] += self.population[consumer] / building.consumers[consumer]

        # Round results up
        for building_name in results:
            results[building_name] = math.ceil(results[building_name])
        return results

ditchwater = Island(name="Ditchwater")
ditchwater.population["farmers"] = 150
ditchwater.population["workers"] = 55
print(ditchwater.calculate_production_buildings())
