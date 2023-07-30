import copy

class Dataset():

    def __init__(self):
        self.canonical_dataset = None
        self.canonical_depth = None
        self.canonical_indexes = None

        self.dataset = {}
        self.dataset_depth = 3
        self.models = ["model_1", "model_2", "model_3"]
        self.trials = ["trial_1", "trail_2"]
        self.properties = ["property_1", "property_2", "property_3", "property_4"]
        self.values = ["value_1", "value_2", "value_3", "value_4"]

        self._construct_dataset()
        self._init_canonical_dataset()

        while self.canonical_depth > 1:
            self._collapse_dataset_layer()
            self.canonical_depth -= 1

        self._get_dataset_indexes()

    def _init_canonical_dataset(self):
        self.canonical_dataset = copy.deepcopy(self.dataset)
        self.canonical_depth = self.dataset_depth

    def _construct_dataset(self):
        for model in self.models:
            self.dataset[model] = {} 
            for trial in self.trials:
                self.dataset[model][trial] = {}
                for x in range(len(self.properties)):
                    prop = self.properties[x]
                    val = self.values[x]
                    self.dataset[model][trial][prop] = model + "_" + prop + "_" + val

    def _collapse_dataset_layer(self):
        new_dataset = {}
        for x in range(len(self.canonical_dataset)):
            key_1 = list(self.canonical_dataset.keys())[x]
            # print("key_1: ", key_1)
            for y in range(len(self.canonical_dataset[key_1])):
                key_2 = list(self.canonical_dataset[key_1].keys())[y]
                # print("key_2: ", key_2)

                new_key = key_1 + "|" + key_2
                # print("new_key: ", new_key)
                # print()
                new_dataset[new_key] = self.canonical_dataset[key_1][key_2]
        self.canonical_dataset = new_dataset

    def _get_dataset_indexes(self):
        canonical_keys = list(self.canonical_dataset.keys())
        nkeys = len(canonical_keys[0].split("|"))
        
        self.canonical_indexes = {}
        for x in range(nkeys):
            self.canonical_indexes["key_" + str(x)] = {}

        for key in canonical_keys:
            subkey_list = key.split("|")

            for x in range(len(self.canonical_indexes)):
                idx = list(self.canonical_indexes.keys())[x]
                if subkey_list[x] not in self.canonical_indexes[idx]:
                    self.canonical_indexes[idx][subkey_list[x]] = []

                self.canonical_indexes[idx][subkey_list[x]].append(key)

    def rename_canonical_indexes(self, index_names):
        if len(index_names) == len(self.canonical_indexes):
            new_indexes = {}
            for x, index in enumerate(self.canonical_indexes):
                value = self.canonical_indexes[index]
                new_indexes[index_names[x]] = value
            self.canonical_indexes = new_indexes
        else:
            raise ValueError("Incorrect number of index names.")

    def get_canonical_index_depth1_keys(self, index):
        indexes = self.canonical_indexes[index]
        return list(indexes.keys()), indexes
 
    def get_canonical_index_depth1_values(self, index):
        # returned values are unordered
        indexes_keys, indexes = self.get_canonical_index_depth1_keys(index)
        values = {}
        for key in indexes_keys:
            data_keys = indexes[key]
            values[key] = []
            for el in data_keys:
                values[key].append(self.canonical_dataset[el])
        return values
        
    def get_canonical_index_depth2_values(self, indexes):
        # returned values are unordered
        key_1 = indexes[0]
        key_2 = indexes[1]
        indexes_1_keys, indexes_1 = self.get_canonical_index_depth1_keys(key_1)
        indexes_2_keys, indexes_2 = self.get_canonical_index_depth1_keys(key_2)

        # construct 2 level dataset
        new_dataset = {}
        for subkey_1 in indexes_1_keys:
            new_dataset[subkey_1] = {}
            canonical_keys_1 = self.canonical_indexes[key_1][subkey_1]
            for subkey_2 in indexes_2_keys:

                subkey_set_1 = indexes_1[subkey_1]
                subkey_set_2 = indexes_2[subkey_2]
                canonical_keys_2 = self.canonical_indexes[key_2][subkey_2]
                key_intersection = list(set(canonical_keys_1) & set(canonical_keys_2))

                new_dataset[subkey_1][subkey_2] = [] 
                for key in key_intersection:
                    new_dataset[subkey_1][subkey_2].append(self.canonical_dataset[key])
        return new_dataset
 
dataset = Dataset()
#print()
#print("--------------------------------------------------")
#print("dataset")
#print("--------------------------------------------------")
#print(dataset.dataset)
#print()

#print()
#print("--------------------------------------------------")
#print("canonical_dataset")
#print("--------------------------------------------------")
#print(dataset.canonical_dataset)
#print()

dataset.rename_canonical_indexes(["model","trial","property"])

#print()
#print("--------------------------------------------------")
#print("indexes")
#print("--------------------------------------------------")
#print()
#for key in dataset.canonical_indexes:
#    print( key)
#    print(dataset.canonical_indexes[key])
#    print()

#model_values = dataset.get_canonical_index_depth1_values("model")
#print()
#print("model_values")
#print(model_values)
#print()

#model_values = dataset.get_canonical_index_depth1_values("property")
#print()
#print("property_values")
#print(model_values)
#print()

prop_dataset = dataset.get_canonical_index_depth2_values(["property", "model"])
print()
print("prop_dataset")
print(prop_dataset)
print()

model_dataset = dataset.get_canonical_index_depth2_values(["model", "property"])
print()
print("model_dataset")
print(model_dataset)
print()
