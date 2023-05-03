import json

class item:
    def __init__(self, name, weight, freezer, fragile):
        self.name = name
        self.weight = weight
        self.freezer = freezer
        self.fragile = fragile
def loadItems():
    item_list = []
    # Load items from json file
    with open('items.json', 'r') as f:
        data = json.load(f)
        for obj in data:
            object_instance = item(**obj)
            item_list.append(object_instance)
    return item_list

def main():
    #load in item list from .JSON file
    obj_list = loadItems()
    items = sorted(obj_list, key=lambda x: x.weight)
    #implement rule based loading system

    #rule Ra: bag large items
    #rule Rb: bag medium items
    #rule Rc: bag small items
    #rule Rd: put freeze items in a freezer bag
    #rule Re: put fragile items together in a bag with weight limit half of normal bags
    #rule Rf: each bag can contain < 10 weight(large: 5, medium: 2, small: 1)
    #rule Rg: for fragile items bag large fragile items
    #rule Rh: for fragile items bag medium fragile items
    #rule Ri: for fragile items bag small fragile items
    #rule Rj: for fragile items create a new bag
    #Rule Rk: for freezer items bag large freezer items
    #rule Rl: for freezer items bag medium freezer items
    #rule Rm: for freezer items bag small freezer items
    #rule Rn: for freezer items create a new freezer bag
    bag_list = []

    bag_index = 1
    bag_size = 10
    fragile_bag = 0
    freezer_bag = 0

    print("Start bagging item! Start by bagging the larger items.")

    for obj in items:
        if obj.weight == 'large':
            if obj.freezer == True:
                 pass
            elif obj.fragile == True:
                pass
            else:
                if bag_size < 5:
                    print("Rule Rf says: Start a new bag.")
                    bag_index = bag_index + 1
                    bag_size = 10
                print("Rule Ra says: Put " + obj.name + " in bag", bag_index)
                bag_size = bag_size - 5
        if obj.weight == 'medium':
            if obj.freezer == True:
                 pass
            elif obj.fragile == True:
                pass
            else:
                if bag_size < 2:
                    print("Rule Rf says: Start a new bag.")
                    bag_index = bag_index + 1
                    bag_size = 10

                print("Rule Rb says: Put " + obj.name + " in bag", bag_index)
                bag_size = bag_size - 2

        if obj.weight == 'small':
            if obj.freezer == True:
                 pass
            elif obj.fragile == True:
                pass
            else:
                if bag_size < 1:
                    print("Rule Rf says: Start a new bag.")
                    bag_index = bag_index + 1
                    bag_size = 10
                print("Rule Rc says: Put " + obj.name + " in bag", bag_index)
                bag_size = bag_size - 1

    for obj in items:
        if obj.fragile == True:
            if(fragile_bag == 0):
                print("Rule Re says: Start a new bag")
                bag_size = 5
                bag_index = bag_index + 1
                fragile_bag = 1
            if obj.weight == 'large':
                if bag_size < 5:
                    print("Rule Rj says: Start a new bag.")
                    bag_size = 5
                    bag_index = bag_index + 1
                print("Rule Rg says: Put " + obj.name + " in bag", bag_index)
                bag_size = bag_size - 5
            elif obj.weight == 'medium':
                if bag_size < 2:
                    print("Rule Rj says: Start a new bag.")
                    bag_size = 5
                    bag_index = bag_index + 1
                print("Rule Rh says: Put " + obj.name + " in bag", bag_index)
                bag_size = bag_size - 2
            elif obj.weight == 'small':
                if bag_size < 1:
                    print("Rule Rj says: Start a new bag.")
                    bag_size = 5
                    bag_index = bag_index + 1
                print("Rule Ri says: Put " + obj.name + " in bag", bag_index)
                bag_size = bag_size - 1

    for obj in items:
        if obj.freezer == True:
            if (freezer_bag == 0):
                print("Rule Rd says: Start a new freezer bag")
                bag_size = 10
                bag_index = bag_index + 1
                freezer_bag = 1
            if obj.weight == 'large':
                if bag_size < 5:
                    print("Rule Rn says: Start a new freezer bag.")
                    bag_size = 10
                    bag_index = bag_index + 1
                print("Rule Rk says: Put " + obj.name + " in bag", bag_index)
                bag_size = bag_size - 5
            elif obj.weight == 'medium':
                if bag_size < 2:
                    print("Rule Rn says: Start a new freezer bag.")
                    bag_size = 10
                    bag_index = bag_index + 1
                print("Rule Rl says: Put " + obj.name + " in bag", bag_index)
                bag_size = bag_size - 2
            elif obj.weight == 'small':
                if bag_size < 1:
                    print("Rule Rn says: Start a new bag.")
                    bag_size = 10
                    bag_index = bag_index + 1
                print("Rule Rm says: Put " + obj.name + " in bag", bag_index)
                bag_size = bag_size - 1


if __name__ == "__main__":
    main()
