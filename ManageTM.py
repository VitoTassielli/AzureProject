from az.cli import az
import json
import argparse

def az_cli (command):
    # AzResult = namedtuple('AzResult', ['exit_code', 'result_dict', 'log'])
    exit_code, result_dict, logs = az(command)

    # On 0 (SUCCESS) print result_dict, otherwise get info from `logs`
    if exit_code == 0:
        #print(result_dict)
        return result_dict
    else:
        print(logs)

parser = argparse.ArgumentParser()
parser.add_argument("-rg", "--resourcegroup", dest = "resourceGroup", help="Resource group")
parser.add_argument("-r", "--region", dest = "region", help="Region which we want manipulate")
parser.add_argument("-a", "--action", dest ="action", help="turnOff or turnOn")
parser.add_argument("-p", "--profile", dest ="profile", help="One profile or write everyprofile")

args = parser.parse_args()
if(args.resourceGroup == None or args.region == None or args.action == None or args.profile == None):
    print("Argoument variables to be defined")
    quit()

print( "ResourceGrouo {} Region {} Action {} Profile {}".format(
        args.resourceGroup,
        args.region,
        args.action,
        args.profile
        ))


desiredStatus = ""
oppositeStatus = ""
resourceGroup = args.resourceGroup #"MLS_ForgeGO_STGv2"
action = args.action    #"turnOff"
profileName = "common-mls-por-stgv2"

#Fix variables
if(args.region == "CentralUS"):
    myRegion = "Central US"
elif(args.region == "EastUS2"):
    myRegion = "East US 2"

if(action == "turnOn"):
    desiredStatus = "Enabled"
    oppositeStatus = "Disabled"
elif(action == "turnOff"):
    desiredStatus = "Disabled"
    oppositeStatus = "Enabled"
else:
    quit()

az_cli("login")
az_cli("account set --subscription d30970ac-05c8-47f0-bd6b-2e2b20f72a38")

if(args.profile == "everyprofile"):
    listProfiles = az_cli("network traffic-manager profile list -g " + resourceGroup + " --query [].name")

    for profile in listProfiles:
        TMendpoints = az_cli("network traffic-manager endpoint list --profile-name " + profile + " -g " + resourceGroup + " --query [].[name,endpointStatus,endpointLocation]")
        print('\n' + profile)

        for endpoint in TMendpoints:
            if(endpoint[1] == oppositeStatus and endpoint[2] == myRegion):
                print("ACTION: " + args.action + " " + myRegion + " endpoint of " + profile + " Traffic Manager")
                #print("network traffic-manager endpoint update --type azureEndpoints -g " + resourceGroup + " --profile-name " + profileName + " -n " + endpoint[0] + " --endpoint-status " + desiredStatus)
                status = az_cli("network traffic-manager endpoint update --type azureEndpoints -g " + resourceGroup + " --profile-name " + profile + " -n " + endpoint[0] + " --endpoint-status " + desiredStatus)
                print(status["endpointStatus"])



else:
    print()