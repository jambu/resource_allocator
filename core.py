# -*- coding: utf-8 -*-

__author__ = 'Jambunathan'

PRICE_PRECISION = 3

def calculate_cost(items, exp_weight, min_value):
  
  '''
    This method implements a variation of unbounded knapsack algorithm,
    where there is infinite supply of items to be placed on the knapsack.
    Also, the weights are floats rather than non-negative integers.
    So we multiply the weights and the exp_weight by 1000. (Maximum precision of 3 decimal places is allowed.)
    The weight of knapsack (exp_weight) is optional,
    but there has to be a minimum value expected specified otherwise.

  '''

  exp_weight = int(exp_weight * (10**PRICE_PRECISION))
  weights = [int(item[2]* (10**PRICE_PRECISION)) for item in items]
  values = [item[1] for item in items]
  item_names = [item[0] for item in items]

  k_arr = [0 for x in range(exp_weight+1)]
  print exp_weight
  #for i in k_arr:
  #  print i

  return {}

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
      cpus (int) [optional]:
        The Minimum number of cpus needed. 
      price (float) [optional]:
        The maximum price that can be spent for this allocation

  '''
  server_cpus = { "large": 1,
                 "xlarge": 2,
                 "2xlarge": 4,
                 "4xlarge": 8,
                 "8xlarge": 16,
                 "10xlarge": 32
               }

  result = []

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

get_costs(instances, 10, None, 38.0)

