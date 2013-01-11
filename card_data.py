REPLACEMENTS = [
    ('\xe2\x80\x94', '-'),
    ]

class CardDatabase(object):
    def __init__(self):
        self.data = {}

    def __init__(self, fname):
        self.data = {}
        self.read_from_file(fname)

    def read_from_file(self, fname):
        separator = '||'
        desired_cols = ["set", "type", "power", "toughness", "loyalty", "converted_manacost", "artist", "flavor", "color", "rarity"]
        key = "name"
        csv_data = open(fname).read()
        # Some of the data is strange, so apply the replacements as given at the top of the file
        for old, new in REPLACEMENTS:
            csv_data = csv_data.replace(old, new)
        # First line is garbage
        lines = csv_data.splitlines()[1:]
        # second line has the column headers
        col_names = lines[0].split(separator)[:-1]

        for line in lines[1:]:
            fields = line.split(separator)[:-1]
            temp_data = dict(zip(col_names, fields))
            self.data[temp_data[key]] = dict((k, temp_data[k]) for k in desired_cols if temp_data[k] != "")
