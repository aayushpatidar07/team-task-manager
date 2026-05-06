import json, urllib.request
base='http://127.0.0.1:8001/api/v1'

# Register
reg = {'name':'Test User','email':'testuser+1@example.com','password':'Password123'}
req = urllib.request.Request(base+'/auth/register', data=json.dumps(reg).encode(), headers={'Content-Type':'application/json'}, method='POST')
try:
    r=urllib.request.urlopen(req)
    print('REGISTER', r.status, r.read().decode())
except Exception as e:
    try:
        resp=e.read().decode()
    except:
        resp=str(e)
    print('REGISTER ERROR:', resp)

# Login
log={'email':reg['email'],'password':reg['password']}
req2=urllib.request.Request(base+'/auth/login', data=json.dumps(log).encode(), headers={'Content-Type':'application/json'}, method='POST')
try:
    r2=urllib.request.urlopen(req2)
    body=r2.read().decode()
    print('LOGIN', r2.status, body)
    token=json.loads(body)['access_token']
    # Get tasks
    req3=urllib.request.Request(base+'/tasks', headers={'Authorization':f'Bearer {token}'})
    r3=urllib.request.urlopen(req3)
    print('TASKS', r3.status, r3.read().decode())
except Exception as e:
    try:
        print('LOGIN/TASKS ERROR:', e.read().decode())
    except:
        print('LOGIN/TASKS ERROR:', str(e))
