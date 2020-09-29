import http.client

conn = http.client.HTTPSConnection("fsnd-hm.auth0.com")

payload = "{\"client_id\":\"y4qZ9TR8IUsvfc2SbjUz7wvUJqxRaV1C\",\"client_secret\":\"okNHXuIa9ZOyv9NIimoXJB22D-a_6BucOO6qP-XmLN_fkQvAsK81aGSm1Te0qg2m\",\"audience\":\"goal\",\"grant_type\":\"client_credentials\"}"

headers = { 'content-type': "application/json" }

conn.request("POST", "/oauth/token", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))