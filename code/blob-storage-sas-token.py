from datetime import datetime, timedelta
import requests
from azure.storage.blob import (
    BlockBlobService,
    ContainerPermissions,
)

accountName = "lablupperuser"
accountKey = ""
containerName = "lablup-container"
blobName = "myblockblob"

def GetSasToken():
    blobService = BlockBlobService(account_name=accountName, account_key=accountKey)
    sas_token = blobService.generate_container_shared_access_signature(containerName,ContainerPermissions.READ, datetime.utcnow() + timedelta(hours=1))
    print(sas_token)
    return sas_token

def AccessTest(token):
    print(token)
    blobService = BlockBlobService(account_name = accountName, account_key = None, sas_token = token)
    blobService.get_blob_to_path(containerName,blobName,"c://temp//result.png")


token=GetSasToken()
# print token
AccessTest(token)