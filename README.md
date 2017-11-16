# Lablup per-user-storage concept code
This Python concept code for per-user-storage concept code for Lablup.

## Per-user-storage for Backend.AI users
Azure Storage Account Blob is best option for SaaS business - handling unlimited storage account with secure SAS token and SMB protocol, fully managed.

### Create storage container
```sh
pip install azure-storage-blob 
```

```python
block_blob_service.create_container('lablup-container')
```

### Upload blob on container 
```python
block_blob_service.create_blob_from_path(
    'lablup-container',  # continaer name
    'myblockblob3',      # save as name on blob storage
    'azure_center.png',  # local image file
    content_settings=ContentSettings(content_type='image/png')
)
```

### List blob on container
```python
generator = block_blob_service.list_blobs('lablup-container')
for blob in generator:
    print(blob.name)
```

### Generate SAS token for secure access on per-user-storage
```python
def GetSasToken():
    blobService = BlockBlobService(account_name=accountName, account_key=accountKey)
    sas_token = blobService.generate_container_shared_access_signature(
        containerName,
        ContainerPermissions.READ,
        datetime.utcnow() + timedelta(hours=1)
    )
    print(sas_token)
    return sas_token

def AccessTest(token):
    print(token)
    blobService = BlockBlobService(account_name=accountName, account_key=None, sas_token=token)
    blobService.get_blob_to_path(containerName, blobName, "result.png")
```

### Mount on Linux machine with Azure Files
```sh
sudo apt install cifs-utils
sudo mkdir -p /mnt/azvolume
sudo mount -t cifs //$USERNAME.file.core.windows.net/<subfolder_here> /mnt/azvolume -o vers=3.0,username=$USERNAME,password=$PASSWORD,dir_mode=0777,file_mode=0777,sec=ntlmssp
```

### Integration with Backend.AI

There are two types of integration:

* Shared/private datasets on Azure Blob Storage
* Per-user cloud directory on Azure Files

Backend.AI manager and agents use an etcd cluster to store and load its global configuration.
Here we have built a prototype scheme for "remote volumes" in etcd configuration:

```yaml
volumes:

  - name: azure-shard-1
    mount:
      at: requested
      fstype: cifs
      path: "//USERNAME.file.core.windows.net/vfolder"
      options: "vers=3.0,username=USERNAME,password=PASSWORD,dir_mode=0777,file_mode=0777,sec=ntlmssp"

  - name: azure-deeplearning-samples
    mount:
      at: startup
      fstype: cifs
      path: "//USERNAME.file.core.windows.net/dlsamples"
      options: "vers=3.0,username=USERNAME,password=PASSWORD,dir_mode=0777,file_mode=0777,sec=ntlmssp"
```

The Backend.AI manager manages the per-use "virtual folder" as follows:

* The manager instance always mounts all remote volumes specified in the etcd config.
* On vfolder creation request by the user:
  - Create a sub-directory using a random UUID under one of the "requested" volume.
  - Add a database record for its user-specific alias, the host volume and the UUID path of the directory.
* It provides storage statistics (e.g., how many files are there, how much size it is using) to the users via the Backend.AI API.
* On the kernel creation request by the user:
  - Parse the creation config of the request and extract which per-user volume is to be mounted in the container.
  - Attach the "vfolder" record information to the agent-routed request.

The Backend.AI agent uses this configuration as follows:

* On startup of each agent, it reads the config from etcd and do:
  - Mount the remote volumes which has `at: startup` property into the host filesystem
* On the kernel creation request routed from the manager:
  - Mount the remote volumes indicated by the manager as the creation config into the host filesystem. They have `at: requested` property in the etcd config.
  - Mount the "startup" volumes and the "requested" volumes into the container's `/home/work` directory.
  - The user codes can now seamlessly access the files in the volumes like a plain sub-directory inside the home directory.
  - When the user shuts down the kernel or the kernel itself terminates, unmount the volume. (But keep it mounted if other kernels are still using it)

## Reference 
- [Lablup per-user-storage concept repo](https://github.com/lu-project/per-user-storage)
- [Azure subscription and service limits, quotas, and constraints](https://docs.microsoft.com/en-us/azure/azure-subscription-service-limits#storage-limits)
- [Constructing an Account SAS](https://docs.microsoft.com/en-us/rest/api/storageservices/constructing-an-account-sas)
- [Use Azure Files with Linux](https://docs.microsoft.com/en-us/azure/storage/files/storage-how-to-use-files-linux)
- https://github.com/lablup/backend.ai-manager/issues/28


