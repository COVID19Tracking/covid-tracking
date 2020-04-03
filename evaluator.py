import argparse
import concurrent.futures
import subprocess
import yaml
import os.path

parser = argparse.ArgumentParser(description='Evaluate all urlwatch filters.')
parser.add_argument('--output_dir', type=str, default=None,
                    help='''If set, the output for each filter will be written
                    to a separate file in this directory. If unset, it will be 
                    sent to STDOUT''')
parser.add_argument('--urls_yaml', type=str, default='urls.yaml',
                    help='''Filter file to use.''')
parser.add_argument('--parallelism', type=int, default=10,
                    help='''How many filters to run in parallel.''')

args = parser.parse_args()

def evaluate_filter(filter_num):
  urlwatch_output = ''
  try:
    urlwatch_output = subprocess.check_output(
      ['urlwatch', '--urls', args.urls_yaml, '--test-filter', '{}'.format(filter_num)], stderr=subprocess.STDOUT).decode()
  except subprocess.CalledProcessError as e:
    urlwatch_output = e.output.decode()

  return urlwatch_output

with open(args.urls_yaml, 'r') as yaml_file:
  urls_list = yaml.load_all(yaml_file, Loader=yaml.FullLoader)

  futures = {}
  with concurrent.futures.ThreadPoolExecutor(max_workers=args.parallelism) as executor:
    for i, url in enumerate(urls_list):
      # filters are 1-indexed
      futures[url['name']] = executor.submit(evaluate_filter, i+1)
    
  for name, future in futures.items():
    urlwatch_output = str(future.result())
    if args.output_dir:
      with open(os.path.join(args.output_dir, name), 'w') as output_file:
        print(name)
        output_file.write(urlwatch_output)
    else:
      print(f"{name}:\n{urlwatch_output}")
