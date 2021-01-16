from datapackage import Package
import requests

# package = Package('https://datahub.io/sports-data/english-premier-league/datapackage.json')

# # print list of all resources:
# print(package.resource_names)

# # print processed tabular data (if exists any)
# for resource in package.resources:
#     if resource.descriptor['datahub']['type'] == 'derived/csv':
#         print(resource.read())

def get_referees():
    response = requests.get("https://pkgstore.datahub.io/sports-data/english-premier-league/season-1819_json/data/175e7265560b9ab9102566c5dae7cbf3/season-1819_json.json")
    response.raise_for_status()
    # reponse is a list of games
    jsonResponse = response.json()
    referees = set()
    for game in jsonResponse:
        referees.add(game["Referee"])
    return referees

if __name__ == "__main__":
    get_referees()