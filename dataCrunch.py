import csv

class ObjectifyCSV(object):
    """
    object for parsing a csv file
    """

    def __init__(self, path):
        """
        input parameter:    path
        description:        relative path from the python file running to
                            the target csv file
        """

        self.data = {}
        self.headers = []

        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    for header in row:
                        self.data[header] = {}
                        self.headers.append(header)
                else:
                    col_count = 0
                    for entry in row:
                        header = self.headers[col_count]
                        self.data[header][line_count] = entry
                        col_count += 1
                line_count += 1

    def get_by_field(self, filter, return_fields=None):
        """
        input parameter:    filter
        description:

        optional input:     return_fields
        description:
        """

        if return_fields is None:
            return_fields = self.headers

        results = []
        keys = set()

        # search for any key that matches a filter and add it to the keys set
        for header, sets in self.data.items():
            for key, value in sets.items():
                if header in filter:
                    if filter[header] == value:
                        keys.add(key)

        for key in keys:
            row = []
            for header in return_fields:
                row.append(self.data[header][key])
            results.append(row)

        return results


if __name__ == "__main__":
    test = ObjectifyCSV('data/listings.csv')

    QA = test.get_by_field({'CITY': 'Seattle', 'ZIP OR POSTAL CODE': '98109'}, ['ADDRESS', 'BEDS', 'PRICE'])
    for row in QA:
        print(row)
