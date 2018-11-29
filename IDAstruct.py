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
            raise ValueError("Must be json Array, example: \n"+'[{ "name":"a","offset":"0x10","type":5},{ "name":"b","offset":"0x15","type":"mem"}]')
    except Exception, e:
        print("You have format error:\t"+str(e)+"\nPlease check that you are not working the right method:\n"+members_json)
        return None
    sid = GetStrucIdByName(name)
    if sid != -1:
        DelStruc(sid)

    sid = AddStrucEx(-1, name, 0)
    print "struct id is : %x" % sid
    sorted_members = sorted(member_array ,key = lambda p: int(p['offset'],16))
    last = sorted_members[-1]
    first_offset = sorted_members[0]['offset']
    if(first_offset!=0):
        sorted_members.insert(0,{'name':'this','offset':hex(0),'type':int(first_offset,16)})
    number_of_members = 0
    for elem in sorted_members:
        number_of_members += 1
        if 'type' not in elem:
            elem['type'] = min_value
        elem['name'] = str(elem['name'])
        elem['offset']=int(elem['offset'],16)
    
    if (size is None) or (last['offset'] + last['type'] > size):
        size = last['offset'] + last['type']
    else:
        for i in range(0,size-(last['offset'] + last['type']),min_value):
            current= {
                "name":"attr" + str(number_of_members+1),
                "offset":last['offset'] + last['type'] + i,
                "type":min_value
            }
            sorted_members.append(current)
            number_of_members+=1

    prev = sorted_members[0]
    for elem in sorted_members[1:]:
        current_offset = prev['offset'] + prev['type']
        if current_offset!=elem['offset'] :
            raise ValueError("your Json have double meaning, offset: "+hex(elem['offset'])+"\nnot Is not continuous with its predecessor: "+str(prev))
        prev=elem
        
    for element in sorted_members:
        print element
        AddStrucMember(sid, element["name"], BADADDR, FF_DATA ,-1, element["type"])
    
    return sorted_members


def create_structure_with_file(name, json_file,size=None, min_value=4):
    try:
        with open(json_file) as f:
            data = json.load(f)
        struct = create_structure(name,data,size,min_value)        
        return struct
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