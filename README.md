# COMP30910 - FYP Design and Implementation
Final year Computer Science with Data Science project.

## PaperMill: A Visual Interface for Managing Research Paper Collections
An essential aspect of the writing process of a literature review is building a collection of relevant papers regarding the topic at hand. This allows a researcher to develop a keen and broad understanding of past work and analysis undertaken. There are many tools available that visualize relationships between academic papers based on properties including citations, authors, and references. However, what these tools lack is the ability to find individual papers within these visualizations, or a recommender system based on a previously established collection.  Using a specially curated dataset containing over four million academic papers, this project will develop a tool that will not only visualize the relationships between publications but will also help users find papers relevant to their search, thanks to an in-built recommender system. The aim of this tool is to expedite the writing process of a literature review, by shortening the time a researcher spends searching for pertinent papers.

## Project Specification
The main objective of this project is to build a visualization tool that shows the relationship between literature reviews. As well as that, it will also contain a recommender system based on various factors. The project specification is broken down into two sections; core and advanced. The core specifications are the basic, yet essential features included in the tool. These features will be focused on first. The advanced specifications refer to the more complex features that will be developed once the core features are properly implemented. Below is a list of the core and advanced specifications.
<br><br>Core:
* Using an appropriate dataset, build a database of papers including metadata, citation graph, publication location, and co-author information.
* Build a visual tool to illustrate the connections between a collection of research papers.
* Allow the user to highlight different types of connections between papers (co-authorship, cited, cited-by, etc.).
* Use the citation graph to recommend papers to a user based on papers collected already by the researcher.
* Collect feedback from trial users on the usefulness of the tool. 

<br><br>Advanced:
* Handle visualization of the network of papers and time in an elegant and intuitive way.
* Use text mining techniques to make content-based recommendations.
* Develop a feature to suggest appropriate publication venues to researchers based on the content of a new paper.
* Allow a user to provide ratings for papers and make recommendations based on these ratings.
* Connect to existing platforms such as Google Scholar, ResearchGate etc. to ingest a researcher's paper collections.
* A completed, well designed controlled user trial that evaluates the usefulness of the tool.

## How to Run
PaperMill is a Django-based web app that connects to a Neo4j database. To setup the project, follow the list of instructions below: <br>
1. A virtual environment should be setup using the libraries listed in the requirements.txt file
2. Install the latest version of Neo4j
3. To begin the data preprocessing, download the DBLP_V11 dataset from [here](https://lfs.aminer.cn/misc/dblp.v11.zip). If you wish to skip the preprocessing, the cleaned data can be downloaded from [here](https://drive.google.com/drive/folders/1tKbVttaWletlF1uTqj_dvNqc9cn2eNWl). If you chose to skip the preprocessing, move to step 5
4. Run the RUNME.ipynb from the virtual environment
    1. If your system has sufficient memory free to hold the similarity matrix (>4GB):
    <br>- In the "Generating Recommender System Framework" section of RUNME.ipynb, set createSimMatrix to False
    <br>- In "src/recommendation/views.py", uncomment line 44
    <br>- In "src/recommendation/views.py", comment line 41
5. Start a new Neo4j project. The following instructions are for Neo4j Desktop:
    1. Start a new project.
    2. Click "Add Database
    3. Click "Create a Local Graph"
    4. Name the graph whatever you like
    2. For password, use: PMVG123
    3. Click "Create"
    4. When the database is created, click the three dots and then "Manage"
    5. Click the "Settings" tab
    6. Overwrite the config here with the contents of the neo4j_conf.txt file
    7. Start the database
    8. Import the "neo4j" data, using the Cypher queries listed in the cypher_queries.txt file
6. In command line/Powershell/Terminal, activate the virtual environment and move to the "src" directory
7. In the command line, create a Django admin user: `python manage.py createsuperuser`
8. Initiate the SQLite database: `python manage.py makemigrations` followed by `python manage.py migrate`
9. Run the app: `python manage.py runserver`
10. In your web browser, go to: 127.0.0.1
