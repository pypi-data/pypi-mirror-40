import requests
import json
from .game_result import GameResult


class RAWG:

    def __init__(self, user_agent):
        self.user_agent = user_agent

    def request(self, param: str, url="https://api.rawg.io/api/games"):
        headers = {
            'User-Agent': self.user_agent
        }
        response = requests.get(url + param, headers=headers)
        return json.loads(response.text)

    def search_request(self, query, num_results=1):
        param = "?page_size={num}&search={query}&page=1".format(
            num=num_results, query=query)
        return self.request(param)

    def game_request(self, name):
        param = "/{name}".format(name=name)
        return self.request(param)

    def search(self, query, num_results=5):
        json = self.search_request(query, num_results)
        results = [GameResult(j, self.user_agent)
                   for j in json.get("results", [])]
        return results


if __name__ == "__main__":
    r = RAWG("RAWG-python-wrapper-test")
    g = r.search("Warframe")
    g[0].populate()
    while True:
        exec(input(">>>"))
