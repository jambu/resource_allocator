from core import get_costs

instances = {'us-east': {'large': .754, 'xlarge':.743, '2xlarge':.523, '4xlarge':.734}}

print '\nAsk for minimum CPU'
print get_costs(instances, 2, 2, None)

print '\nAsk for minimum CPU, error case'
print get_costs(instances, 2, 0, None)

print '\nAsk for maximum cost'
print get_costs(instances, 2, None, 34.34)

print '\nAsk for maximum cost, error case'
print get_costs(instances, 2, None, .345)

print '\nAsk for minimum CPU, maximum cost'
print get_costs(instances, 2, 90, 98.143)

print '\nAsk for minimum CPU, maximum cost, error case'
print get_costs(instances, 2, 1000, 98.143)

multi_instances = {'us-east': {'large': .754, 'xlarge':.743, '2xlarge':.523, '4xlarge':.734}, 'us-west': {'large': .004, 'xlarge':.003, '2xlarge':.003, '4xlarge':.004}}

print '\nAsk for muti regions'
print get_costs(multi_instances, 2, 1000, 98.143)
