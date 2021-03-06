import math

import pytest

import main


@pytest.fixture()
def set_global_modifier_1():
    existing_mod = main.GLOBAL_CONSUMPTION_MODIFIER
    main.GLOBAL_CONSUMPTION_MODIFIER = 1
    yield
    main.GLOBAL_CONSUMPTION_MODIFIER = existing_mod


@pytest.fixture()
def example_island(set_global_modifier_1):
    "example island with all fertilities"
    world = set()
    example_island = main.Island(name="example_island", fertility={}, exports={}, world=world)
    for resource in main.NATURAL_RESOURCES:
        example_island.fertility[resource] = None
    example_island.fertility["coal_mine"] = 100  # Cant be none
    return example_island


def test_pop_type_in_buildings():
    for building in main.CONSUMABLES_BUILDINGS.values():
        for consumer in building.consumers:
            assert consumer in main.POPULATION_RESIDENCES


def test_add_to_pop(example_island):
    example_island.residences["farmers"] = 5
    assert "farmers" in example_island.residences
    assert example_island.residences["farmers"] == 5
    example_island.residences["farmers"] += 2
    assert example_island.residences["farmers"] == 7


def test_all_buildings_in_lists():
    assert len(main.ALL_BUILDINGS) == len(main.CONSUMABLES_BUILDINGS) + len(main.CONSTRUCTION_MATERIAL_BUILDINGS)


def test_names_correct():
    for building in main.ALL_BUILDINGS:
        assert building == main.ALL_BUILDINGS[building].name


def test_all_requirements_positive():
    for building in main.ALL_BUILDINGS:
        for requirement in main.ALL_BUILDINGS[building].requires:
            assert main.ALL_BUILDINGS[building].requires[requirement] > 0


def test_all_buildings_in_required(example_island: main.Island):
    example_island.calculate_required_production_buildings()
    assert len(example_island.required_buildings) == len(main.CONSUMABLES_BUILDINGS) + len(main.CONSTRUCTION_MATERIAL_BUILDINGS)


# [worker pop, required fishery]
@pytest.mark.parametrize("example_numbers", [[1, 1], [80, 1], [81, 2], [160, 2], [161, 3]])
def test_fisher_numbers(example_island: main.Island, example_numbers):
    example_island.residences["farmers"] = example_numbers[0]
    example_island.calculate_required_production_buildings()
    assert math.ceil(example_island.required_buildings["fishery"]) == example_numbers[1]


# [worker pop, required schnapps]
@pytest.mark.parametrize("example_numbers", [[1, 1], [60, 1], [61, 2], [120, 2], [121, 3]])
def test_schnaps_numbers(example_island: main.Island, example_numbers):
    example_island.residences["farmers"] = example_numbers[0]
    example_island.calculate_required_production_buildings()
    assert math.ceil(example_island.required_buildings["schnapps"]) == example_numbers[1]


# @pytest.mark.parametrize("residences",
#                          [
#                              [{"farmers": 1, "workers": 0},
#                               {"farmers": 10, "workers": 0}],
#
#                              [{"farmers": 2, "workers": 0},
#                               {"farmers": 11, "workers": 0}],
#
#                              [{"farmers": 6, "workers": 0},
#                               {"farmers": 55, "workers": 0}],
#
#                              [{"farmers": 1, "workers": 1},
#                               {"farmers": 10, "workers": 1}],
#
#                              [{"farmers": 1, "workers": 3},
#                               {"farmers": 10, "workers": 59}],
#
#                              [{"farmers": 2, "workers": 0},
#                               {"farmers": 20, "workers": 0}]
#                          ]
#                          )
# def test_residence_numbers(example_island, residences):
#     example_island.residences = residences[1]
#     residences = example_island.required_residence_buildings()
#     for residence in residences:
#         assert residences[residence] == residences[0][residence]


# Number schnapps (potato always == schnapps)
@pytest.mark.parametrize("example_numbers", [1, 1.1, 2, 4, 8, 32, 32.1, 65])
def test_calculate_requirements_schnapps(example_island, example_numbers):
    example_island.add_required_building(building_required="schnapps", number_required=example_numbers)
    assert example_island.required_buildings["potato"] == example_numbers


