import math

import pytest

import main


@pytest.fixture()
def example_island():
    "example island with all fertilities"
    example_island = main.Island(name="example_island", fertility={}, exports={})
    for resource in main.NATURAL_RESOURCES:
        example_island.fertility[resource] = None
    return example_island


@pytest.fixture()
def hop_exporter_island() -> main.Island:
    example_island2 = main.Island(name="example_island2", fertility={}, exports={"hops": None})
    for resource in main.NATURAL_RESOURCES:
        example_island2.fertility[resource] = None
    return example_island2


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


def test_all_buildings_in_lists():
    assert len(main.ALL_BUILDINGS) == len(main.CONSUMABLES_BUILDINGS) + len(main.CONSTRUCTION_MATERIAL_BUILDINGS)


def test_all_requirements_positive():
    for building in main.ALL_BUILDINGS:
        for requirement in main.ALL_BUILDINGS[building].requires:
            if type(main.ALL_BUILDINGS[building].requires[requirement]) is dict:
                for possible_provider in main.ALL_BUILDINGS[building].requires[requirement]:
                    assert main.ALL_BUILDINGS[building].requires[requirement][possible_provider] > 0
            else:
                assert main.ALL_BUILDINGS[building].requires[requirement] > 0


def test_all_buildings_in_required(example_island: main.Island):
    example_island.calculate_required_production_buildings()
    assert len(example_island.required_buildings) == len(main.CONSUMABLES_BUILDINGS) + len(main.CONSTRUCTION_MATERIAL_BUILDINGS)


# [worker pop, required fishery]
@pytest.mark.parametrize("example_numbers", [[1, 1], [800, 1], [801, 2], [1600, 2], [1610, 3]])
def test_fisher_numbers(example_island: main.Island, example_numbers):
    example_island.population["farmers"] = example_numbers[0]
    example_island.calculate_required_production_buildings()
    assert math.ceil(example_island.required_buildings["fishery"]) == example_numbers[1]


# [worker pop, required schnapps]
@pytest.mark.parametrize("example_numbers", [[1, 1], [600, 1], [601, 2], [1200, 2], [1210, 3]])
def test_schnaps_numbers(example_island: main.Island, example_numbers):
    example_island.population["farmers"] = example_numbers[0]
    example_island.calculate_required_production_buildings()
    assert math.ceil(example_island.required_buildings["schnapps"]) == example_numbers[1]


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
def test_calculate_requirements_schnapps(example_island, example_numbers):
    example_island.add_required_building(building_required="schnapps", number_required=example_numbers)
    assert example_island.required_buildings["potato"] == example_numbers


@pytest.mark.parametrize("example_farmer_number", [[1, 1], [590, 1], [600, 1], [601, 2], [1200, 2], [1201, 3]])
def test_producer_chain_schnapps(example_island, example_farmer_number):
    example_island.population["farmers"] = example_farmer_number[0]
    assert example_island.population["workers"] == 0
    example_island.calculate_required_production_buildings()
    assert math.ceil(example_island.required_buildings["potato"]) == example_farmer_number[1]


@pytest.fixture()
def remove_brewery():
    del main.CONSUMABLES_BUILDINGS["brewery"]
    yield
    main.CONSUMABLES_BUILDINGS["brewery"] = main.BREWERY

# num workers, num bakerys, num flours,
@pytest.mark.parametrize("example_numbers", [[1, 1, 1], [2199, 2, 1], [2200, 2, 1], [2201, 3, 2]])
def test_bread_chain(example_island, remove_brewery, example_numbers):
    # Pretend no beer
    example_island.population["workers"] = example_numbers[0]
    example_island.calculate_required_production_buildings()
    assert math.ceil(example_island.required_buildings["bakery"]) == example_numbers[1]
    assert math.ceil(example_island.required_buildings["grain"]) == example_numbers[1]
    assert math.ceil(example_island.required_buildings["flour"]) == example_numbers[2]


