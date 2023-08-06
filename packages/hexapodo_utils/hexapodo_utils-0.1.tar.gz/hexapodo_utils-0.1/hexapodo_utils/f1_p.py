import json
import os
import re
import string
import random
import pickle
import networkx as nx
import pandas as pd
from io import StringIO
from dask import dataframe, delayed
from smart_open import smart_open


# schema_graph
def obj_name(location):
    """
    Transforms an s3 path into the name of the table it corresponds to. If location is not in the expected format, 
    returns the path

    :param location:
    :return: String
    """
    match = re.search('/(\w+)/?$', location)
    if match is None:
        match = re.search('/(\w+)\.\w+$', location)
        if match is None:
            return location
    
    return match.group(1)

# semantic_table, schema_graph, record_mastering, general_domain_all, category_collapse, deduplication, faida-dask, json_to_parquet
def read_json(loc):

    # checck optionally what the default would be
    if not loc:
        return None

    with smart_open(loc.replace("s3a://", "s3://")) as f:
        content = f.read()
        if type(content) == bytes:
            content = content.decode()
        return json.loads(content)


# benfords_law, summary, schema_graph, record_mastering, number_parsing, hyucc, frequencies, category_collapse, deduplication, faida-candidates
def read_parquet(location):
    """
    Simple wrapper around dask's parquet read

    :param session:
    :param location:
    :return:
    """
    location = location.replace("s3a://", "s3://")
    if location.endswith("/"):
        glob = location + "*.parquet"
    elif location.endswith(".parquet"):
        glob = location
    else:
        glob = location + "/*.parquet"

    return dataframe.read_parquet(glob)


# semantic_table, personal_identifier_tests, personal_identifier_sanitizations, hyucc, hyfd, entity-knowledge-graph, read_parquet
def read_parquet(location, npartitions):
    """
    Simple wrapper around dask's parquet read
    :param session:
    :param location:
    :param npartitions:
    :return:
    """
    location = location.replace("s3a://", "s3://")
    if location.endswith("/"):
        glob = location + "*.parquet"
    elif location.endswith(".parquet"):
        glob = location
    else:
        glob = location + "/*.parquet"

    return dataframe.read_parquet(glob).drop_duplicates().repartition(npartitions=npartitions)

# entity-knowledge-graph, features-extraction-gd
def read_data(location):
    """
    Reads data in parquet format and takes a sample if MAX_DATA_SIZE env variable is set. Otherwise returns the full
    data. Deals with a few different glob configurations
    :param session:
    :param location:
    :return:
    """
    location = location.replace("s3a://", "s3://")
    if location.endswith("/"):
        glob = location + "*.parquet"
    elif location.endswith(".parquet"):
        glob = location
    else:
        glob = location + "/*.parquet"

    data = dataframe.read_parquet(glob)
    max_size = os.environ.get("MAX_DATA_SIZE", None)
    size = data.size.compute()
    if max_size and size > int(max_size):
        p = int(max_size)/size
        data = data.sample(p)
    return data



# benfords_law, summary, personal_identifier_tests, hyucc, hyfd, general_domain_all, frequencies, deduplication, faida-dask
def write_file(text_file, file_location):
    """
    Writes a json file into s3

    :param text_file:
    :param file_location:
    :return:
    """
    location = file_location.replace("s3a://", "s3://")
    with smart_open(location, 'w') as f:
        f.write(text_file)
        # record_mastering (receives the raw file, before json.dumps)
        f.write(json.dumps(text_file, ensure_ascii=False))


# summary, frequencies, knowledge_graph, entity-knowledge-graph, features-extraction-gd, doesn't use read_json
# semantic_table : uses read_json
def read_graph(graph_location):
    '''
    Read a node_link data json into a networkx graph
    :param graph_location:
    :return:
    '''
    graph_location = graph_location.replace("s3a://", "s3://")
    node_link_data = read_json(graph_location)
    graph = nx.readwrite.json_graph.node_link_graph(node_link_data)
    return graph

# knowledge_graph
def write_graph(schema, graph_location):
    """
    Writes a networkx graph into node_link data json

    :param schema:
    :param graph_location:
    :return:
    """
    graph_location = graph_location.replace("s3a://", "s3://")
    json_scheme = nx.readwrite.json_graph.node_link_data(schema)

    with open(graph_location, 'w') as f:
        f.write(json.dumps(json_scheme))


# schema_graph
def path_list_to_dict(path_list):
    path_dict = {}
    for path in path_list:
        table_name = obj_name(path)
        path_dict[table_name] = path
    
    return path_dict


