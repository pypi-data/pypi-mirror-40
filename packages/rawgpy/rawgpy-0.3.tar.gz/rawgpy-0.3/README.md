# rawgpy - RAWG python api wrapper

this is a small wrapper fpr the https://RAWG.io (game database) API

usage:
initialize API:

`rawg = RAWG("<user-agent-here>")` please supply a User-Agent that describes your project

search for a game:

`results = rawg.search("<game name here>")` searches for the game, and returns a list of (5) results

if you want to limit the number of results, you can chage that by doing:

`results = rawg.search("<game name here>", num_results=2)`

the results are GameResult objects, whihc contain all attribute the API supplies

you can request more info for a game with

`game = results[0]`
`game.populate()`