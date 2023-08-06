# yomi
A collection of tools for running tournaments of AI agents against each-other on various games

## Install

```
pipenv install yomi
```

### Local Development

For local work, setting up a new `Pipfile` and `Pipfile.lock` can be acomplished via:

```
pipenv install -e .
pipenv install --dev -e .[dev]
```

## Example

Running an example `random_unlimited_tournament`
```
from yomi.base import random_unlimited_tournament
from yomi.agents import RandomAgent
from yomi.games import TicTacToe

results = random_unlimited_tournament(TicTacToe, ((RandomAgent, {'name': 'p1'}), (RandomAgent, {'name': 'p2'})))
print(results[0].mean())
```

## Testing

```
pytest
```

```
flake8
```
