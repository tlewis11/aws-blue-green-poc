import logging
import boto3
import os
import sys
import botocore.exceptions
import json


def setup_logging(log_stream=sys.stdout, log_level=logging.INFO):
  log = logging.getLogger(__name__)
  out_hdlr = logging.StreamHandler(log_stream)
  out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
  out_hdlr.setLevel(logging.INFO)
  log.addHandler(out_hdlr)
  log.setLevel(log_level)
  return log

class CloudformationFactory:
  def __init__(self, config={}, logger=None):
    self.region = 'us-east-2'
    self.cfn = boto3.client('cloudformation', region_name=self.region)
    assert logger is not None
    self.logger = logger

  def upsert_stack(self, stack_name, template, params):
    if self.check_update(stack_name, template, params):
      self.create_stack(stack_name, template, params)
    else:
      self.update_stack(stack_name, template, params)

  def update_stack(self, stack_name, template, parameters=[], wait=True):
    # assert stack_name not in self.stacks.keys()

    # TODO: remove the hard-coded capabilities param
    try:
      self.cfn.update_stack(StackName=stack_name, TemplateBody=template, Parameters=parameters,Capabilities=['CAPABILITY_NAMED_IAM'])
      # self.logger.info(f'Beginning stack update {stack_name}')
      if wait:
        waiter = self.cfn.get_waiter('stack_update_complete')
        waiter.wait(
            StackName=stack_name,
            WaiterConfig={
                'Delay': 10,
                'MaxAttempts': 180
            }
        )
      self.logger.info(f'stack update complete for stack: {stack_name}')
    except Exception as e:
      print(e)

  def create_stack(self, stack_name, template, parameters=[], wait=True):
    # assert stack_name not in self.stacks.keys()

    # TODO: remove the hard-coded capabilities param
    self.cfn.create_stack(StackName=stack_name, TemplateBody=template, Parameters=parameters,Capabilities=['CAPABILITY_NAMED_IAM'])
    self.logger.info(f'Beginning stack create {stack_name}')
    if wait:
      waiter = self.cfn.get_waiter('stack_create_complete')
      waiter.wait(
          StackName=stack_name,
          WaiterConfig={
              'Delay': 20,
              'MaxAttempts': 180
          }
      )
    self.logger.info(f'stack create complete for stack: {stack_name}')

  def check_update(self, stack_name, template, parameters):

    if self._stack_exists(stack_name):
        print('Updating {}'.format(stack_name))
        return False
    else:
        print('Creating {}'.format(stack_name))
        return True

  def _stack_exists(self, stack_name):
      stacks = self.cfn.list_stacks()['StackSummaries']
      for stack in stacks:
          if stack['StackStatus'] == 'DELETE_COMPLETE':
              continue
          if stack_name == stack['StackName']:
              return True
      return False


if __name__ == '__main__':
  logger = setup_logging()

  cfn_handle = CloudformationFactory(logger=logger)

  elb = False
  if elb:
    params = []
    stack_name = 'demo-loadbalancer'
    with open('load_balancer.yml', 'r') as fp:
      template = fp.read()

    cfn_handle.upsert_stack(stack_name, template, params)

  else:
    stack_name = 'webapp-demo'
    with open('webapp.yml', 'r') as fp:
      template = fp.read()

    outputs = boto3.client('cloudformation', region_name='us-east-2').describe_stacks(StackName='demo-loadbalancer')['Stacks'][0]['Outputs']
    target_group = [output['OutputValue'] for output in outputs if output['OutputKey'] == 'AppTargetGroupArn'][0]
    print(target_group)
    params = [
          {
            'ParameterKey': 'TargetGroupArn',
            'ParameterValue': target_group,
          }
        ]
    cfn_handle.upsert_stack(stack_name, template, params)
