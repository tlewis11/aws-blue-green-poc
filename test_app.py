import boto3
import requests
import time

if __name__ == '__main__':
  outputs = boto3.client('cloudformation', region_name='us-east-2').describe_stacks(StackName='demo-loadbalancer')['Stacks'][0]['Outputs']
  elb_dns = [output['OutputValue'] for output in outputs if output['OutputKey'] == 'LoadBalancerDns'][0]
  #run basic tests against ip address
  # should return 200
  time.sleep(40)
  uri = f'http://{elb_dns}'
  r = requests.get(uri)
  code = r.status_code
  expected_code = 200
  print('testing elb dns returns 200...')
  assert code is expected_code , f'Expected {expected_code} status code. Instance returned {code}'
  print('good')
  print('testing contents of webpage...')
  assert 'Hello from' in r.text, 'Web page did not contain the correct contents.'
  print('good')
