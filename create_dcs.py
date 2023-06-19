import os
import json

# recursively traverse materials directory
# and find all ipynb files
# create a dictionary of all ipynb files

notebooks = {}
for root, dirs, files in os.walk('materials/fa22'):
    for file in files:
        if file.endswith('.ipynb'):
            path = os.path.join(root, file)
            notebooks[file] = path
print(notebooks)

# open .devcontainer/devcontainer.json
# read json into a dictionary
with open('.devcontainer/devcontainer.json', 'r') as f:
    dc = json.load(f)
    
    # create a new devcontainer.json for each file in notebooks
    for file, path in notebooks.items():
        # create a new devcontainer.json
        new_dc = dc.copy()
        new_dc['name'] = file
        new_dc['customizations']['codespaces'] = {
            'openFiles': [path]
        }
        # make directory for new devcontainer.json
        # based on file name without extension
        dir = os.path.join('.devcontainer', file.split('.')[0])
        os.mkdir(dir)
        # write new devcontainer.json to directory
        with open(os.path.join(dir, 'devcontainer.json'), 'w') as f:
            json.dump(new_dc, f, indent=4)