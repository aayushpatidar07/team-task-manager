import urllib.request

def main():
    try:
        r = urllib.request.urlopen('http://127.0.0.1:8000/')
        print('ROOT status', r.status)
        body = r.read(800).decode('utf-8', errors='ignore')
        print('ROOT snippet:\n', body)
    except Exception as e:
        print('ROOT error', e)

    try:
        r2 = urllib.request.urlopen('http://127.0.0.1:8000/static/js/app.js')
        print('\napp.js status', r2.status)
        js = r2.read().decode('utf-8', errors='ignore')
        found = 'http://127.0.0.1:8000/api/v1' in js
        print('API_PREFIX present:', found)
        print('\napp.js head lines:')
        for i, line in enumerate(js.splitlines()[:20], start=1):
            print(f'{i:02d}:', line)
    except Exception as e:
        print('app.js error', e)

if __name__ == '__main__':
    main()
