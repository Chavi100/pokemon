import requests


def get_next_form(name):
   link = "https://pokeapi.co/api/v2/pokemon/"+name
   info = requests.get(link, verify=False).json()
   species=info["species"]
   link=species["url"]
   info=requests.get(link, verify=False).json()
   avolution_chain=info["evolution_chain"]
   link =avolution_chain["url"]
   info=requests.get(link, verify=False).json()
   evolv=info['chain']['evolves_to'][0]['species']['name']
   return evolv

def get_info(name):
   link = "https://pokeapi.co/api/v2/pokemon/" + name
   info = requests.get(link, verify=False).json()
   return  info