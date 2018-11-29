from idaapi import stroffflag, offflag
import json

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
print "%x" % sid
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
        "name":elem_key,
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
    print elem
    prev = elem
members[0]['size'] = min_value
members.reverse()
print members
for element in members:
     AddStrucMember(sid, element["name"], BADADDR, FF_DATA ,-1, element["size"])