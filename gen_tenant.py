import csv, json
SRC="/mnt/user-data/uploads/LOCURA/AzureResourceGraphResults-Nueva_consulta_1.csv"
def mapType(t):
    t=t.lower()
    m={'microsoft.compute/virtualmachines':'vm','microsoft.sql/servers':'sqlserver','microsoft.sql/servers/databases':'sqldb',
       'microsoft.storage/storageaccounts':'storage','microsoft.keyvault/vaults':'keyvault','microsoft.web/sites':'webapp',
       'microsoft.documentdb/databaseaccounts':'cosmos','microsoft.operationalinsights/workspaces':'loganalytics',
       'microsoft.network/networksecuritygroups':'nsg','microsoft.network/virtualnetworkgateways':'vpngw',
       'microsoft.network/azurefirewalls':'firewall','microsoft.network/virtualnetworks':'generic'}
    return m.get(t,'generic')
TYPE_ES={'microsoft.operationalinsights/workspaces':'Log Analytics','microsoft.storage/storageaccounts':'Cuenta de almacenamiento',
 'microsoft.sql/servers':'SQL Server','microsoft.sql/servers/databases':'Base de datos SQL','microsoft.web/sites':'App Service',
 'microsoft.web/serverfarms':'Plan App Service','microsoft.web/certificates':'Certificado App Service','microsoft.web/staticsites':'Static Web App',
 'microsoft.keyvault/vaults':'Key Vault','microsoft.cognitiveservices/accounts':'Azure AI Services','microsoft.cognitiveservices/accounts/projects':'Proyecto AI',
 'microsoft.dbforpostgresql/flexibleservers':'PostgreSQL Flexible','microsoft.network/virtualnetworks':'Red virtual','microsoft.network/networkwatchers':'Network Watcher',
 'microsoft.network/networkwatchers/flowlogs':'Flow Logs','microsoft.managedidentity/userassignedidentities':'Identidad administrada',
 'microsoft.insights/components':'Application Insights','microsoft.insights/workbooks':'Workbook','microsoft.insights/actiongroups':'Grupo de acciones',
 'microsoft.insights/activitylogalerts':'Alerta de actividad','microsoft.insights/datacollectionrules':'Regla de recolección','microsoft.insights/datacollectionendpoints':'Endpoint de recolección',
 'microsoft.alertsmanagement/smartdetectoralertrules':'Smart Detector','microsoft.logic/workflows':'Logic App','microsoft.communication/communicationservices':'Communication Services',
 'microsoft.communication/emailservices':'Email Service','microsoft.communication/emailservices/domains':'Dominio de email','microsoft.migrate/assessmentprojects':'Azure Migrate (assessment)',
 'microsoft.migrate/migrateprojects':'Azure Migrate (proyecto)','microsoft.offazure/importsites':'Import Site','microsoft.offazure/mastersites':'Master Site',
 'microsoft.azureactivedirectory/ciamdirectories':'Directorio CIAM','microsoft.visualstudio/account':'Azure DevOps'}
nodes=[]
for r in csv.DictReader(open(SRC,encoding='utf-8-sig')):
    t=r['type']
    nodes.append({'name':r['name'],'type':mapType(t),'typeLabel':TYPE_ES.get(t.lower(), t.split('/')[-1]),'armType':t,
                  'rg':r['resourceGroup'] or '(sin grupo)','loc':r['location'],'checks':[]})
assigned={'frameworks':['MCSB (ASC Default)','ISO 27001:2022','ISO 27002','ISO 27017','NIS2','Spain ENS','NIST 800-53 r5','GDPR','PCI DSS v4'],
          'keys':['mcsb','iso','ens','nis2','nist','rgpd']}
out={'ts':0,'source':'tenant','tenant':'TCM · b6e05d8b','count':len(nodes),'nodes':nodes,'assigned':assigned}
json.dump(out, open('/home/claude/tablero-xr/tenant.json','w',encoding='utf-8'), ensure_ascii=False, separators=(',',':'))
from collections import Counter
print("tenant.json:",len(nodes),"recursos ·", round(len(json.dumps(out))/1024),"KB")
print("tipos modelo:", dict(Counter(n['type'] for n in nodes)))
print("grupos de recursos:", len(set(n['rg'] for n in nodes)))