@pytest.mark.parametrize("example_farmer_number", [[1, 1], [59, 1], [60, 1], [61, 2], [120, 2], [121, 3]])
def test_producer_chain_schnapps(example_island, example_farmer_number):
    example_island.residences["farmers"] = example_farmer_number[0]
    assert example_island.residences["workers"] == 0
    example_island.calculate_required_production_buildings()
    assert math.ceil(example_island.required_buildings["potato"]) == example_farmer_number[1]


@pytest.fixture()
def remove_brewery():
    del main.CONSUMABLES_BUILDINGS["brewery"]
    yield
    main.CONSUMABLES_BUILDINGS["brewery"] = main.BREWERY


# num workers, num bakerys, num flours,
@pytest.mark.parametrize("example_numbers", [[1, 1, 1], [110 / 2, 1, 1], [110, 2, 1], [111, 3, 2]])
def test_bread_chain(example_island, remove_brewery, example_numbers):
    # Pretend no beer
    example_island.residences["workers"] = example_numbers[0]
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
@pytest.mark.parametrize("example_numbers", [[1, 1, 1, 1], [241, 5 + 2, 5, 2]])
def test_sausages_and_soap(example_island, example_numbers):
    example_island.residences["workers"] = example_numbers[0]
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
    world = set()
    fertile_island = main.Island(name="fertile", fertility=example_fertility, exports={}, world=world)


def test_no_fertility_farmers(example_island: main.Island):
    example_island.residences["farmers"] = 1
    example_island.fertility = {}
    with pytest.raises(main.NoFertility):
        example_island.calculate_required_production_buildings()


def test_no_fertility_workers(example_island):
    example_island.residences["workers"] = 1
    example_island.fertility = {}
    with pytest.raises(main.NoFertility):
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
    example_island.residences["workers"] = 1
    example_island.calculate_required_production_buildings()


def test_export_allowed():
    world = set()
    coal_export_island = main.Island(name="coal_export_island", fertility={"coal_mine": 1}, exports={"coal_mine": 1}, world=world)


def test_export_more_than_possible():
    world = set()
    with pytest.raises(AssertionError):
        coal_export_island = main.Island(name="coal_export_island", fertility={"coal_mine": 1}, exports={"coal_mine": 2}, world=world)


def test_export_unlimited_fer_limit():
    world = set()
    with pytest.raises(AssertionError):
        bad_isle = main.Island(name="bad", fertility={"grain": 1}, exports={"grain": None}, world=world)


def test_limit_export_allowed():
    world = set()
    coal_export_island = main.Island(name="coal_export_island", fertility={"coal_mine": None}, exports={"coal_mine": 1}, world=world)


def test_world_creation(example_island: main.Island):
    assert example_island in example_island.world
    second_isle = main.Island(name="2nd", fertility={}, exports={}, world=example_island.world)
    assert second_isle in example_island.world


def test_export_hops_sucess():
    world = set()
    main_island = main.Island(name="main-isle", fertility={"potato": None, "grain": None}, exports={}, world=world)
    main_island.residences["workers"] = 1
    hop_island = main.Island(name="hop-isle", fertility={"hops": None}, exports={"hops": None}, world=world)
    main_island.calculate_required_production_buildings()
    assert main_island.required_buildings["hops"] == 0
    assert math.ceil(hop_island.required_buildings["hops"]) == 1
    assert math.ceil(hop_island.exports_to["hops"]["main-isle"]) == 1


def test_export_to_sucess():
    world = set()
    main_island = main.Island(name="main-isle", fertility={"potato": None, "grain": None}, exports={}, world=world)
    main_island.residences["workers"] = (130 / 2) * 2 / 3  # number of workers that means 1 hop field required
    hop_island = main.Island(name="hop-isle", fertility={"hops": None}, exports={"hops": None}, world=world)
    main_island.calculate_required_production_buildings()
    assert len(hop_island.exports_to) == 1
    assert math.ceil(hop_island.exports_to["hops"]["main-isle"]) == 1


