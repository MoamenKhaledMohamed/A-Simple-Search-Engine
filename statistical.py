import operator


def get_results_of_search(query):
    # Filter Query and get its weight
    weight_of_query = get_weight_of_query(query)

    # Generate Weight Matrix and get similarity between docs.
    similarity = get_similarity_between_docs(weight_of_query)

    # Sort similarity
    sorted_similarity = sorted(similarity.items(), key=operator.itemgetter(1), reverse=True)

    return sorted_similarity


# ----------------------------- Query Part -------------------------------------------


# Filter Query and get its weight
def get_weight_of_query(query):
    weight_of_query = {'A': 0., 'B': 0., 'C': 0., 'D': 0., 'E': 0., 'F': 0.}

    # Remove <, :, and > from query
    # example <B:0.3;C:0.2> to B0.3;C0.2
    query = query.replace('<', '')
    query = query.replace(':', '')
    query = query.replace('>', '')

    # split query to array of strings
    # example B0.3;C0.2 to ['B0.3', 'C0.2']
    query = query.split(';')

    # insert values to weight_of_query
    for sub_query in query:
        weight_of_query[sub_query[0]] = float(sub_query[1:])

    return weight_of_query


# ---------------------------------- Document Part ------------------------------------------

# Generate weight matrix
def get_similarity_between_docs(weight_of_query):
    weight_matrix = [{'A': 0., 'B': 0., 'C': 0., 'D': 0., 'E': 0., 'F': 0.} for i in range(10)]
    similarity = {}

    for numberOfDocument in range(len(weight_matrix)):
        name_of_doc = './files/Doc' + str(numberOfDocument + 1)
        frequency_of_chars = get_frequency_of_chars(name_of_doc)
        key = 'D' + str(numberOfDocument + 1)
        similarity[key] = 0
        for char in weight_matrix[numberOfDocument]:
            weight_matrix[numberOfDocument][char] = (frequency_of_chars[char] / frequency_of_chars['length'])
            weight_matrix[numberOfDocument][char] *= weight_of_query[char]
            similarity[key] += weight_matrix[numberOfDocument][char]

    return similarity


# create method take document's name and return dictionary contain the number of chars.
def get_frequency_of_chars(name_of_doc):
    frequency_of_chars = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'length': 0}

    # read document
    lines = open(name_of_doc, "r")

    # get frequency and close the file
    for line in lines:
        for char in line:
            if char != ' ':
                frequency_of_chars[char] += 1
                frequency_of_chars['length'] += 1

    lines.close()

    return frequency_of_chars
