#Import des bibliotheques
import requests
import csv
from flask import Flask, jsonify
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

collection_url = 'https://api.geekdo.com/xmlapi/collection/megtrinity'

app = Flask(__name__)

@app.route('/')
def allDetail():
    return 'Pour acceder à la liste des jeux allez sur http://127.0.0.1:5000/games' 

@app.route('/games', methods=['GET'])
def gameDetail():
    response = requests.get(collection_url)
    xml_data = response.text
    root = ET.fromstring(xml_data)
    games = []

  
    for item in root.findall(".//item"):
        game_id = item.get("objectid")
        title_element = item.find(".//name")
        if title_element is not None:
            title = title_element.text
        else:
            title = "N/A"

        published_year_element = item.find(".//yearpublished")
        if published_year_element is not None:
            published_year = published_year_element.text
        else:
            published_year = "N/A"



        min_players_element = item.find(".//stats").attrib.get('minplayers')
        max_players_element = item.find(".//stats").attrib.get('maxplayers')
        players = f"{min_players_element} - {max_players_element}"
        min_playtime_element = item.find(".//stats").attrib.get('minplaytime')
        max_playtime_element = item.find(".//stats").attrib.get('maxplaytime')
        playtime = f"{min_playtime_element} - {max_playtime_element}"
        thumbnail_element = item.find(".//thumbnail")
        thumbnail = thumbnail_element.text

     
        game_info = {
            'id': game_id,
            'title': title,
            'lst_published_year': published_year,
            'players': players,
            'playtime': playtime,
            'thumbnail': thumbnail,
        }

        games.append(game_info)

    return jsonify(games)

@app.route('/games/<int:game_id>', methods=['GET'])
def idgame(game_id):
    response = requests.get( f"https://api.geekdo.com/xmlapi/boardgame/{game_id}")
    xml_data = response.text
    root = ET.fromstring(xml_data)
    games = []
    
    for item in root.findall(".//boardgame"):
        description = item.find(".//description").text
        game_id = item.get("objectid")
        title_element = item.find(".//name")
        title = title_element.text
        image = item.get("image") 
       
    
        game_info = {
            'categories' : ','.join([cat.text for cat in root.findall('.//boardgamecategory')]),
            'description' : description,
            'expansions': [exp.text for exp in root.findall('.//boardgameexpansion')],
            'id': game_id,
            'image' : image,
            'players': f"{root.find('.//minplayers').text} - {root.find('.//maxplayers').text}",
            'playtime': f"{root.find('.//minplaytime').text} - {root.find('.//maxplaytime').text}",
            'title': title,
            

        }

    games.append(game_info)

    return games

if __name__ == '__main__':
    app.run(debug=True)
