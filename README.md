## Dependencies and Running the Project

### Dependencies
This project requires Python and several Python packages. If you haven't installed Python yet, you can download it from the official website: https://www.python.org/downloads/

After installing Python, you can install the required packages using pip. Open your terminal and run the following commands:
`pip install copy`
`pip install time`
`pip install tabulate`
`pip install tkinter`
`pip install CustomTkinter`
N.B. .CSV files must be compatible to our format, for the sake of testing just use the files in the diractory
## Running the Project
`python ./ProblemGUI.py`

# Agriculture Problem Solver

## Overview
This project is an application of various search algorithms to solve an agriculture problem. The primary focus is to optimize the organization of agricultural production in Algeria.

## Objective
The aim is to optimize various aspects of agricultural production, including:

1. Minimizing consumer prices
2. Maximizing production output
3. Achieving self-sufficiency in product production

These objectives require careful consideration and definition. For instance, the lowest price for the consumer needs a meaningful definition, and the focus of maximizing production could be on specific or strategic products.

## Methodology
The project involves:

- Analyzing the agricultural capabilities of each city/Wilaya, including its yearly production, land usage for agriculture, crop types, and productivity.
- Understanding the country's consumption patterns for main products such as wheat, corn, dates, potatoes, tomatoes, green pepper, aubergines, etc.
- Observing the seasonal changes in product prices.

The project applies different search strategies, including two uninformed strategies, A* or IDA*, and Hill Climbing. The goal is to find the best assignment of agricultural production in the country. Comparative analyses are performed to evaluate the search strategies in terms of solution quality, time, and space requirements.

The problem is also approached as a constraint-satisfaction problem using techniques discussed in the course. The results from both approaches are then compared.

## Files

### AgricultureProblem.py
This file contains the `AgricultureProblem` class which defines the problem to be solved. It includes methods for defining the initial state, goal state, and possible actions.

### City.py
This file contains the `City` class which represents a city in the problem. Each city has a name, a list of products it can produce, and a list of neighboring cities.

### Country.py
This file contains the `Country` class which represents the entire country. It includes a list of all cities and methods for adding cities and finding a city by name.

### DataLoader.py
This file contains the `DataLoader` class which is responsible for loading data from CSV files. It includes methods for loading city data and product data.

### GraphSearch.py
This file contains the `GraphSearch` class which implements various search algorithms including IDA_Star, IDS, steepest, and UCS.

### main.py
This is the main entry point of the application. It creates an instance of the `App` class from `ProblemGUI.py` and starts the GUI.

### Node.py
This file contains the `Node` class which represents a node in a search algorithm. Each node has a state, a parent node, an action that led to it, a cost, a priority, and a depth.

### ProblemGUI.py
This file contains the `App` class which is a subclass of `tk.Tk`. This class creates and manages the GUI for the application.

### Product.py
This file contains the `Product` class which represents a product that can be produced by a city. Each product has a name, a production value, a strategic value, a removable value, a productivity value, and a list of seasons it can be produced in.

### DataStructures.py
This file contains the `PriorityQueue`, `stack`, and `queue` classes which are used in the search algorithms.

## Instructions for Use
To run the project, execute the `main()` function in the `main.py` file. The GUI will appear. Use the "Upload Wilaya CSV" and "Upload Product CSV" buttons to upload the necessary data. Select a search method from the dropdown menu and click "Search". The results will be displayed in the text field. You can save the results to a CSV file by clicking "Save to CSV".

## Data
The project uses data loaded from the `DataLoader` class. The data includes information about cities, consumption, and prices.

## Dependencies
The project requires the following Python libraries: `copy`, `time`, `tabulate`, and `markdown`.
