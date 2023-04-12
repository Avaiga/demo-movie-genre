import taipy as tp
import pandas as pd
from taipy import Config, Scope, Gui

# Create a Taipy App that will output the 7 best movies for a genre

# Taipy Core - backend definition

# Filter function for Task
def filtering_genre(initial_dataset: pd.DataFrame, selected_genre):
    filtered_dataset = initial_dataset[initial_dataset['genres'].str.contains(selected_genre)]
    filtered_data = filtered_dataset.nlargest(7, 'Popularity %')
    return filtered_data


# Input Data Nodes configuration
initial_dataset_cfg = Config.configure_data_node(id="initial_dataset",
                                                 storage_type="csv",
                                                 path="data.csv",
                                                 scope=Scope.GLOBAL)

selected_genre_cfg = Config.configure_data_node(id="selected_genre_node",
                                                 default_data="ACTION",
                                                 scope=Scope.GLOBAL)

# Output Data Node configuration
filtered_data_cfg = Config.configure_data_node(id="filtered_data",
                                                 scope=Scope.GLOBAL)


# Task configuration
filter_task_cfg = Config.configure_task(id="filter_genre",
                                            function=filtering_genre,
                                            input=[initial_dataset_cfg, selected_genre_cfg],
                                            output=filtered_data_cfg,
                                            skippable=True)

# Pipeline configuration
pipeline_cfg = Config.configure_pipeline(id="pipeline",
                                         task_configs=[filter_task_cfg])
# Scenario configuration
scenario_cfg = Config.configure_scenario(id="scenario", pipeline_configs=[pipeline_cfg])

# Run of the Taipy Core service
tp.Core().run()

# Creation of my scenario
scenario = tp.create_scenario(scenario_cfg)



#Taipy GUI- front end definition

# Callback definition
def modify_df(state):
    scenario.selected_genre_node.write(state.selected_genre)
    tp.submit(scenario)
    state.df = scenario.filtered_data.read()    

# Get list of genres
list_genres = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy', 'IMAX', 'Romance',
               'Sci-FI', 'Western', 'Crime', 'Mystery', 'Drama', 'Horror', 'Thriller', 'Film-Noir',
               'War', 'Musical', 'Documentary']

# Initialization of variables
df = pd.DataFrame(columns=['Title', 'Popularity %'])
selected_genre = None

# movie_genre_app
movie_genre_app = """
# Film recommendation

## Choose your favorite genre
<|{selected_genre}|selector|lov={list_genres}|on_change=modify_df|dropdown|>

## Here are the top 7 picks
<|{df}|chart|x=Title|y=Popularity %|type=bar|title=Film Popularity|>
"""
# run the app
Gui(page=movie_genre_app).run()