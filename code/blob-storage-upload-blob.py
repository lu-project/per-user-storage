from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings

block_blob_service = BlockBlobService(account_name='lablupperuser', 
    account_key='')
block_blob_service.create_blob_from_path(
    'lablup-container',  # continaer name
    'myblockblob',  # save as name on blob storage
    'azure_center.png',   # local image file
    content_settings=ContentSettings(content_type='image/png')
            )

# list blob
generator = block_blob_service.list_blobs('lablup-container')
for blob in generator:
    print(blob.name)
