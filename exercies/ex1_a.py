from database import Relation, generate_database


def natural_join(relation1: Relation, relation2: Relation) -> Relation:
    hash = {}
    new_row= {}
    relation=[]
    i = 0 
    for row1 in relation1:
        hash[i] = row1 #save the index of row by the key value
        i=i+1
    #print(list(hash.values())[0].get(#b))
    #print((list(hash.items()))[0][1].get('b'))
    hash_len=len(list(hash.values()))
    hash_keys_list=list(hash.values())[0].keys()
    for row2 in relation2:
        attributes = list(row2.keys())
        if (attributes[0]) in list(hash.values())[0].keys() :
            if row2.get(attributes[0]) == hash.values()[0].get(attributes[0]):
                print('ok')

                new_rowd = {**row2 , **list(hash.values())[0]}
        #print('row2',row2)
        print(list(hash.values())[0].keys())
        #print(row2.get(attributes[0]))
    return new_rowd
    
if __name__ == "__main__":
    relation1: Relation = [
        {"a": 0, "b": 2},
        {"a": 1, "b": 3},
        {"a": 2, "b": 4},
    ]

    relation2: Relation = [
        {"b": 3, "c": 5},
        {"b": 4, "c": 6},
        {"b": 4, "c": 7},
        {"b": 5, "c": 8},

    ]

    natural_join(relation1,relation2)