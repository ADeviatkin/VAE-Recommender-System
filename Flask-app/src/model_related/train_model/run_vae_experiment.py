import json
import sys
from recbole.quick_start import run_recbole
import io
from contextlib import redirect_stdout

def run_experiment(json_config):
    # Convert the JSON string back to a Python dictionary
    config = json.loads(json_config)
    
    # Prepare a string buffer to capture the stdout
    f = io.StringIO()
    
    # Use redirect_stdout to capture output
    with redirect_stdout(f):
        run_recbole(model=config['model'], config_dict=config)
    
    # Get the captured output
    output = f.getvalue()
    
    # Define a file name based on your requirements, here's a simple example
    filename = f"results_{config['model']}_{config['dataset']}.txt"
    
    # Save the output to a file
    with open(filename, 'w') as file:
        file.write(output)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_experiment(sys.argv[1])
    else:
        print("No configuration provided.")
