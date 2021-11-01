import requests


def test_get_pokemons_by_type():
    url = "http://localhost:3002/get_pokemon_of_type/normal"
    name = requests.get(url=url).json()
    assert ["eevee"] in name
    url = "http://localhost:3002/update_pokemon_type/eevee"
    ans=requests.get(url=url)
    assert ans.status_code == 400

def test_add_pokemon():
    url = "http://localhost:3002/add_pokemon"
    pokemon={
        "id":193,
        "name":"yanma",
        "height":12,
        "weight":380
    }
    res = requests.post(url=url, json=pokemon)
    assert res.status_code==400
    url = "http://localhost:3002/get_pokemon_of_type/bug"
    res = requests.get(url=url)
    assert "yanma" in res
    url = "http://localhost:3002/get_pokemon_of_type/flying"
    res = requests.get(url=url)
    assert "yanma" in res

def test_update_pokemon_types():
    url = "http://localhost:3002/update_pokemon_type/venusaur"
    res = requests.get(url=url)
    assert res.status_code==200
    url = "http://localhost:3002/get_pokemon_of_type/poison"
    res = requests.get(url=url)
    assert "venusaur" in res
    url = "http://localhost:3002/get_pokemon_of_type/grass"
    res = requests.get(url=url)
    assert "venusaur" in res

def test_get_pokemons_by_owner():
    url = "http://localhost:3002/all_owners_pokemons/Drasna"
    res = requests.get(url=url)
    assert res.status_code==200
    assert res == ["wartortle", "caterpie", "beedrill", "arbok", "clefairy",
                               "wigglytuff", "persian", "growlithe", "machamp", "golem", "dodrio", "hypno", "cubone", "eevee", "kabutops"]


def test_get_owners_of_a_pokemon():
    url = "http://localhost:3002/all_pokemons_trainers/charmander"
    res = requests.get(url=url)
    assert res.status_code==200
    assert res==["Giovanni", "Jasmine", "Whitney"]

def test_evolve():
    url = "http://localhost:5000/evolve_pokemon"
    json={
        "pokemon_name":"pinsir",
        "owner_name":"Whitney ",
        "owner_town":"Zedon"
    }
    res = requests.put(url=url, json=json)
    assert res=="failed to update pokemon in db"
    json = {
        "pokemon_name": "spearow",
        "owner_name": "Archie",
        "owner_town": "Little Italy"
    }
    res = requests.put(url=url, json=json)
    assert res == "failed to update pokemon in db"
    json = {
        "pokemon_name": "oddish",
        "owner_name": "Whitney",
        "owner_town": "Zedon"
    }
    res = requests.put(url=url, json=json)
    assert res == "evolved pokemon oddish to gloom"
    json = {
        "pokemon_name": "oddish",
        "owner_name": "Whitney",
        "owner_town": "Zedon"
    }
    res = requests.put(url=url, json=json)
    assert res == "trainer has no such pokemon"
    url = "http://localhost:3002/all_owners_pokemons/Whitney"
    res = requests.get(url=url)
    assert "gloom" in res


