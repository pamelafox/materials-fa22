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
with open('.devcontainer/devcontainer.json', 'r') as f:
    dc = json.load(f)
    
    for file, path in notebooks.items():
        assignment = file.split('.')[0]
        # Customize the devcontainer.json dict with filename-based customizations
        new_dc = dc.copy()
        new_dc['name'] = f"Data 8: {assignment}"
        new_dc['postAttachCommand'] = f"code /workspaces/materials-fa22/{path}"
        new_dc["build"] = {
		    "dockerfile": "dockerfile",
		    "context": ".."
	    }
        # Write new devcontainer.json into filename-based directory
        dir = os.path.join('.devcontainer', assignment)
        if not os.path.exists(dir):
            os.mkdir(dir)
        with open(os.path.join(dir, 'devcontainer.json'), 'w') as f:
            json.dump(new_dc, f, indent=4)