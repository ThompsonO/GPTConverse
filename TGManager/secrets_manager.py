import yaml
import os

relative_path = r'Documents\secrets'
secret_path = os.path.expanduser(os.path.join(os.environ['USERPROFILE'], relative_path))
secrets = {}

def load_secret_group(group_name):
    group_path = os.path.join(secret_path, group_name + '.yml') 
    with open(group_path, "r") as group_file:
        try:
            secrets[group_name] = yaml.safe_load(group_file)
        except yaml.YAMLError as exc:
            print(exc)

def secret_group_loaded(group_name):
    if (group_name in secrets.keys()):
        return True
    return False

def get_secret_group(group_name):
    if not secret_group_loaded(group_name):
        load_secret_group(group_name)
    return secrets[group_name]

def get_secret(group_name, secret_name):
    if not secret_group_loaded(group_name):
        load_secret_group(group_name)
    return secrets[group_name][secret_name]

if __name__ == "__main__":
    load_secret_group("minecraft")
    print(secrets['minecraft']['username'])
