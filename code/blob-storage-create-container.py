# install sdk
# pip install azure-storage-blob

from azure.storage.blob import BlockBlobService
block_blob_service = BlockBlobService(account_name='lablupperuser', 
    account_key='')

block_blob_service.create_container('lablup-container')

# public access purpose
# from azure.storage.blob import PublicAccess
# block_blob_service.create_container('mycontainer', public_access=PublicAccess.Container)