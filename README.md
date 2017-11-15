# Lablup per-user-storage concept code
This Python concept code for per-user-storage concept code for Lablup

## per-user-storage for backend.ai users
Azure Storage Account Blob is best option for SaaS business - handling unlimited storage account with secure SAS token and SMB protocol, fully managed.

### Create storage container
```
# pip install azure-storage-blob 
block_blob_service.create_container('lablup-container')
```

### Upload blob on container 
```
block_blob_service.create_blob_from_path(
    'lablup-container',  # continaer name
    'myblockblob3',  # save as name on blob storage
    'azure_center.png',   # local image file
    content_settings=ContentSettings(content_type='image/png')
            )
```

### List blob on container
```
generator = block_blob_service.list_blobs('lablup-container')
for blob in generator:
    print(blob.name)
```

### Generate SAS token for secure access on per-user-storage
```
def GetSasToken():
    blobService = BlockBlobService(account_name=accountName, account_key=accountKey)
    sas_token = blobService.generate_container_shared_access_signature(containerName,ContainerPermissions.READ, datetime.utcnow() + timedelta(hours=1))
    print(sas_token)
    return sas_token

def AccessTest(token):
    print(token)
    blobService = BlockBlobService(account_name = accountName, account_key = None, sas_token = token)
    blobService.get_blob_to_path(containerName,blobName,"c://temp//result.png")
```

### Mount on Linux machine with Azure Files
```
sudo mount -t cifs //<name_here>.file.core.windows.net/<subfolder_here> [mount point] -o vers=3.0,username=lablupperuser,password=<password>,dir_mode=0777,file_mode=0777,sec=ntlmssp
```


## Reference 
- [Lablup per-user-storage concept repo](https://github.com/lu-project/per-user-storage)
- [Azure subscription and service limits, quotas, and constraints](https://docs.microsoft.com/en-us/azure/azure-subscription-service-limits#storage-limits)
- [Constructing an Account SAS](https://docs.microsoft.com/en-us/rest/api/storageservices/constructing-an-account-sas)
- [Use Azure Files with Linux](https://docs.microsoft.com/en-us/azure/storage/files/storage-how-to-use-files-linux)





