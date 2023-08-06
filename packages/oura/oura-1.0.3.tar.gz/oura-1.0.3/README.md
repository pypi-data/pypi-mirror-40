
Usage:

Install the package:

```
pip install oura
```

Once you register an application, you can use this sample script to authorize access to your own data or some test account data. It will follow the auth code flow and print out the token response. 
```
./token-request.py <client-id> <client-secret>
``` 

Or in your application, do
```
from oura import OuraClient, OuraOAuth2Client

auth_client = OuraOAuth2Client(client_id='my_application', client_secret='random-string')
url = auth_client.authorize_endpoint(scope='defaults to all scopes', 'https://localhost/myendpoint')
# user clicks url, auth happens, then redirect to given url
```

Now we handle the redirect by exchanging an auth code for a token

```
# save this somewhere, see below
token_dict = auth_client.fetch_access_token(code='auth_code_from_query_string')
```

Now that's out of the way, you can call the api:
```
# supply all the params for auto refresh
oura = OuraClient(<client_id>, <client_secret> <access_token>, <refresh_token>, <refresh_callback>)

# or just these for make calls until token expires
oura = OuraClient(<client_id>, <access_token>)

# make authenticated API calls
oura.user_info()
oura.sleep_summary(start='2018-12-05', end='2018-12-10')
oura.activity_summary(start='2018-12-25')
oura.readiness_summary() # throws exception since start is None
```


The `refresh_callback` is a fuction that takes a token dict and saves it somewhere. It will look like:
```
{'token_type': 'bearer', 'refresh_token': <refresh>, 'access_token': <token>, 'expires_in': 86400, 'expires_at': 1546485086.3277025}
```

Live your life.
