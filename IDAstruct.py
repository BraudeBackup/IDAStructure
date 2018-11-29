#---------------------------------------------------------------------
# Structure Builder
#
# This script creates structures and populate them
# with members of different types.
#
# Author: Kfir Girstein <kfirgirstein@gmail.com>
#---------------------------------------------------------------------

from idaapi import stroffflag, offflag
import json

def create_structure(name, members_json,size=None, min_value=4):
    try:
        member_array = json.loads(members_json)
        if (member_array is None) or (type(member_array) is not list):
            raise ValueError("Must be json Array, example: \n"+'[{ "name":"John"},{"age":30},{"city":"New York"}]')
    except Exception, e:
        print("You have format error:\t"+str(e)+"\nPlease check that you are not working the right method:\n"+members_json)
    sid = GetStrucIdByName(name)
    if sid != -1:
        DelStruc(sid)
    sid = AddStrucEx(-1, name, 0)
    print "struct id is : %x" % sid
    sorted_members = sorted(member_array ,key = lambda p: next(iter(p.values())))
    last_offset = next(iter(sorted_members[-1].values()))
    first_offset = next(iter(sorted_members[0].values()))
    if(first_offset!=0):
        sorted_members.insert(0,{'attr0':0})
    members = []
    i = 0
    for elem in sorted_members:
        i += 1
        elem_key=next(iter(elem.keys()))
        elem_value=next(iter(elem.values()))
        current= {
            "name":str(elem_key),
            "offset":elem_value,
        }
        members.append(current)
       
    if (size is None) or (last_offset > size):
        size = last_offset + min_value
    else:
        current= {
            "name":"attr" + str(i+1),
            "offset":size,
        }
    members.reverse()
    prev = members[0]
    for elem in members[1:]:
        elem["size"] = prev["offset"] - elem["offset"]
        prev = elem
    members[0]['size'] = min_value
    members.reverse()
    print "The Struct's members are:"
    for element in members:
        print element
        AddStrucMember(sid, element["name"], BADADDR, FF_DATA ,-1, element["size"])
    return members

def create_structure_with_file(name, json_file,size=None, min_value=4):
    try:
        with open(json_file) as f:
            data = json.load(f)
        return create_structure(name,data,size,min_value)
    except Exception, e:
        print("Error in your json file:" +str(e))

def print_choice(numberOfChoice=2):
    print("you can use: create_structure(name, members_json)")
    print("Example: create_structure('temp','[{\"x\":3}]')")
    print("you can use: create_structure_with_file(name, json_file)")
    print("Example: create_structure('temp','json_path')")
    print("Optionally send the size of the structure as an additional parameter")


if __name__ == "__main__":
    print("---------------------------------------------------------------------------------------")
    print("you have imported Structure's Utils for IDA python")
    print("you can choose any method from the folowing:")
    print_choice()
    print("---------------------------------------------------------------------------------------")
    pass