import sys
import os
import functools
import string
import stringdist
import jellyfish
import hashlib
from collections import Counter
from operator import mul
import math
import re

_no_bytes_err = 'expected str, got bytes'


# extracted from jellyfish package for multiple workers purposes
# https://pypi.org/project/jellyfish/
# value_correspondance, schema_graph, category_collapse
# value_correspondence, schema_graph (change function's name from from jaro_distance to jaro_similarity)
# jaro_similarity: category_collapse 
def jaro_similarity(s1, s2, boost_threshold=0.7):
    """
    :param s1:
    :param s2:
    :return: the jaro distance  of string1 and string2
    """
    return round(jellyfish.jaro_winkler(s1, s2, False, False, boost_threshold), 2)


# value_correspondence, schema_graph, category_collapse, faida-candidates
def ngrams(word, n):
    """
    :param word:
    :param n:
    :return: returns list of n-grams of the input word
    """
    if n < len(word):
        return [word[i:i+n] for i in range(len(word)-n+1)]
    else:
        return [word]

# value_correspondence, schema_graph, category_collapse, faida-candidates
def merge(A, B, f):
    """
    :param A:
    :param B:
    :param f:
    :return: a dictionary with the intersection of keys in A and B, with a function applied to it's values
    """
    # Start with symmetric difference; keys either in A or B, but not both
    merged = {k: f(A[k], B[k]) for k in A.keys() & B.keys()}
    return merged

# value_correspondence, schema_graph, faida-candidates (change cosine_distance name to cosine_similarity)
# cosine_similarity category_collapse
def cosine_similarity(s1, s2, q=2):
    """
    Computes de cosine similarity using the q-grams of s1 and s2
    :param s1: string 1
    :param s2: string 2
    :param q: integer to compute the n-grams
    :return:
    """
    nv1 = Counter(ngrams(s1,q))
    nv2 = Counter(ngrams(s2,q))
    v1v2 = merge(nv1, nv2, mul)
    v1v2_dot = sum(v1v2.values())
    v1_square = math.sqrt(sum(map(lambda x: x*x, nv1.values())))
    v2_square = math.sqrt(sum(map(lambda x: x*x, nv2.values())))
    return round(float(v1v2_dot)/(v1_square*v2_square),2)

# category_collapse
def levenshtein_similarity(s1, s2):
    """
    Computes the normalized levenshtein distance between a pair of strings

    :param s1: string1
    :param s2: string2
    :return:
    """
    lev_norm = stringdist.levenshtein_norm(s1, s2)
    if math.isnan(lev_norm):
        return 1
    else:
        return (1-lev_norm)

# category_collapse
def ensembled_similarity(s1, s2):
    """
    Computes an embeded similarity (jaro, cosine & levenshtein) between a pair of strings

    :param s1: string1
    :param s2: string2
    :return:
    """
    sim1 = levenshtein_similarity(s1, s2)
    sim2 = cosine_similarity(s1, s2)
    sim3 = jellyfish.jaro_distance(s1, s2)
    sum_sim = sim1+sim2+sim3
    return sum_sim/3


# hyucc, hydf, faida-dask
def hash_(x):
    x_bytes = str(x).encode()
    hashed = hashlib.md5(x_bytes)
    return int.from_bytes(hashed.digest(), byteorder="big", signed=False)

# schema_graph
def get_distance_metric(zip_cols, name_source, name_target, dist_type="cosine"):
    """
    calculates useful distances between table names and columns to determine the primary and foreign keys

    :param zip_cols: list of tuples where tuple corresponds to faida outcomes on the form (foreign, primary) columns
    :param name_source:
    :param name_target:
    :param dist_type: either cosine or jaro
    :return:
    """
    dist_func = cosine_similarity if dist_type == "cosine" else jellyfish.jaro_distance
    dist_tuples = [(dist_func(ding, name_source),
                    dist_func(ded, name_target),
                    dist_func(ding, name_target),
                    dist_func(ded, name_source),
                    dist_func(ded, ding)) for ded, ding in zip_cols]

    return dist_tuples

# category_collapse
def text_cleaner_remove_accents(x):
    """
    :param x:
    :return: a basic clean for text comparison
    """
    x = str(x)
    x = x.lower()
    x = re.sub('[^A-Za-z0-9áéíóúü]+', '', x)
    x = re.sub('á','a', x)
    x = re.sub('é','e', x)
    x = re.sub('í','i', x)
    x = re.sub('ó','o', x)
    x = re.sub('ú','u', x)

    return x

# value_correspondence, schema_graph
def text_cleaner(x):
    """
    :param x:
    :return: a basic clean for text comparison
    """
    x = str(x)
    x = x.lower()
    x = re.sub('[^A-Za-z0-9áéíóúü]+', '', x)
    return x

# personal_identifier_sanitizations
def get_cleaned_personal_identifier(x):
    """
    Returns upper case cleaned personal identifiers (CURP, RFC, NSS)
    :param x:
    :return:
    """
    return str(x).strip().upper().replace('-', '').replace(' ', '')


# personal_identifier_tests
def clean_text(values):
    """
    Eliminates dashes and blank spaces, changes all to uppercase

    :param values: column to clean
    :return: cleaned text
    """
    return [get_cleaned_personal_identifier(value) for value in values]


# obj_name_p
# must accept paths ending with /, paths ending with path/file.parquet



# summary, frequencies
# this changes because when files are read from tests they have .parquet in file path
def obj_name_parquet(location):
    # TODO:improve the way we obtain the name of the table associated to the path
    if re.search('/(\w+)/?$', location) is not None:
        table_name = re.search('/(\w+)/?$', location).group(1)
    else:
        table_name = re.search('/(\w+)?.parquet$', location).group(1)

    return table_name

# semantic_table, frequencies, entity-knowledge-graph, features-extraction-gd
def obj_name_pointless(location):
    return re.search('/(\w+)/?$', location).group(1)

def obj_name_last_name(location):
    last_name = re.search('/([\w\.]+)/?$', location).group(1)
    if last_name.endswith(".parquet"):
        last_name = last_name.replace(".parquet", "")
    return last_name

def obj_name_last_name_sh(location):
    last_name = re.search('/([\w\.]+)/?$', location).group(1)

    if location.endswith("/"):
        last_name = last_name[:-1]
    elif last_name.endswith(".parquet"):
        last_name = last_name.replace(".parquet", "")
    else:
        pass
    return last_name


# knowledge_graph
def obj_name_path_to_name_pointless(location):
    """
    Transforms an s3 path into the name of the table it corresponds to.

    :param location:
    :return: String
    """
    return re.search('/(\w+)/?$', location).group(1)


# schema_graph
def obj_name_path_to_name_point(location):
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








