# Ovomaltino

[![Latest Version](https://img.shields.io/pypi/v/Ovomaltino.svg)](https://pypi.org/project/Ovomaltino/)
[![LGPLv3 License](https://img.shields.io/badge/license-LGPLv3-blue.svg)]()
[![Build Status](https://img.shields.io/github/workflow/status/Ovomaltino/Ovomaltino/ci)](https://github.com/Ovomaltino/Ovomaltino/actions?query=workflow%3Aci)
[![Codecov](https://img.shields.io/codecov/c/github/Ovomaltino/Ovomaltino)](https://codecov.io/gh/Ovomaltino/Ovomaltino)

## **What is it?**

**ovomaltino is** a multi-agent system model capable of evolving through **sociological concepts** and the exposure to an external, unknown and uncontrolled system without the need for a training, standard or previously established objective. It is intended to be a **fully integrable** and **standalone** machine learning block, providing **a simple and scalable model.** it’s born from a scientific research and can be (found here)[https://www.fatecsaocaetano.edu.br/fascitech/index.php/fascitech/article/view/183/142](found here).

## **Where to get it**

The source code is currently hosted on GitHub at: [https://github.com/Ovomaltino/Ovomaltino](https://github.com/Ovomaltino/Ovomaltino)

Binary installers for the latest released version are available at the [Python Package Index (PyPI)](https://pypi.org/project/Ovomaltino) and on [Conda](https://docs.conda.io/en/latest/).

```
# conda
conda install ovomaltino

```

```
# or PyPI
pip install ovomaltino

```

## **License**
[GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.pt-br.html)

## **Getting Help**

For usage questions, the best way is to see the [Velh-IA Project](https://github.com/ccr5/Velh-IA), which implemented Ovomaltino or search on StackOverflow. In addition, general questions and discussions can also be sent to maintainers.

## Usage

Read [scientific research article](https://www.fatecsaocaetano.edu.br/fascitech/index.php/fascitech/article/view/183/142) to understand how it really works. However, after to install Ovomaltino, you need to import on your code:

```python
from ovomaltino.ovomaltino import Ovomaltino
```

So, the next step is to create an ovaltine object passing information from the API. The Ovomaltino organization makes a template API using MongoDB available for use.

```python
mas = Ovomaltino("localhost", 3005, "v1")
```

Now we have all settings done. So, the next step is load Ovomaltino.

```python
mas.load(
	5, # Number of agents in MAS (Multi Agent System)
	[0, 1, 2, 3, 4, 5, 6, 7, 8], # List of request values of the external environment
	# Dict with all external environment response and 
  # its consequence to the MAS's agents
	{  
	  'WINNER': {'consequence': 0},
		'DRAW': {'consequence': 0},
		'LOSER': {'consequence': -1}
	}
)
```

Send values to Education social fact on MAS 

```python
mas.observe(
	# request values passed to other users of the external environment
	[-1,-1,-1,-1,-1,-1,-1,-1,-1],
	# response passed to other user users of the external environment 
	4,
	# Old value to search
	1,
	# New value to set
	0
)
```

Interacting with the multi-agent system

```python
# Send a status of external environment to get a action
mas_action = mas.process([-1, -1, -1, 1, -1, 0, 1, -1, 0])

# Save the MAS status
mas_action['save']()

# Rollback if something wrong happened
mas_action['rollback']()
```

## **Discussion and Development**

Most development discussions take place on GitHub in this repo.

## **Contributing to pandas**

All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.

A detailed overview on how to contribute can be found in the **[contributing guide](https://github.com/Ovomaltino/Ovomaltino/blob/main/CONTRIBUTING.md)**.

If you are simply looking to start working with the pandas codebase, navigate to the [GitHub "issues" tab](https://github.com/Ovomaltino/Ovomaltino/issues) and start looking through interesting issues. There are a number of issues listed under [Docs](https://github.com/Ovomaltino/Ovomaltino/issues?labels=Docs&sort=updated&state=open) and [good first issue](https://github.com/Ovomaltino/Ovomaltino/issues?labels=good+first+issue&sort=updated&state=open) where you could start out.
