import os
import yaml
import subprocess
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the list of resource kinds that need a namespace update
RESOURCE_KINDS = [
    'Pod', 'Deployment', 'StatefulSet', 'DaemonSet', 'ReplicaSet', 'ReplicationController',
    'Job', 'CronJob', 'Service', 'ConfigMap', 'Secret', 'PersistentVolumeClaim', 
    'Ingress', 'RoleBinding', 'NetworkPolicy', 'ResourceQuota', 'LimitRange'
]

def update_namespace(file_path, new_namespace):
    try:
        with open(file_path, 'r') as file:
            documents = list(yaml.safe_load_all(file))
            updated_documents = []
            for doc in documents:
                if doc and 'kind' in doc and doc['kind'] in RESOURCE_KINDS:
                    if 'metadata' in doc:
                        doc['metadata']['namespace'] = new_namespace
                    updated_documents.append(doc)

        with open(file_path, 'w') as file:
            yaml.safe_dump_all(updated_documents, file)
        
        logging.info(f"Updated namespace for file: {file_path}")
    except Exception as e:
        logging.error(f"Failed to update namespace for file: {file_path} with error: {e}")

def process_directory(directory, new_namespace):
    logging.info(f"Processing directory: {directory}")
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.yaml') or file.endswith('.yml'):
                update_namespace(os.path.join(root, file), new_namespace)

def apply_yaml_files(directory):
    logging.info(f"Applying YAML files in directory: {directory}")
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.yaml') or file.endswith('.yml'):
                file_path = os.path.join(root, file)
                try:
                    subprocess.run(['kubectl', 'apply', '-f', file_path], check=True)
                    logging.info(f"Applied file: {file_path}")
                except subprocess.CalledProcessError as e:
                    logging.error(f"Failed to apply file: {file_path} with error: {e}")

# Replace 'your_directory_path' with the path to your YAML files and 'review' with your new namespace
project_directory = 'your_directory_path'
new_namespace = 'your_namespace'

# Update namespaces in YAML files
process_directory(project_directory, new_namespace)

# Apply the updated YAML files
apply_yaml_files(project_directory)
