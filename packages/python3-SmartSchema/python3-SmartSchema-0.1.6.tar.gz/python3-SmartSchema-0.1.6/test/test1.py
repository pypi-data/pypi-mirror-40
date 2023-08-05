from SmartSchema import SmartSchema
if __name__ == "__main__":
    schema = SmartSchema({
        "inum": lambda inst: "{}/{}/{}".format("rke", "2018-19", inst['ref']),
        "tax": lambda inst: (inst['val'] - inst['txbl']) / inst['txbl'],
        "txbl": lambda inst: inst['val'] * 100 / (100 + inst['tax']),
        "val": lambda inst: inst['tax'] * inst['txbl'] / 100 + inst['txbl']
    })
    i = {
        "ref": "678",
        "idt": "1-11-18",
        "iname": "@tfcgpl",
        "tax": 18,
        # "txbl": 30000
        "val": 35400
    }
    schema.invoke(i)
    print(i)
