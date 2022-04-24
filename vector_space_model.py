import math
import operator


def get_result_by_vector_space_model(query):
    # Get Idf
    idf = get_idf()

    # Get Weight of Query
    weight_of_query = get_weight_of_query(query, idf)

    # Get Similarity
    similarity = get_similarity(idf, weight_of_query)

    # Sort similarity
    sorted_similarity = sorted(similarity.items(), key=operator.itemgetter(1), reverse=True)

    return sorted_similarity


def get_idf():
    number_of_files_contain_chars = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0}

    # get number of files that contain each char.
    for numberOfDocument in range(10):
        name_of_doc = './files/Doc' + str(numberOfDocument + 1)
        file = open(name_of_doc, "r")
        lines = file.readlines()
        for char in number_of_files_contain_chars:
            # convert list to string
            lines = ''.join(lines)
            exist = lines.find(char)
            if exist is not -1:
                number_of_files_contain_chars[char] += 1

    # get idf
    for char in number_of_files_contain_chars:
        number_of_files_contain_chars[char] = math.log2(10 / number_of_files_contain_chars[char])

    return number_of_files_contain_chars


# ----------------------------- Query Part -------------------------------------------

def get_weight_of_query(query, idf):
    weight_of_query = {'A': 0.0, 'B': 0.0, 'C': 0.0, 'D': 0.0, 'E': 0.0, 'F': 0.0}
    for char in query:
        if char is not ' ':
            weight_of_query[char] += 1

    # get max number in query
    all_values = weight_of_query.values()
    max_value = max(all_values)

    # get weight of query
    for char in weight_of_query:
        weight_of_query[char] = (weight_of_query[char] / max_value) * idf[char]

    return weight_of_query


# ---------------------------------- Document Part ------------------------------------------

def get_similarity(idf, weight_of_query):
    weight_matrix = [{'A': 0., 'B': 0., 'C': 0., 'D': 0., 'E': 0., 'F': 0.} for i in range(10)]
    similarity = {}

    weight_of_query2 = weight_of_query.copy()
    sum_2_times_weight_of_query = get_pow_then_sum(weight_of_query2)

    for numberOfDocument in range(10):
        name_of_doc = './files/Doc' + str(numberOfDocument + 1)
        weight_matrix[numberOfDocument] = get_weight_of_doc(name_of_doc, weight_matrix[numberOfDocument], idf)

        key = 'D' + str(numberOfDocument + 1)
        similarity[key] = 0

        for char in weight_matrix[numberOfDocument]:
            similarity[key] += weight_matrix[numberOfDocument][char] * weight_of_query[char]

        similarity[key] /= math.sqrt(get_pow_then_sum(weight_matrix[numberOfDocument]) * sum_2_times_weight_of_query)

    return similarity


def get_weight_of_doc(name_of_doc, weight_of_doc, idf):
    # read document
    lines = open(name_of_doc, "r")

    # get frequency of char in a file and close the file
    for line in lines:
        for char in line:
            if char != ' ':
                weight_of_doc[char] += 1

    lines.close()

    all_values = weight_of_doc.values()
    max_value = max(all_values)

    for char in weight_of_doc:
        weight_of_doc[char] = (weight_of_doc[char] / max_value) * idf[char]

    return weight_of_doc


def get_pow_then_sum(dic):
    for char in dic:
        dic[char] *= dic[char]

    return sum(dic  .values())
