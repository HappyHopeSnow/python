import re
from urllib import request


req = request.Request('http://3409736.blog.51cto.com/3399736/1294451')
u = request.urlopen(req)
data = u.read().decode('gbk')
print(data)

urls = re.findall(r"<a.*?href=\s*[\"']*([^\"']+).*?<\/a>", data, re.I)
for u in urls:
    print(u)