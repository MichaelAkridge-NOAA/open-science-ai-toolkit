import subprocess
from random import sample
from concurrent.futures import ThreadPoolExecutor

# Set the source and destination GCS paths
bucket_path = 'gs://nmfs_odp_pifsc/PIFSC/SOD/MOUSS/jpg/'
destination_folder = 'gs://nmfs_odp_pifsc/PIFSC/ESD/ARP/data_management/20240920_lgdds/'

# Function to list files and subfolders in a GCS folder
def list_gcs_items(folder_path):
    cmd = ['gsutil', 'ls', folder_path]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"Error listing items in {folder_path}: {result.stderr.decode()}")
        return []
    return result.stdout.decode().splitlines()

# Function to pull a random sample of files from a folder and copy to destination
def pull_random_sample_from_gcs(source_folder, sample_size, dest_folder):
    files = list_gcs_items(source_folder)
    
    # Filter the files to only include image types
    image_files = [f for f in files if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    # Take a random sample from the list of image files
    if len(image_files) > sample_size:
        sampled_files = sample(image_files, sample_size)
    else:
        sampled_files = image_files  # If there are fewer files than the sample size, just take all
    
    # Copy the sampled files to the destination GCS folder using multithreading (`gsutil -m cp`)
    for file in sampled_files:
        print(f"Copying {file} to {dest_folder}...")
        cmd = ['gsutil', '-m', 'cp', file, dest_folder]  # Using gsutil -m for parallel copies
        subprocess.run(cmd)

# Recursive function to explore folders and pull a sample of images
def process_folders(folder_path, sample_size, dest_folder):
    items = list_gcs_items(folder_path)
    
    for item in items:
        if item.endswith('/'):  # If the item is a subfolder, recurse into it
            print(f"Found folder: {item}, exploring...")
            process_folders(item, sample_size, dest_folder)
        else:
            # If item is a file, we ignore it here (will be handled by pull_random_sample_from_gcs)
            continue

    # Pull a sample of images from the current folder
    print(f"Processing images in folder: {folder_path}")
    pull_random_sample_from_gcs(folder_path, sample_size, dest_folder)

# Step 1: Start processing from the base bucket path using a thread pool for parallel processing
sample_size = 5  # Number of images to copy from each folder

# Use a ThreadPoolExecutor for parallel folder processing
with ThreadPoolExecutor(max_workers=8) as executor:
    # Process each subfolder in parallel
    subfolders = list_gcs_items(bucket_path)
    futures = []
    
    for subfolder in subfolders:
        if subfolder.endswith('/'):  # Ensure it's a folder
            print(f"Scheduling folder for processing: {subfolder}")
            # Submit the folder processing to the thread pool
            futures.append(executor.submit(process_folders, subfolder, sample_size, destination_folder))

    # Wait for all threads to complete
    for future in futures:
        future.result()

print("Sampled dataset copying complete.")
