result = '''<row>
    <entry>name</entry>
    <entry>data_type</entry>
    <entry>description</entry>
</row>\n'''

with open('data.txt') as f:
    text = []
    for line in f:
        text.append(line)

name = text.pop(0)
name = name.replace('\n','')
name = name.replace(':','')
name = name.strip()
description = text.pop(0)
description = description.replace('\n','')
description = description.replace(':description: ','')
description = description.strip()
data_type = text.pop(0)
data_type = data_type.replace('\n','')
data_type = data_type.replace(':data_type: :','')
data_type = data_type.strip()

result = result.replace('name',name)
result = result.replace('data_type',data_type)
result = result.replace('description',description)

print(result)

with open('result.txt', 'a') as doc:
    doc.write(result)
    doc.close()