import pprint
import subprocess
import yaml

pp = pprint.PrettyPrinter(indent=2, width=120)

with open('urls.yaml', 'r') as file:
  urls_list = yaml.load_all(file, Loader=yaml.FullLoader)

  for i, url in enumerate(urls_list):
    i += 1

    try:
      urlwatch_output = subprocess.check_output(
        ['urlwatch', '--urls', 'urls.yaml', '--test-filter', '{}'.format(i)], stderr=subprocess.STDOUT)
      print(f"✅ {url['name']}")
    except subprocess.CalledProcessError as e:
      print(f"🚨 {url['name']}\n")
      print(f"{e.output.decode()}")

