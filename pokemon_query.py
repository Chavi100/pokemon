from my_requests import get_info


from connections import con,cursor


def get_query(query):
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except:
        return Exception

def send_query(query):
    try:
        cursor.execute(query)
        con.commit()
    except:
        return Exception

#part 1 not used
def heaviest_pokemon():
    try:
        cursor.execute("SELECT * FROM pokemon WHERE weight = (SELECT max(weight) FROM pokemon)")
        result = cursor.fetchall()
        return result
    except(Exception):
        pass

#part 1 not used
def old_find_by_type(type):
    try:
        cursor.execute("select name from pokemon where type='{}'".format(type))
        result = cursor.fetchall()
        return result
    except(Exception):
        pass



def add_pokemon(pokemon):
    try:
        cursor.execute("insert into pokemon(id,name,height,weight)VALUES(%s,%s,%s,%s)",(pokemon['id'],pokemon["name"],pokemon['height'],pokemon['weight']))
        con.commit()
        return 200
    except(Exception):
        return 400


def delete_pokemon(pok_id):

    try:
        cursor.execute("DELETE from pokemon_type WHERE pokemon_id='{}'".format(pok_id))
        con.commit()
    except:
        res='failed to delete from pokemon_type table ar you sure it exists?'
        return res,400
    try:
        cursor.execute("DELETE from pokemon_owner WHERE pokemon_id='{}'".format(pok_id))
        con.commit()
    except:
        res='failed to delete from pokemon_owner table'
        return res,400
    try:
        cursor.execute("DELETE from pokemon WHERE id='{}'".format(pok_id))
        con.commit()
    except:
        res='failed to delete from pokemon table'
        return res, 400
    return ("deleted",200)

def find_by_name(name):
    try:
        cursor.execute("select id from pokemon where name='{}'".format(name))
        result = cursor.fetchall()
        return result
    except:
        print('failed to search')


def find_by_type(type):
    try:
        cursor.execute("select name from pokemon where id in(select pokemon_id from pokemon_type where pokemon_type='{}')".format(type))
        result = cursor.fetchall()
        return result
    except:
        return 'failed to search'


def find_owners(pokemon):
    try:
        cursor.execute("select name from pokemon_owner where pokemon_id=(select id from pokemon where name ='{}')".format(pokemon))
        result = cursor.fetchall()
        return result
    except(Exception):
        return 'failed to search'


def find_roster(trainer_name):
    try:
        cursor.execute("select pokemon.name from pokemon ,pokemon_owner where pokemon_id=id and pokemon_owner.name='{}'".format(trainer_name))
        result = cursor.fetchall()
        return result
    except(Exception):
        return 'failed to search'


def update_type(type_list, name):
    res="updated"
    try:
        cursor.execute("select id from pokemon where name='{}'".format(name))
        result = cursor.fetchall()
        for type in type_list:
            try:
                cursor.execute("INSERT INTO pokemon_type (pokemon_id, pokemon_type) VALUES (%s,%s)", (result[0], type))
                con.commit()
            except(Exception):
                res="failed updating type"
    except(Exception):
        res= 'could not fined pokemon'
    return res

def evolve_pokemon(name,next_form,trainer,town):
    if trainer in find_owners(name):
        old_form_id=find_by_name(name)
        next_form_id=find_by_name(next_form)
        if next_form_id==():
            info=get_info(next_form)
            try:
                cursor.execute("INSERT INTO pokemon (id, name,height,weight) VALUES (%s,%s,%s,%s)",(info["id"], info["name"], info["height"],info["weight"]))
                con.commit()
                next_form_id=info["id"]
                con.commit()
            except:
                return "failed to add evolved pokemon to db"
        else:
            next_form_id=next_form_id[0][0]
        try:
            cursor.execute("update pokemon_owner set pokemon_id='{}' where name='{}' and town ='{}' and pokemon_id='{}'".format(next_form_id, trainer,town ,old_form_id[0][0]))
            con.commit()
        except:
            return "failed to update pokemon from db"
        return "success"
    else:
        return "trainer has no such pokemon"

# extension 1
# def finds_most_owned():
#     try:
#         cursor.execute("select name from pokemon where id ='(select pokemon_id , count(*) as num from pokemon_owner group by pokemon_id order by num desc fetch first 1 row with ties)'")
#         result = cursor.fetchall()
#         con.commit()
#         return result
#     except(Exception):
#         pass
#     con.commit()
