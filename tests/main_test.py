import math

import pytest

import main


@pytest.fixture()
def example_island():
    example_island = main.Island(name="england", fertility=set())
    return example_island


def test_pop_type_in_buildings():
    for building in main.CONSUMABLES_BUILDINGS.values():
        for consumer in building.consumers:
            assert consumer in main.POPULATION_RESIDENCES


def test_add_to_pop(example_island):
    example_island.population["farmers"] = 50
    assert "farmers" in example_island.population
    assert example_island.population["farmers"] == 50
    example_island.population["farmers"] += 25
    assert example_island.population["farmers"] == 75

def test_all_buildings_in_required(example_island):
    required = example_island.required_production_buildings()
    assert len(required) == len(main.CONSUMABLES_BUILDINGS) + len(main.CONSTRUCTION_RES_BUILDING)


# [worker pop, required fishery]
@pytest.mark.parametrize("example_numbers", [[1, 1], [800, 1], [801, 2], [1600, 2], [1610, 3]])
def test_fisher_numbers(example_island, example_numbers):
    example_island.population["farmers"] = example_numbers[0]
    required = example_island.required_production_buildings()
    assert math.ceil(required["fishery"]) == example_numbers[1]


# [worker pop, required schnapps]
@pytest.mark.parametrize("example_numbers", [[1, 1], [600, 1], [601, 2], [1200, 2], [1210, 3]])
def test_schnaps_numbers(example_island, example_numbers):
    example_island.population["farmers"] = example_numbers[0]
    required = example_island.required_production_buildings()
    assert math.ceil(required["schnapps"]) == example_numbers[1]


@pytest.mark.parametrize("population",
                         [
                             [{"farmers": 1, "workers": 0},
                              {"farmers": 10, "workers": 0}],

                             [{"farmers": 2, "workers": 0},
                              {"farmers": 11, "workers": 0}],

                             [{"farmers": 6, "workers": 0},
                              {"farmers": 55, "workers": 0}],

[{"farmers": 1, "workers": 1},
                            {"farmers": 10, "workers": 1}],

[{"farmers": 1, "workers": 3},
                            {"farmers": 10, "workers": 59}],

                             [{"farmers": 2, "workers": 0},
                              {"farmers": 20, "workers": 0}]
                         ]
                         )
def test_residence_numbers(example_island, population):
    example_island.population = population[1]
    residences = example_island.required_residence_buildings()
    for residence in residences:
        assert residences[residence] == population[0][residence]


# Number schnapps (potato always == schnapps)
@pytest.mark.parametrize("example_numbers", [1, 1.1, 2, 4, 8, 32, 32.1, 65])
def test_calculate_requirements_schnapps(example_numbers):
    existing = {}
    for building_name in main.CONSUMABLES_BUILDINGS:
        existing[building_name] = 0
    res = main.calculate_requirements(building_name="schnapps", building_number=example_numbers, existing_buildings=existing)
    assert res["potato"] == example_numbers


@pytest.mark.parametrize("example_farmer_number", [[1, 1], [590, 1], [600, 1], [601, 2], [1200, 2], [1201, 3]])
def test_producer_chain_schnapps(example_island, example_farmer_number):
    example_island.population["farmers"] = example_farmer_number[0]
    assert example_island.population["workers"] == 0
    res = example_island.required_production_buildings()
    assert math.ceil(res["potato"]) == example_farmer_number[1]


# num workers, num bakerys, num flours,
@pytest.mark.parametrize("example_numbers", [[1, 1, 1], [2199, 2, 1], [2200, 2, 1], [2201, 3, 2]])
def test_bread_chain(example_island, example_numbers):
    example_island.population["workers"] = example_numbers[0]
    res = example_island.required_production_buildings()
    assert math.ceil(res["bakery"]) == example_numbers[1]
    assert math.ceil(res["grain"]) == example_numbers[1]
    assert math.ceil(res["flour"]) == example_numbers[2]


@pytest.mark.parametrize("example_numbers", [0, 1, 2, 3, 55])
def test_sawmill(example_island, example_numbers):
    example_island.constuction_res_building["sawmill"] = example_numbers
    res = example_island.required_production_buildings()
    assert res["lumberjack"] == example_numbers


# number workers, number pig farms, number slaughterhouses, num soap factories
@pytest.mark.parametrize("example_numbers", [[1, 1, 1, 1], [4800, 7, 5, 1]])
def test_sausages_and_soap(example_island, example_numbers):
    example_island.population["workers"] = example_numbers[0]
    res = example_island.required_production_buildings()
    assert math.ceil(res["pig"]) == example_numbers[1]
    assert math.ceil(res["slaughters"]) == example_numbers[2]
    assert math.ceil(res["soap"]) == example_numbers[3]
