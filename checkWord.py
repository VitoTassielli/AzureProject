import os

basePath = "/mnt/c/Users/vito.tassielli/Desktop/MLS/k8s.integration/configs/"
#directory_in_str = [basePath+"extfeeds", basePath+"forge-importer-custom", basePath+"graphicasset", basePath+"graphicassetapi", basePath+"job-dispatcher", basePath+"jobdispatcher-jobs-api-custom"]
deployment = "extfeeds"
directory_in_str = [basePath+deployment]

extfeeds = ['"SERILOG_PROPERTY_APPLICATION_ROLE": "#{tenant}#-extfeeds"', '"SERILOG_PROPERTY_APPLICATION_NAME": "#{tenant}#-extfeeds"', '"ETCD_NOTIFICATIONS_SERVICE_BUS_MANAGER_HTTP_CALL": "false"','"GUISHELL_CLIENT_ALLOWED_SCOPES": "#{tenant}#-forge-backoffice"', '"GUISHELL_FORGE_BACKOFFICE": "#{tenant}#-forge-backoffice"', '"GUISHELL_FORGE_APPLICATION_NAME": "#{tenant}#-forge-backoffice"', '"ETCD_NOTIFICATIONS__SERVICE_BUS_MESSAGE": "false"', '"SERVICE_BUS_CONNECTIONSTRING"', '"SERVICE_BUS_SECONDARY_CONNECTIONSTRINGS"', '"SERVICE_BUS_NOTIFICATIONS_ENDPOINT_NAME": "#{tenant}#-kvss"']
forgeImporterCustom = ['"GUISHELL_APPLICATION_PARENT_NAME": "#{tenant}#-forge-backoffice"', '"GUISHELL_CLIENT_ALLOWED_SCOPES": "#{tenant}#-forge-backoffice"']
graphicasset = ['"SERILOG_PROPERTY_APPLICATION_NAME": "#{tenant}#-graphicasset"', '"SERILOG_PROPERTY_APPLICATION_ROLE": "#{tenant}#-graphicasset"']
graphicassetapi = ['"SERILOG_PROPERTY_APPLICATION_NAME": "#{tenant}#-graphicassetapi"', '"SERILOG_PROPERTY_APPLICATION_ROLE": "#{tenant}#-graphicassetapi"']
jobDispatcher = ['"SERILOG_PROPERTY_APPLICATION_NAME": "#{tenant}#-job-dispatcher"', '"SERILOG_PROPERTY_APPLICATION_ROLE": "#{tenant}#-job-dispatcher"', '"GUISHELL_APPLICATION_PARENT_NAME": "#{tenant}#-forge-backoffice"', '"GUISHELL_FORGE_BACKOFFICE": "#{tenant}#-forge-backoffice"', '"GUISHELL_FORGE_APPLICATION_NAME": "#{tenant}#-forge-backoffice"']
jobdispatcherJobsApiCustom = ['"SERILOG_PROPERTY_APPLICATION_NAME": "#{tenant}#-jd-jobs-api"', '"SERILOG_PROPERTY_APPLICATION_ROLE": "#{tenant}#-jd-jobs-api"', '"GUISHELL_FORGE_APPLICATION_NAME": "#{tenant}#-forge-backoffice"', '"GUISHELL_FORGE_BACKOFFICE": "#{tenant}#-forge-backoffice"', '"GUISHELL_APPLICATION_PARENT_NAME": "#{tenant}#-forge-backoffice"', '"GUISHELL_CLIENT_ALLOWED_SCOPES": "#{tenant}#-forge-backoffice|#{tenant}#-azure-search|#{tenant}#-sync-forge-to-azure"']



for currentDir in directory_in_str:
    #Set current directory
    directory = os.fsencode(currentDir)
    os.chdir(currentDir)
    print("\nCHECKING " + deployment)

    #Set current variables set
    if(currentDir == (basePath+"extfeeds")):
        variableSet = extfeeds
        #My configs don't have "ETCD_NOTIFICATIONS__SERVICE_BUS_MESSAGE": "false" (ci vuole il doppio trattino basso?)

    elif(currentDir == (basePath+"forge-importer-custom")):
        variableSet = forgeImporterCustom
        #It's OK

    elif(currentDir == (basePath+"graphicasset")):
        variableSet = graphicasset
        #It's OK

    elif(currentDir == (basePath+"graphicassetapi")):
        variableSet = graphicassetapi
        #It's OK

    elif(currentDir == (basePath+"job-dispatcher")):
        variableSet = jobDispatcher
        #It's OK

    elif(currentDir == (basePath+"jobdispatcher-jobs-api-custom")):
        variableSet = jobdispatcherJobsApiCustom
        #It's OK
        
    #variableSet = ['"SERILOG_DD_HOST"']
    #Read config of a Deployment
    print("Tenat should have: " + str(len(variableSet)) + " variables\n")
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        with open(filename) as f:
            itsVariables=0

            for variable in variableSet:
                f.seek(0)
                if variable in f.read():
                    itsVariables=itsVariables+1
                    #print(filename + " have " + variable)
                else: print(filename + " don't have " + variable)