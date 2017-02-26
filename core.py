# -*- coding: utf-8 -*-

__author__ = 'Jambunathan'

# The below constant specifies the decimal points allowed in the prices.
PRICE_PRECISION = 3


def pick_max_weight(items, min_value):

  '''
    This function picks a large enough maximum weight
    for the given min_value and items.
  '''

  # return 5000

  # pick the item with poor "value per unit weight ratio"
  # use (min_value/value) * weight * 2 for the min "value per unit weight" item.
  # the knapsack algo cannot do worse than non greedy case

  values_per_unit_weight = [float("inf") for x in items]

  for idx, (_, value, weight) in enumerate(items):
    if value <= min_value:
      values_per_unit_weight[idx] = float(value)/float(weight)

  # none of the weights are less than or equal to the expected weight
  if all([x == float("inf") for x in values_per_unit_weight]):
    return -1

  min_idx = values_per_unit_weight.index(min(values_per_unit_weight))

  max_weight = (float(min_value)/float(items[min_idx][1])) * items[min_idx][2] * 2
  return max_weight


def calculate_cost(items, max_weight, min_value):

  '''
    This method implements a variation of unbounded knapsack algorithm.
    There is infinite supply of items to be placed on the knapsack.
    Also, the weights are floats rather than non-negative integers.
    So we multiply the weights and the max_weight by 1000. (Maximum precision of 3 decimal places is allowed.)
    The weight of knapsack (max_weight) is optional,
    but a "minimum value expected" should be specified otherwise for returning the value.

  '''

  if not max_weight:
    exit_on_min_value = True
    max_weight = pick_max_weight(items, min_value)
    if max_weight == -1:
      return {"error": 'All the item values are more than the expected value: {}'.format(min_value),
              "total_cost": ''}
  else:
    exit_on_min_value = False

  max_weight = int(max_weight * (10**PRICE_PRECISION))
  weights = [int(item[2] * (10**PRICE_PRECISION)) for item in items]
  values = [item[1] for item in items]
  item_names = [item[0] for item in items]

  # An array, main_arr created to find the optimal value for each of the weight upto max_weight
  # Another array choice_arr is created to note the choice made at each step to remember the items chosen.

  main_arr = [0 for x in range(max_weight+1)]
  choice_arr = [-1 for x in range(max_weight+1)]

  for i, _ in enumerate(main_arr):
    found_min_value = False

    for j in range(len(values)):
      # the current item must weigh less than the current max weight
      if weights[j] <= i:
        if (values[j] + main_arr[i - weights[j]]) > main_arr[i]:
          main_arr[i] = values[j] + main_arr[i - weights[j]]
          # Have chosen the jth item for the current max weight or capacity
          choice_arr[i] = j

      if exit_on_min_value and main_arr[i] >= min_value:
        found_min_value = True
        break

    if found_min_value:
      break

  item_counts = [0 for _ in item_names]
  current_choice = choice_arr[i]

  current_weight = i
  while current_weight > 0 and current_choice != -1:
    item_counts[current_choice] = item_counts[current_choice] + 1
    current_weight = current_weight - weights[current_choice]
    current_choice = choice_arr[current_weight]

  return_data = {}

  servers_data = []
  for idx, item in enumerate(item_names):
    if item_counts[idx] > 0:
      servers_data.append((item, item_counts[idx]))

  return_data['total_cost'] = float(i)/float(10**PRICE_PRECISION)
  return_data['servers'] = sorted(servers_data, key=lambda x: x[1], reverse=True)

  # if the requested minimum value cannot be achieved with the required cost, throw error
  if main_arr[i] < min_value:
    return_data['error'] = 'A cost of {0} can only yield the value: {1} | expected: {2}'.format(return_data['total_cost'],
                                                                                                main_arr[i],
                                                                                                min_value)

  return return_data


def get_costs(instances, hours, cpus, price):

  '''
    This method calculates the total cost for different server requirements.
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

  server_cpus = {
                 "large": 1,
                 "xlarge": 2,
                 "2xlarge": 4,
                 "4xlarge": 8,
                 "8xlarge": 16,
                 "10xlarge": 32
               }

  result = []

  if cpus is None and price is None:
    raise Exception('Either cpus or price needs to be specified')

  for region_name, region_data in instances.iteritems():
    print 'Processing region {}'.format(region_name)
    items = []
    for server_name, server_price in region_data.iteritems():

      # create tuple of (item_name, item_value, item_weight)
      # once a server is selected, it is selected for the whole duration, so the per hour price is multiplied by hours
      # If we run algo per hour, we need to divide the price by hours which will result in
      # incorrect calculation for some cases

      items.append((server_name, server_cpus[server_name], server_price * hours))

    return_data = calculate_cost(items, price, cpus)
    return_data['region'] = region_name
    result.append(return_data)

  result = sorted(result, key=lambda x: x['total_cost'])

  return result