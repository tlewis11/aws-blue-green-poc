import requests

if __name__ == '__main__':

  #discover application ip address
  instance_ip = '3.137.182.152'
  #run basic tests against ip address
  # should return 200
  uri = f'http://{instance_ip}'
  r = requests.get(uri)
  code = r.status_code
  expected_code = 200
  assert code is expected_code , f'Expected {expected_code} status code. Instance returned {code}'
  assert 'My Instance!' in r.text, 'Web page did not contain the correct contents.'
