import pypi_test.lib.utilities as utilities 

class Deployment(object):
  def __init__(self, config):
    self.name = str('{} from init'.format(config['name']))
# def main(first_value, second_value):
#   return utilities.add_two_values(first_value, second_value)

# if __name__ == "__main__":
#   main()