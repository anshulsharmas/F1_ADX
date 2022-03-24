import imp
import io
from typing import Mapping
from azure.kusto.data import KustoConnectionStringBuilder
from azure.kusto.data.data_format import DataFormat
from time import sleep

from azure.kusto.ingest import (
    IngestionProperties,
    KustoStreamingIngestClient,
    ManagedStreamingIngestClient,
    IngestionStatus,
    QueuedIngestClient
)

ingest_total=0

# replace with ADX Azure AD app credentials 
clusterPath = ""
appId = ""
appKey = ""
appTenant = ""
dbName = ""
tableName = ""

csb = KustoConnectionStringBuilder.with_aad_application_key_authentication(
    clusterPath,
    appId,
    appKey,
    appTenant
)

client = KustoStreamingIngestClient (csb)#KustoStreamingIngestClient (csb) # ManagedStreamingIngestClient.from_engine_kcsb(csb) #QueuedIngestClient(dmb)

ingestionProperties = IngestionProperties(
    database=dbName,
    table="",
    data_format=DataFormat.CSV
    #,flush_immediately=True  
)

def ingest_kusto(t_name, data):
    global ingest_total
    ingestionProperties.table=t_name
    str_stream = io.StringIO(data)
    #print(data)
    try:
        res= client.ingest_from_stream(str_stream, ingestion_properties=ingestionProperties)
        ingest_total+=1
        print(ingest_total)
        #print(res.status)
    except Exception as e: 
        print(e)
        pass