def test_export_to_sucess_many(set_global_modifier_1):
    world = set()
    main_island = main.Island(name="main-isle", fertility={"potato": None, "grain": None}, exports={}, world=world)
    main_island.residences["workers"] = (130 / 2) * (2 / 3) * 5  # number of workers that means 5 hop field required
    hop_island = main.Island(name="hop-isle", fertility={"hops": None}, exports={"hops": None}, world=world)
    main_island.calculate_required_production_buildings()
    assert len(hop_island.exports_to) == 1
    assert math.ceil(hop_island.exports_to["hops"]["main-isle"]) == 5


@pytest.fixture()
def remove_sewing_machines():
    del main.CONSUMABLES_BUILDINGS["sewing_machine"]
    yield
    main.CONSUMABLES_BUILDINGS["sewing_machine"] = main.SEWING_MACHINE


# number artisans, cannery, kitchen, iron, pepper, cattle
@pytest.mark.parametrize("example_numbers", [[390, 6, 8, 1, 8, 8], [391, 7, 9, 2, 9, 9]])
def test_cannery_numbers(example_island: main.Island, example_numbers, remove_sewing_machines):
    example_island.residences["artisans"] = example_numbers[0]
    example_island.calculate_required_production_buildings()
    assert math.ceil(example_island.required_buildings["cannery"]) == example_numbers[1]
    assert math.ceil(example_island.required_buildings["kitchen"]) == example_numbers[2]
    assert math.ceil(example_island.required_buildings["iron_mine"]) == example_numbers[3]
    assert math.ceil(example_island.required_buildings["peppers"]) == example_numbers[4]
    assert math.ceil(example_island.required_buildings["cattle"]) == example_numbers[5]


def test_windows(example_island: main.Island):
    example_island.requested_construction_buildings["windows"] = 4
    example_island.calculate_required_production_buildings()
    assert example_island.required_buildings["sand"] == 2
    assert example_island.required_buildings["glass"] == 2
    assert example_island.required_buildings["lumberjack"] == 1


def test_more_hops(example_island: main.Island):
    del example_island.fertility["hops"]
    example_island.residences["workers"] = 130 * 2
    hop_island = main.Island(name="hop-isle", fertility={"hops": None}, exports={"hops": None}, world=example_island.world)
    example_island.calculate_required_production_buildings()
    hop_island.calculate_required_production_buildings()
    assert example_island.required_buildings["hops"] == 0
    assert example_island.required_buildings["brewery"] == 4
    assert hop_island.required_buildings["hops"] == 6


@pytest.fixture()
def artisans_dont_drink_beer():
    del main.BREWERY.consumers["artisans"]
    yield
    main.BREWERY.consumers["artisans"] = 1950 / 2


@pytest.fixture()
def artisans_dont_drink_rum():
    del main.RUM.consumers["artisans"]
    yield
    main.RUM.consumers["artisans"] = 1950 / 2


def test_exports_correct_num_with_both(artisans_dont_drink_rum, set_global_modifier_1):
    world = set()
    main_island = main.Island(name="main-isle",
                              fertility={"potato": None, "grain": None, "peppers": None, "iron_mine": None, "coal_mine": 100, "sugar": None, "cotton": None,
                                         "furs": None}, exports={}, world=world)
    # main_island.residences["farmers"] = 1000
    main_island.residences["workers"] = (130 / 2) * (2 / 3) * 5  # number of workers that means 5 hop field required
    main_island.residences["artisans"] = (65 / 2) * (2 / 3) * 5
    hop_island = main.Island(name="hop-isle", fertility={"hops": None}, exports={"hops": None}, world=world)
    main_island.calculate_required_production_buildings()
    hop_island.calculate_required_production_buildings()
    assert len(hop_island.exports_to) == 1
    assert math.ceil(hop_island.exports_to["hops"]["main-isle"]) == 10 == math.ceil(hop_island.required_buildings["hops"])


