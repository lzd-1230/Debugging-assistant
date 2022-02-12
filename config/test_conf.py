import yaml

f = open("./config/config.yaml")
config = yaml.safe_load(f.read())
print(config["graph"])