@pytest.mark.parametrize("example_numbers", [0, 1, 2, 3, 55])
def test_sawmill(example_island, example_numbers):
    example_island.requested_construction_buildings["sawmill"] = example_numbers
    example_island.calculate_required_production_buildings()
    assert example_island.required_buildings["lumberjack"] == example_numbers


# number workers, number pig farms, number slaughterhouses, num soap factories
@pytest.mark.parametrize("example_numbers", [[1, 1, 1, 1], [4800, 7, 5, 1]])
def test_sausages_and_soap(example_island, example_numbers):
    example_island.population["workers"] = example_numbers[0]
    example_island.calculate_required_production_buildings()
    assert math.ceil(example_island.required_buildings["pig"]) == example_numbers[1]
    assert math.ceil(example_island.required_buildings["slaughters"]) == example_numbers[2]
    assert math.ceil(example_island.required_buildings["soap"]) == example_numbers[3]


@pytest.mark.parametrize("example_fertility", [{},
                                               {"iron_mine": 5, "coal_mine": 1},
                                               {"potato": None},
                                               {"grain": 5},
                                               {"peppers": 55}])
def test_fertilities(example_fertility):
    fertile_island = main.Island(name="fertile", fertility=example_fertility, exports={})


def test_no_fertility_farmers(example_island: main.Island):
    example_island.population["farmers"] = 1
    example_island.fertility = {}
    with pytest.raises(AssertionError):
        example_island.calculate_required_production_buildings()


def test_no_fertility_workers(example_island):
    example_island.population["workers"] = 1
    example_island.fertility = {}
    with pytest.raises(AssertionError):
        example_island.calculate_required_production_buildings()


def test_display(example_island: main.Island):
    example_island.display_required()


def test_many_clay_pits(example_island: main.Island):
    example_island.fertility["clay"] = 1
    example_island.requested_construction_buildings["brick"] = 3
    with pytest.raises(main.NoFertility):
        example_island.calculate_required_production_buildings()


def test_good_clay_pit_number(example_island: main.Island):
    example_island.fertility["clay"] = 1
    example_island.requested_construction_buildings["brick"] = 2
    example_island.calculate_required_production_buildings()


def test_steel_works(example_island: main.Island):
    example_island.requested_construction_buildings["steel_works"] = 1
    example_island.calculate_required_production_buildings()


def test_steel_works_no_coalmine(example_island: main.Island):
    example_island.fertility["coal_mine"] = 0
    example_island.requested_construction_buildings["steel_works"] = 3
    example_island.calculate_required_production_buildings()
    assert example_island.required_buildings["coal_mine"] == 0
    assert example_island.required_buildings["charcoal_kiln"] == 2
    assert example_island.required_buildings["furnace"] == 2
    assert example_island.required_buildings["steel_works"] == 3
    assert example_island.required_buildings["iron_mine"] == 1


def test_steel_works_one_coal(example_island: main.Island):
    example_island.fertility["coal_mine"] = 1
    example_island.requested_construction_buildings["steel_works"] = 6
    example_island.calculate_required_production_buildings()
    assert example_island.required_buildings["coal_mine"] == 1
    assert example_island.required_buildings["charcoal_kiln"] == 2
    assert example_island.required_buildings["furnace"] == 4
    assert example_island.required_buildings["steel_works"] == 6
    assert example_island.required_buildings["iron_mine"] == 2


def test_brewery_no_exports(example_island: main.Island):
    example_island.population["workers"] = 1
    example_island.calculate_required_production_buildings()


def test_export_allowed():
    coal_export_island = main.Island(name="coal_export_island", fertility={"coal_mine": 1}, exports={"coal_mine": 1})


def test_export_more_than_possible():
    with pytest.raises(AssertionError):
        coal_export_island = main.Island(name="coal_export_island", fertility={"coal_mine": 1}, exports={"coal_mine": 2})