def test_some_coalmine_somekiln():
    main_island = main.Island(name="main-isle", fertility={"potato": None, "grain": None, "peppers": None, "iron_mine": 55, "coal_mine": 1}, exports={},
                              world=set())
    main_island.requested_construction_buildings["weapons"] = 12
    main_island.requested_construction_buildings["steel_works"] = 3
    main_island.calculate_required_production_buildings()
    assert main_island.required_buildings["weapons"] == 12
    assert main_island.required_buildings["coal_mine"] == 1
    assert main_island.required_buildings["charcoal_kiln"] == 4


def test_odd_furnace_number():
    world = set()

    mainisle = main.Island(name="main-isle", fertility={"grain": None, "potato": None, "peppers": None,
                                                        "iron_mine": 2, "coal_mine": 1, "clay": 3},
                           exports={},
                           world=world)
    mainisle.requested_construction_buildings["sawmill"] = 4
    mainisle.requested_construction_buildings["brick"] = 6
    mainisle.requested_construction_buildings["sailmaker"] = 1
    mainisle.requested_construction_buildings["steel_works"] = 2
    mainisle.requested_construction_buildings["weapons"] = 3
    mainisle.requested_construction_buildings["windows"] = 1
    mainisle.calculate_required_production_buildings()
    assert mainisle.required_buildings["coal_mine"] == 1
    assert math.ceil(mainisle.required_buildings["furnace"]) == 3
    assert math.ceil(mainisle.required_buildings["charcoal_kiln"]) == 1


def test_no_sugar_export(example_island: main.Island):
    example_island.residences["artisans"] = 1
    del example_island.fertility["sugar"]
    new_world = main.Island(name="newworld",
                            fertility={"sugar": None},
                            exports={},
                            world=example_island.world)
    with pytest.raises(main.NoFertility):
        example_island.calculate_required_production_buildings()


def test_do_producers_have_fert():
    res = main.do_producers_have_fert_requirements("brewery")
    assert len(res) == 2
    assert "grain" in res
    assert "hops" in res


def test_export_rum_not_sugar(example_island: main.Island):
    example_island.residences["artisans"] = 1
    del example_island.fertility["sugar"]
    new_world = main.Island(name="newworld",
                            fertility={"sugar": None},
                            exports={"rum": None},
                            world=example_island.world)
    example_island.calculate_required_production_buildings()
    new_world.calculate_required_production_buildings()


def test_no_coal(example_island: main.Island):
    del example_island.fertility["coal_mine"]
    example_island.residences["artisans"] = 1
    example_island.calculate_required_production_buildings()


def test_make_coats_import_raw():
    fur_island = main.Island(name="fur-isle",
                             fertility={"furs": None},
                             exports={"hunting_cabin": None},
                             world=set()
                             )
    cotton_isle = main.Island(name="cotton-isle",
                              fertility={"cotton": None},
                              exports={"cotton_mill": None},
                              world=fur_island.world)
    coat_isle = main.Island(name="coat-isle",
                            fertility={"grain": None, "hops": None, "peppers": None, "iron_mine": None, "sugar": None},
                            exports={},
                            world=fur_island.world)
    coat_isle.residences["artisans"] = 1
    coat_isle.calculate_required_production_buildings()
    fur_island.calculate_required_production_buildings()
    cotton_isle.calculate_required_production_buildings()
    assert math.ceil(cotton_isle.exports_to["cotton_mill"]["coat-isle"]) == 1
    assert math.ceil(cotton_isle.exports_to["cotton_mill"]["coat-isle"]) == 1

    assert math.ceil(fur_island.exports_to["hunting_cabin"]["coat-isle"]) == 1
    assert math.ceil(coat_isle.required_buildings["fur_dealer"]) == 1


def test_new_world_pop(example_island: main.Island):
    example_island.residences["jornaleros"] = 1
    example_island.residences["obreros"] = 1
    example_island.calculate_required_production_buildings()


