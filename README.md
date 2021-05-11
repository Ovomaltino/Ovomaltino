# Ovomaltino

[![Latest Version](https://img.shields.io/pypi/v/Ovomaltino.svg)](https://pypi.org/project/Ovomaltino/)
[![LGPLv3 License](https://img.shields.io/badge/license-LGPLv3-blue.svg)]()
[![Build Status](https://img.shields.io/github/workflow/status/Ovomaltino/Ovomaltino/ci)](https://github.com/Ovomaltino/Ovomaltino/actions?query=workflow%3Aci)
[![Codecov](https://img.shields.io/codecov/c/github/Ovomaltino/Ovomaltino)](https://codecov.io/gh/Ovomaltino/Ovomaltino)

multiagent system model using sociological theories for AI learning
Project page:	https://github.com/Ovomaltino/Ovomaltino


## Usage
```
from ovomaltino.ovomaltino import Ovomaltino

# Set API data
mas = Ovomaltino("localhost", 3005, "v1")

# Load Ovomaltino with interactions data
mas.load(5, [0, 1, 2, 3, 4, 5, 6, 7, 8], 
		{'WINNER': {'consequence': 0},
		 'DRAW': {'consequence': 0},
		 'LOSER': {'consequence': -1}})

# Passing data to the social fact Education
mas.observe([-1,-1,-1,-1,-1,-1,-1,-1,-1], 4, 1, 0)

# Interacting with the multi-agent system
mas_action = mas.process(game_status)
mas_action['save']()
mas_action['rollback']()
```
