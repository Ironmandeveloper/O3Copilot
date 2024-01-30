"""
This class, LabelSearch, provides functionality for searching labels within a given query. It allows for both
direct word matching and pattern-based matching using regular expressions for case-insensitive label detection.

Class:
- LabelSearch: Searches for labels within an input query.

Methods:
- __init__: Initializes the LabelSearch object with a list of labels.
- search: Searches for labels in a given query, supporting direct word matching and pattern-based matching.

Usage:
1. Create an instance of LabelSearch by providing a list of labels.
2. Use the 'search' method to find matching labels in a given query.

Example:
    label_search = LabelSearch({'kpi','plant', 'line', 'unit','machine','availability', 'olp', 'opf', ...})
    query = "give me table and pie chart of of top 5 lines which have best oee in plant orp from  7 oct 2023 8:10pm to 8 oct 2023 9:23am"
    matching_labels = label_search.search(query)
    print(matching_labels)
    # Output: ['plant', 'orp']
    
Author: Sahil
Date: 19 Nov 2023
"""

import re
class LabelSearch:
    def __init__(self, labels):
        """
        Initializes the LabelSearch object.

        Args:
            labels (list): List of labels to search for.
        """
        self.labels = set(label.lower() for label in labels)
        self.label_patterns = [re.compile(r'\b{}\b'.format(re.escape(label)), re.IGNORECASE) for label in labels]


    def search(self, query):
        """
        Searches for labels in the given query.

        Args:
            query (str): Input query.

        Returns:
            list: List of matching labels found in the query.
        """
        words = query.lower().split()
        matching_words = {word for word in words if word in self.labels}
        if not matching_words:
            # Try using regular expressions to match labels with variations
            for pattern in self.label_patterns:
                matching_words.update(set(pattern.findall(query)))
        return list(matching_words)