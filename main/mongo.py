import pymongo


class mongodata:
    def __init__(self):
        self.__client = pymongo.MongoClient(
            "mongodb+srv://test1un:SlHxbeWHN2AfcpKt@cluster0.pffpd.gcp.mongodb.net/invoice_db?retryWrites=true&w=majority")
        self.__db = self.__client['invoice_db']
        self.__college = self.__db['college']
        self.__trainer = self.__db['trainer']
        self.__bank = self.__db['bank_details']

# Returns sorted list of trainer names - Used in form
    def trainer_names(self):
        names = list()
        for x in self.__trainer.find({}, {"_id": 0, "name": 1}).sort('name'):
            names.append(x['name'])
        return names

    # Returns sorted list of college names - Used in form
    def college_names(self):
        names = list()
        for x in self.__college.find({}, {"_id": 0, "name": 1}).sort('name'):
            names.append(x['name'])
        return names

    # Returns dictionary of trainer details
    def trainer_details(self, name):
        return self.__trainer.find_one({"name": name})

    # Returns dictionary of bank details of a single trainer
    def bank_details(self, id):
        return self.__bank.find_one({"_id": id})

    # Returns location of college
    def college_location(self, name):
        return self.__college.find_one({"name": name})['location']

    def add_trainer(self, tdata, bdata):
        self.__trainer.insert_one(tdata)
        bdata['_id'] = self.__trainer.find_one(tdata)['_id']
        self.__bank.insert_one(bdata)

    def add_college(self, cdata):
        self.__college.insert_one(cdata)
