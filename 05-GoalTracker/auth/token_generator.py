import http.client

conn = http.client.HTTPSConnection("fsnd-hm.auth0.com")

payload = "{\"client_id\":\"Tnl5GBx1UPP4xf16D3RtQKW0cRrq1FJf\",\"client_secret\":\"0w2TbO1lxnm_8N7nAyQBOXnKTOABHIkzbprrG1nBl8vExzgY9v1E9yQqKamxTfEZ\",\"audience\":\"goal\",\"grant_type\":\"client_credentials\"}"

headers = { 'content-type': "application/json" }

conn.request("POST", "/oauth/token", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))