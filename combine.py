import json
import glob
import os

# Function to convert all lists within a dictionary to tuples
def convert_lists_to_tuples(d):
    for key, value in d.items():
        if isinstance(value, list):
            d[key] = tuple(value)
        elif isinstance(value, dict):  # Recursively handle nested dictionaries
            convert_lists_to_tuples(value)
    return d

# Function to preprocess each dictionary into a single text string and add it as "text data"
def preprocess(json_data):
    text_data = ""
    for key, value in json_data.items():
        if isinstance(value, list):
            value_str = ', '.join(map(str, value))
            text_data += f"{key}: {value_str}~"
        else:
            if value in ["0", 0, -1, "-1"]:
                value = "Not Available"
            text_data += f"{key}: {value}~"
    json_data["text data"] = text_data
    return json_data

# Path to the folder containing the JSON files
folder_path = 'F:\Chat_Proj\Project Files\preprocessed_data_bangalore'

# List to store all dictionaries from the JSON files
combined_json = []

# Load and combine each JSON file
for file_name in glob.glob(os.path.join(folder_path, '*.json')):
    with open(file_name, 'r') as file:
        data = json.load(file)
        
        # Ensure data is a list of dictionaries
        if isinstance(data, list):
            for item in data:
                processed_item = preprocess(item)
                # Preprocess each dictionary
                combined_json.append(processed_item)
        else:
            print(f"File {file_name} does not contain a list of dictionaries.")

# Convert lists to tuples within dictionaries to make them hashable
combined_json = [convert_lists_to_tuples(d) for d in combined_json]

# Remove duplicates by converting list of dictionaries to a set of frozensets and back to list
unique_combined_json = [dict(t) for t in {frozenset(d.items()) for d in combined_json}]
print(f"Unique items count: {len(unique_combined_json)}")

# Reassign IDs after removing duplicates
for id_no, item in enumerate(unique_combined_json, start=1):
    item["Id"] = id_no

# Save the merged JSON data without duplicates into a new file
output_file = os.path.join('F:\\Chat_Proj\\Project Files\\combining and automation', 'cleaned_and_combined_blore.json')
with open(output_file, 'w') as outfile:
    json.dump(unique_combined_json, outfile, indent=4)

print(f"Output saved to {output_file}")
