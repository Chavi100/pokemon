import json
from flask import request, Response
from pokemon_query import find_roster,find_owners,find_by_type,update_type,add_pokemon,delete_pokemon,evolve_pokemon
from connections import server,port_number
from my_requests import get_next_form,get_info


@server.route('/')
def index():
    return "welcome to pokemon server! here you can handle a pokemon DB"


@server.route('/add_pokemon',methods=['POST'])
def add_pokemon_to_db():
    res = request.get_json()
    stat=add_pokemon(res)
    if stat==200:
        return Response(json.dumps("added pokemon: {}".format(res["name"])),200)
    else:
        return Response("failed to add pokemon",400)




@server.route('/delete_pokemon/<id>',methods=['DELETE'])
def delete_received_pokemon(id):
    stat=delete_pokemon(id)
    return Response(stat[0],status=stat[1])


@server.route('/update_pokemon_type/<name>',methods=['GET'])
def update_types(name):
    info=get_info(name)
    types=info["types"]
    print(types)
    type_lst=[]
    for slot in types:
        type_lst.append(slot['type']['name'])
    res=update_type(type_lst,name)
    if res=="updated":
        return Response(json.dumps("updated types of : {} ,types ar: {}".format(name,type_lst)),status=200)
    else:
        return Response(res,status=400)


@server.route('/get_pokemon_of_type/<type>',methods=['GET'])
def find_pokemons_of_type(type):
   res=find_by_type(type)
   stat=200
   if res=='failed to search':
       stat=400
   return Response(json.dumps(res),stat)



@server.route('/all_owners_pokemons/<owner>',methods=['GET'])
def find_pokemon_by_owner(owner):
    res=find_roster(owner)
    stat = 200
    if res == 'failed to search':
        stat = 400
    return Response(json.dumps(res),stat)


@server.route('/all_pokemons_trainers/<pokemon>')
def find_owner_by_pokemon(pokemon):
    res=find_owners(pokemon)
    stat = 200
    if res == 'failed to search':
        stat = 400
    return Response(json.dumps(res), stat)


@server.route('/evolve_pokemon',methods=['PUT'])
def evolves():
    res = request.get_json()
    next_form=get_next_form (res['pokemon_name'])
    res=evolve_pokemon(res['pokemon_name'],next_form,res['owner_name'],res['owner_town'])
    if res=="failed to add evolved pokemon to db":
        return Response("failed to add evolved pokemon: {}".format(next_form),400)
    elif res=="failed to update pokemon from db":
        return  Response(res,400)
    elif res=="trainer has no such pokemon":
        return Response(res,400)
    else:
        return Response(json.dumps("evolved pokemon {} to {}".format(res['pokemon_name'],next_form)),200)



if __name__ == '__main__':
    server.run(port=port_number)