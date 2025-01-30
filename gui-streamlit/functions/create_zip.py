import zipfile

def create_zip(files_to_zip, data_files):
    # Create a ZIP file
    with zipfile.ZipFile('my_archive.zip', 'w') as zipf:
        for file in files_to_zip:
            zipf.write(file, arcname=(f"zip/{file.split("/")[-1]}"))
        for file in data_files:
            zipf.write(file, arcname=(f"zip/data/uploads/{file.split('/')[-1]}"))