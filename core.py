# -*- coding: utf-8 -*-

__author__ = 'Jambunathan'

PRICE_PRECISION = 3

def pick_max_weight(items, min_value):
  return 99

def calculate_cost(items, max_weight, min_value):
  
  '''
    This method implements a variation of unbounded knapsack algorithm,
    where there is infinite supply of items to be placed on the knapsack.
    Also, the weights are floats rather than non-negative integers.
    So we multiply the weights and the max_weight by 1000. (Maximum precision of 3 decimal places is allowed.)
    The weight of knapsack (max_weight) is optional,
    but there has to be a minimum value expected specified otherwise.

  '''
  
  if not max_weight:
    max_weight = pick_max_weight(items, min_value)

  max_weight = int(max_weight * (10**PRICE_PRECISION))

  weights = [int(item[2]* (10**PRICE_PRECISION)) for item in items]
  values = [item[1] for item in items]
  item_names = [item[0] for item in items]

  # An array main_arr created to find the optimal value for each of the weight upto max_weight
  # Another array choice_arr is created to note the choice made at each step to remember the items chosen.
  
  main_arr = [0 for x in range(max_weight+1)]
  choice_arr = [-1 for x in range(max_weight+1)]
  
  for i, _ in enumerate(main_arr):
    for j in range(len(values)):
      # the current item must weigh less than the current max weight
      if weights[j] <= i:
        if (values[j] + main_arr[i - weights[j]]) > main_arr[i]:
          main_arr[i] = values[j] + main_arr[i - weights[j]]
          # Have chosen the jth item for the current max weight or capacity
          choice_arr[i] = j

  item_counts = [0 for _ in item_names]
  current_choice = choice_arr[-1]

  #TODO: need to revisit below line in no max_weight case
  current_weight = i
  print current_weight
  while current_weight > 0 and current_choice != -1:
    item_counts[current_choice] = item_counts[current_choice] + 1
    current_weight = current_weight - weights[current_choice]
    current_choice = choice_arr[current_weight]

  return_data = {}
  return_data['total_cost'] = float(i/(10**PRICE_PRECISION))
  
  servers_data = []
  for idx, item in enumerate(item_names):
    if item_counts[idx] > 0:      
      servers_data.append((item, item_counts[idx]))

  return_data['servers'] = sorted(servers_data, key=lambda  x: x[1])
  
  return return_data

def get_costs(instances, hours, cpus, price):

  ''' 
    This method calculates the total cost for different server requirements.
    The user can specify the total number of 
    Input:
      instances (dict): 
        Input the per hour cost for each server type by region
        { "region_name": 
          { "server_type_1": "per hour cost" 
            ...
          }

        }
      hours (int):
        Exact Number of hours the servers are needed
      cpus (int or None) [optional]:
        The Minimum number of cpus needed. 
      price (float or None) [optional]:
        The maximum price that can be spent for this allocation
      
      Either cpus or price should definitely be specified

  '''
  server_cpus = { "large": 1,
                 "xlarge": 2,
                 "2xlarge": 4,
                 "4xlarge": 8,
                 "8xlarge": 16,
                 "10xlarge": 32
               }
  server_cpus = { "large": 10,
                 "xlarge": 40,
                 "2xlarge": 50,
                 "4xlarge": 70,
                
               }

  result = []

  if cpus == None and price == None:
    raise Exception('Either cpus or price needs to be specified')

  for region_name, region_data in instances.iteritems():
    print 'Processing {}'.format(region_name)
    items = []
    for server_name, server_price in region_data.iteritems():
    
      # create tuple of (item_name, item_value, item_weight)
      # once a server is selected, it selected for the whole duration so the per hour price
      #  is multiplied by hours
      # If we run algo per hour, we need to divide the price by hours which will result in 
      # imprecise calculation for some cases

      items.append((server_name, server_cpus[server_name], server_price * hours))

    return_data = calculate_cost(items, price, cpus)
    return_data['region'] = region_name
    result.append(return_data)

  return result


instances =    {

       "us-east": {

           "large": 0.12,

           "xlarge": 0.23,

           "2xlarge": 0.45,

           "4xlarge": 0.774,

           "8xlarge": 1.4,

           "10xlarge": 2.82

       },

       "us-west": {

           "large": 0.14,

           "2xlarge": 0.413,

           "4xlarge": 0.89,

           "8xlarge": 1.3,

           "10xlarge": 2.97

       },

   }

instances = {'a': {'large': 1, 'xlarge': 3, '2xlarge':4, '4xlarge':5}}
print get_costs(instances, 1, None, 8)

