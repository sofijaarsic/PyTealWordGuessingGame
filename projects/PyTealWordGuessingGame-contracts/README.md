# PyTealWordGuessingGame-contracts

This project has been generated using AlgoKit. See below for default getting started instructions.

# Setup

For an interactive guided walkthrough of the project install [CodeTour](https://marketplace.visualstudio.com/items?itemName=vsls-contrib.codetour) in VS Code and run the `Getting Started with Your AlgoKit Project` tour in the `CodeTour` in Explorer panel in your VSCode instance.

### Initial setup

1. Clone this repository locally
2. Install pre-requisites:
   - Make sure to have [Docker](https://www.docker.com/) installed and running on your machine.
   - Install `AlgoKit` - [Link](https://github.com/algorandfoundation/algokit-cli#install): The minimum required version is `1.1`. Ensure you can execute `algokit --version` and get `1.1` or later.
   - Bootstrap your local environment; run `algokit bootstrap all` within this folder, which will:
     - Install `Poetry` - [Link](https://python-poetry.org/docs/#installation): The minimum required version is `1.2`. Ensure you can execute `poetry -V` and get `1.2`+
     - Run `poetry install` in the root directory, which will set up a `.venv` folder with a Python virtual environment and also install all Python dependencies
     - Copy `.env.template` to `.env`
   - Run `algokit localnet start` to start a local Algorand network in Docker. If you are using VS Code launch configurations provided by the template, this will be done automatically for you.
3. Open the project and start debugging / developing via:
   - VS Code
     1. Open the repository root in VS Code
     2. Install recommended extensions
     3. Hit F5 (or whatever you have debug mapped to) and it should start running with breakpoint debugging.
        > **Note**
        > If using Windows: Before running for the first time you will need to select the Python Interpreter.
        1. Open the command palette (Ctrl/Cmd + Shift + P)
        2. Search for `Python: Select Interpreter`
        3. Select `./.venv/Scripts/python.exe`
   - JetBrains IDEs (please note, this setup is primarily optimized for PyCharm Community Edition)
     1. Open the repository root in the IDE
     2. It should automatically detect it's a Poetry project and set up a Python interpreter and virtual environment.
     3. Hit Shift+F10|Ctrl+R (or whatever you have debug mapped to) and it should start running with breakpoint debugging. Please note, JetBrains IDEs on Windows have a known bug that in some cases may prevent executing shell scripts as pre-launch tasks, for workarounds refer to [JetBrains forums](https://youtrack.jetbrains.com/issue/IDEA-277486/Shell-script-configuration-cannot-run-as-before-launch-task).
   - Other
     1. Open the repository root in your text editor of choice
     2. In a terminal run `poetry shell`
     3. Run `python -m smart_contracts` through your debugger of choice

### Subsequently

1. If you update to the latest source code and there are new dependencies you will need to run `algokit bootstrap all` again
2. Follow step 3 above

> For guidance on `smart_contracts` folder and adding new contracts to the project please see [README](smart_contracts/README.md) on the respective folder.

# Tools

This project makes use of Python to build Algorand smart contracts. The following tools are in use:

- [Algorand](https://www.algorand.com/) - Layer 1 Blockchain; [Developer portal](https://developer.algorand.org/), [Why Algorand?](https://developer.algorand.org/docs/get-started/basics/why_algorand/)
- [AlgoKit](https://github.com/algorandfoundation/algokit-cli) - One-stop shop tool for developers building on the Algorand network; [docs](https://github.com/algorandfoundation/algokit-cli/blob/main/docs/algokit.md), [intro tutorial](https://github.com/algorandfoundation/algokit-cli/blob/main/docs/tutorials/intro.md)
- [Beaker](https://github.com/algorand-devrel/beaker) - Smart contract development framework for PyTeal; [docs](https://beaker.algo.xyz), [examples](https://github.com/algorand-devrel/beaker/tree/master/examples)
- [PyTEAL](https://github.com/algorand/pyteal) - Python language binding for Algorand smart contracts; [docs](https://pyteal.readthedocs.io/en/stable/)
- [AlgoKit Utils](https://github.com/algorandfoundation/algokit-utils-py) - A set of core Algorand utilities that make it easier to build solutions on Algorand.
- [Poetry](https://python-poetry.org/): Python packaging and dependency management.

It has also been configured to have a productive dev experience out of the box in [VS Code](https://code.visualstudio.com/), see the [.vscode](./.vscode) folder.
- [AlgoKit Tealer Integration](https://github.com/algorandfoundation/algokit-cli/blob/main/docs/features/tasks/analyze.md): AlgoKit Tealer Integration is a feature in the CLI that allows you to run [Tealer](https://github.com/crytic/tealer) static analyzer on your TEAL
source code. The invocation of this command is included in:
- The github actions workflow file.
- A VSCode task ('Shift+CMD|CTRL+P' and search for 'Tasks: Run Task' and select 'Analyze TEAL contracts with AlgoKit Tealer integration').
- A `pre-commit` hook (if you have enabled `pre-commit` in your project). 
