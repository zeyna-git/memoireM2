from pyoauth2 import Client

KEY = '6e531a86335d03d813b6'
SECRET = '063df27d0ea33d09d06a5624ab7377bca763e14b'
CALLBACK = ''

client = Client(KEY, SECRET, site='https://api.github.com',authorize_url='https://github.com/login/oauth/authorize',
                token_url='https://github.com/login/oauth/access_token')

print ('-' * 80)
authorize_url = client.auth_code.authorize_url(redirect_uri=CALLBACK, scope='user,public_repo')
print ('Go to the following link in your browser:')
print (authorize_url)
print ('-' * 80)

code = input('Enter the verification code and hit ENTER when you re done:')
code = code.strip()
access_token = client.auth_code.get_token(code, redirect_uri=CALLBACK, parse='query')
print('token', access_token.headers)

print('-' * 80)
print('get user info')
ret = access_token.get('/user')
r=ret.parsed
print(r)
name=r.get("login")
print ('##############',name)