def test_new_world_pop_beer_export(example_island: main.Island):
    hop_isle = main.Island(name="hop-isle", fertility={"hops": None},
                           exports={"hops": None}, world=example_island.world)
    beer_isle = main.Island(name="beer-isle", fertility={"grain": None},
                            exports={"brewery": None},
                            world=example_island.world)
    del example_island.fertility["grain"]
    example_island.residences["jornaleros"] = 1
    example_island.residences["obreros"] = 1
    example_island.calculate_required_production_buildings()
    beer_isle.calculate_required_production_buildings()
    hop_isle.calculate_required_production_buildings()
    assert math.ceil(beer_isle.required_buildings["brewery"]) == 1
    assert math.ceil(hop_isle.required_buildings["hops"]) == 1


def test_global_production_modifier(example_island: main.Island):
    main.GLOBAL_CONSUMPTION_MODIFIER = .5
    example_island.residences["farmers"] = 80
    example_island.calculate_required_production_buildings()
    assert example_island.required_buildings["fishery"] == .5


def test_global_modifer_producers(example_island: main.Island):
    main.GLOBAL_CONSUMPTION_MODIFIER = .5
    example_island.residences["farmers"] = 65
    example_island.calculate_required_production_buildings()
    assert example_island.required_buildings["sheep"] == .5


def test_global_modifier_imports(example_island: main.Island):
    del example_island.fertility["potato"]
    potato_isle = main.Island(name="potato-isle", fertility={"potato": None},
                              exports={"potato": None},
                              world=example_island.world)
    main.GLOBAL_CONSUMPTION_MODIFIER = .5
    example_island.residences["farmers"] = 60
    example_island.calculate_required_production_buildings()
    assert potato_isle.required_buildings["potato"] == .5


def test_import_some_iron(example_island: main.Island):
    example_island.fertility["iron_mine"] = 1
    iron_isle = main.Island(name="iron-isle", fertility={"iron_mine": 55}, exports={"iron_mine": 50}, world=example_island.world)
    example_island.requested_construction_buildings["steel_works"] = 6  # require 2 iron mines
    example_island.calculate_required_production_buildings()
    assert example_island.required_buildings["iron_mine"] == 1
    assert iron_isle.required_buildings["iron_mine"] == 1


def test_electrisity_modifier(example_island: main.Island):
    example_island.required_buildings["steel_works"] = 1
    example_island.required_buildings["fur_dealer"] = 2
    example_island.required_buildings["heavy_weapons"] = 5
    example_island.required_buildings["furnace"] = .5
    example_island.electrified_buildings = {"steel_works": 1, "heavy_weapons": 2, "fur_dealer": 1, "furnace": 1}
    example_island.modify_for_powered_buildings()
    assert example_island.required_buildings["steel_works"] == 1
    assert example_island.required_buildings["fur_dealer"] == 1
    assert example_island.required_buildings["heavy_weapons"] == 3
    assert example_island.required_buildings["furnace"] == 1


def test_export_too_much_iron():
    exporter_isle = main.Island(name="exporter-isle", world=set(),
                                fertility={"iron_mine": 1},
                                exports={"iron_mine": 1})

    isle_one = main.Island(name="i1", world=exporter_isle.world)
    isle_one.requested_construction_buildings["steel_works"] = 3
    isle_two = main.Island(name="i2", world=exporter_isle.world)
    isle_two.requested_construction_buildings["steel_works"] = 3

    isle_iron_spare = main.Island(name="ironspare", fertility={"iron_mine": 1}, exports={"iron_mine": 1}, world=exporter_isle.world)

    exporter_isle.calculate_required_production_buildings()
    isle_one.calculate_required_production_buildings()
    isle_two.calculate_required_production_buildings()
    assert exporter_isle.required_buildings["iron_mine"] <= 1
    assert isle_iron_spare.required_buildings["iron_mine"] <= 1


def test_must_import(example_island: main.Island):
    example_island.must_import = {"fishery"}
    example_island.residences["farmers"] = 100
    fish_isle = main.Island(name="fish", exports={"fishery": None}, world=example_island.world)
    example_island.calculate_required_production_buildings()
    fish_isle.calculate_required_production_buildings()
    assert example_island.required_buildings["fishery"] == 0
    assert fish_isle.required_buildings["fishery"] > 0