# schema_graph
def read_schema_as_graph(schema_location):
    """
    Read a node_link data json into a networkx graph

    :param schema_location:
    :return: 'Networkx' directed graph
    """
    if schema_location is None:
        return nx.DiGraph()

    schema_location = schema_location.replace("s3a://", "s3://")

    node_link_data = read_json(schema_location).compute()
    graph = nx.readwrite.json_graph.node_link_graph(node_link_data)

    # Relabel nodes to names
    name_to_path = path_list_to_dict(graph.nodes())
    path_to_name = {path:name for name, path in name_to_path.items()}
    graph = nx.relabel_nodes(graph, path_to_name, copy=True)
    nx.set_node_attributes(graph, name="path", values=path_to_name)

    return graph


# summary, frequencies, entity-knowldege-graph, features-extraction.gd
def get_id_typed_columns(input_data, schema_location):
    """
    Returns the columns that represent either primary or foreign keys.

    :param input_data:
    :param schema_location:
    :return:
    """

    schema_graph = read_graph(schema_location)
    table_name = obj_name(input_data)

    primary_columns = set(ids["primary"] for primary_table, foreign_table, ids in schema_graph.edges(data=True)
                    if primary_table.endswith(table_name) or primary_table.endswith(table_name+"/"))
    foreign_columns = set(ids["foreign"] for primary_table, foreign_table, ids in schema_graph.edges(data=True)
                    if foreign_table.endswith(table_name) or foreign_table.endswith(table_name+"/"))

    id_columns = primary_columns.union(foreign_columns)

    return id_columns


# semantic_table, personal_identifier_tests, number_parsing, categgory_collapse, knowledge_graph
# read_human_input: should use the read_json


# semantic_table
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# number_parsing, category_collapse
def write_parquet(df, location):
    """
    Simple wrapper around dask's parquet write
    :param session:
    :param location:
    :return:
    """
    location = location.replace("s3a://", "s3://")
    if location.endswith("/"):
        glob = location[:-1]
    else:
        glob = location

    df.to_parquet(glob)

# semantic_table
def write_partition(df, location):
    partition_location = location + id_generator()
    if not os.path.exists(location):
        os.makedirs(location)
    with smart_open(partition_location.replace("s3a://", "s3://"),'wb') as f:
        for x in df:
            b = (x + "\n").encode()
            f.write(b)


# schema_graph, entity-knowledge-graph
def s3_parse_path(path):
    """
    separates s3 paths into their components, in case they are valid
    :param path: s3 path
    :return: dict with each of the s3 components
    """
    matches = re.search('^s3[a|n]?://([^/]+)/(.*?([^/]+)/?)$', path)
    if matches is not None:
        return {'matches': matches, 'bucket': matches.group(1),
                'file_key': matches.group(2),
                'file_name': matches.group(3)}
    else:
        raise ValueError("Invalid path: {}".format(path))


# entity-knowledge-graph, schema_graph
flatten = lambda l: [item for sublist in l for item in sublist]

# personal_identifier_tests, number_parsing, category_collapse (should be json read)
# get_dataframe_from_json: personal_identifier_sanitizations (doens't have columns, returns all columns)
def read_json_as_pd_df(json_location, columns=[]):
    """
    Read a s3 path containing a json file into a pandas dataframe

    :param json_location:
    :return df: pandas dataframe
    """
    json_data = read_json(json_location)

    df = pd.DataFrame(json_data)

    if not bool(df) and len(columns) > 0:
        intersect_columns = set(columns).intersection(set(df.columns))
        df = df[list(intersect_columns)]

    return df


# general_domain_all
def load_model(input_model_path):
    """
    loads the predictive model for a certain domain

    :param input_model_path:
    :return model:
    """
    byte_array = read_model_as_byte_array(input_model_path)
    model = pickle.loads(byte_array)

    return model


# general_domain_all
def read_model_as_byte_array(input_model):
    """
    Read a s3 path containing a model into a binary array

    :param input_model:
    :return df: pandas dataframe
    """
    model_location = input_model.replace("s3a://", "s3://")

    with smart_open(model_location, "rb") as f:
        bytes_array = bytearray(map(int, f))

    return bytes_array


# entity-knowledge-graph
def write_pandas_to_s3_json(df, file_name, parsed_output, s3):
    """
    Write pandas dataframe to s3 in json format
    Arguments:
        df {[pandas dataframe]} -- [description]
        file_name {[str]} -- [description]
        parsed_output {[dict]} -- [description]
        s3 {[boto3 resource]} -- [description]
    """

    json_buffer = StringIO()
    df.to_json(json_buffer, orient='records', lines=True)
    s3.Object(parsed_output["bucket"], parsed_output["file_key"] + file_name).put(Body=json_buffer.getvalue())