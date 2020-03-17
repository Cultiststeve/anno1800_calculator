import pytest

import main


@pytest.fixture()
def example_island():
    example_island = main.Island(name="england")
    return example_island


def test_pop_type_in_buildings():
    for building in main.PRODUCTION_BUILDINGS:
        for consumer in building.consumers:
            assert consumer in main.POPULATION_TYPES


def test_add_to_pop(example_island):
    example_island.population["farmers"] = 50
    assert "farmers" in example_island.population
    assert example_island.population["farmers"] == 50
    example_island.population["farmers"] += 25
    assert example_island.population["farmers"] == 75


# [pop, required fishery]
@pytest.mark.parametrize("example_numbers", [[1, 1], [80, 1], [81, 2], [160, 2], [161, 3]])
def test_fisher_numbers(example_island, example_numbers):
    example_island.population["farmers"] = example_numbers[0]
    required = example_island.calculate_production_buildings()
    assert required
    assert len(required) == len(main.PRODUCTION_BUILDINGS)
    assert required["fishery"] == example_numbers[1]

# [pop, required schnapps]
@pytest.mark.parametrize("example_numbers", [[1, 1], [60, 1], [61, 2], [120, 2], [121, 3]])
def test_fisher_numbers(example_island, example_numbers):
    example_island.population["farmers"] = example_numbers[0]
    required = example_island.calculate_production_buildings()
    assert required
    assert len(required) == len(main.PRODUCTION_BUILDINGS)
    assert required["fishery"] == example_numbers[1]
