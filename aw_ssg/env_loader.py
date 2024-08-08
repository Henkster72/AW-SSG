import os

def load_env_variables(file_path):
    crucial_vars = {}
    open_vars = {}
    missing_crucial_vars = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or '=' not in line:
                continue

            key, rest = line.split('=', 1)
            if '|' in rest:
                value, *attributes = rest.split('|')
            else:
                value = rest
                attributes = []

            value = value.strip()

            if 'crucial' in attributes:
                if not value:
                    missing_crucial_vars.append(key)
                crucial_vars[key] = value

            if 'open' in attributes:
                open_vars[key] = value

    if missing_crucial_vars:
        print("Error: Missing crucial environment variables:", ", ".join(missing_crucial_vars))
        exit(1)

    return crucial_vars, open_vars

def set_env_variables(variables):
    for key, value in variables.items():
        os.environ[key] = value

# Load environment variables from the .env file
crucial_vars, open_vars = load_env_variables('.env')

# Set the crucial and open environment variables
set_env_variables(crucial_vars)
set_env_variables(open_vars)
