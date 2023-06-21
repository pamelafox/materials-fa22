import os
import json

# Find all notebooks in materials/fa22
notebooks = {}
for root, dirs, files in os.walk('materials/fa22'):
    for file in files:
        if file.endswith('.ipynb'):
            path = os.path.join(root, file)
            notebooks[file] = path

# Create a new devcontainer.json for each file in notebooks
links = {} # {assignment: {notebook: path, devcontainer: path}}
with open('.devcontainer/devcontainer.json', 'r') as f:
    dc = json.load(f)
    
    for file, path in notebooks.items():
        assignment = file.split('.')[0]
        # Customize the devcontainer.json dict with filename-based customizations
        new_dc = dc.copy()
        new_dc['name'] = f"Data 8: {assignment}"
        new_dc['postAttachCommand'] = f"code /workspaces/materials-fa22/{path}"
        new_dc["build"] = {
		    "dockerfile": "../dockerfile",
		    "context": "../.."
	    }
        # Write new devcontainer.json into filename-based directory
        dir = os.path.join('.devcontainer', assignment)
        if not os.path.exists(dir):
            os.mkdir(dir)
        new_dc_path = os.path.join(dir, 'devcontainer.json')
        with open(new_dc_path, 'w') as f:
            json.dump(new_dc, f, indent=4)
        links[assignment] = {
            'notebook': path,
            'devcontainer': new_dc_path
        }

# Create a table of links in links.md
with open('links.md', 'w') as f:
    f.write("# Assignments \n\n")
    f.write("| Assignment | Link |\n")
    f.write("| --- | --- |\n")
    base_path = f"https://codespaces.new/pamelafox/materials-fa22?quickstart=1&devcontainer_path="

    for assignment, paths in links.items():
        f.write(f"| [{assignment}]({paths['notebook']}]) | [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)]({base_path}{paths['devcontainer']}) |\n")
