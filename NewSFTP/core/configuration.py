import yaml

# Загружает данные из "config.yaml" в config
with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)


def parseConfig():
    global config
    with open("config.yaml", "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)