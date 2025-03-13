def create_batch_script(temp_path):
    content = """
#!/bin/bash

# Check if a directory is passed, otherwise use default "./data"
DATA_DIR=${1:-"./data"}

echo "Using directory: $DATA_DIR"

# Ensure the directory exists
if [ ! -d "$DATA_DIR" ]; then
    echo "Error: Directory '$DATA_DIR' not found!"
    exit 1
fi

# Build the Docker image if not already built
docker-compose build

# Run the container with the dynamically defined directory
docker-compose up -d

# Process each file in the data directory
for file in "$DATA_DIR"/*
do
    # Exclude .json files to prevent re-processing
    if [ -f "$file" ] && [[ "$file" != *.json ]]; then
        echo "Processing file: $file"
        
        # Extract filename without extension
        filename=$(basename "$file")
        filename_no_ext="${filename%.*}"  # Removes the extension

        # Define processed file name in "filename.metadata.json" format
        processed_file="$DATA_DIR/$filename_no_ext.metadata.json"

        # Send the file for processing
        response=$(curl -s -X POST -F "file=@$file" http://localhost:9000/process)
        
        # Save the response
        echo "$response" > "$processed_file"
        echo "Metadata written to: $processed_file"
    else
        echo "Skipping file: $file (already processed or excluded)"
    fi
done

docker-compose down --rmi local

echo "Metadata extraction done. Docker image and container removed."
    """
    with open(f'{temp_path}/run_metadata_extraction.sh', "w") as readme:
        readme.write(content)

    return f'{temp_path}/run_metadata_extraction.sh'