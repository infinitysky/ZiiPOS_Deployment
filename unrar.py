import os
import os.path
import struct 
import wget
import requests
import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont

import patoolib


#---------check system 32 or 64 bit--------------------
def checkSystem():
    version = struct.calcsize("P")*8 
    print("system structure is : " + str(version))
    return version

#----------------Working Space---------------------------------------
def createTempFolder(directory):
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        print("Directory ready")
        
#----------------Create CMD Batch File---------------------------------------

def createDotNet35InstallFile(directory):
    DotNet35InstallFile=directory+"\dotNet35Install.bat"
   
    dotnet35 = open(DotNet35InstallFile,'w')
    
    # Write BATCH fill by using Raw mode "r", Note: Do not change style
    dotnet35.write(r'''Dism /online /Enable-Feature /FeatureName:"NetFx3"''')
    dotnet35.close()
    
    file_exists = os.path.exists(DotNet35InstallFile)
    if (file_exists==True):
         print(".Net 3.5 File ready")
    else:
        print(".Net 3.5 File File Create Error")


def createSQLServerInstallationBatchFile(directory):
    DBInstallFile=directory+"\SQLServerInstall.bat"
    #print(DBInstallFile)  
    SQLInstallationBatchFile = open(DBInstallFile,'w')
    
    # Write BATCH fill by using Raw mode "r", Note: Do not change style
    SQLInstallationBatchFile.write(r'''
cd /d %~dp0
SQLEXPRWT_2008R2_x64_ENU.exe /QS /ACTION=Install /FEATURES=SQLENGINE,REPLICATION,SSMS,SNAC_SDK /IACCEPTSQLSERVERLICENSETERMS /SECURITYMODE=SQL /SAPWD="0000" /INSTANCENAME="SQLEXPRESS2008R2" /SQLSVCACCOUNT="NT AUTHORITY\NETWORK SERVICE" /RSSVCACCOUNT="NT AUTHORITY\NETWORK SERVICE" /AGTSVCACCOUNT="NT AUTHORITY\NETWORK SERVICE" /ADDCURRENTUSERASSQLADMIN="True" /BROWSERSVCSTARTUPTYPE="Automatic" /TCPENABLED="1" /NPENABLED="1"
exit''')
    SQLInstallationBatchFile.close()
    
    file_exists = os.path.exists(DBInstallFile)
    if (file_exists==True):
         print("SQLServer Installation Batch File ready")
    else:
        print("SQLServer Installation Batch File Create Error")
        
def createSQLServerInstallationBatchFileX86(directory):
    DBInstallFile=directory+"\SQLServerInstall.bat"
    #print(DBInstallFile)  
    SQLInstallationBatchFile = open(DBInstallFile,'w')
    
    # Write BATCH fill by using Raw mode "r", Note: Do not change style
    SQLInstallationBatchFile.write(r'''
cd /d %~dp0 
SQLEXPRWT_2008R2_x86_ENU.exe /QS /ACTION=Install /FEATURES=SQLENGINE,REPLICATION,SSMS,SNAC_SDK /IACCEPTSQLSERVERLICENSETERMS /SECURITYMODE=SQL /SAPWD="0000" /INSTANCENAME="SQLEXPRESS2008R2" /SQLSVCACCOUNT="NT AUTHORITY\NETWORK SERVICE" /RSSVCACCOUNT="NT AUTHORITY\NETWORK SERVICE" /AGTSVCACCOUNT="NT AUTHORITY\NETWORK SERVICE" /ADDCURRENTUSERASSQLADMIN="True" /BROWSERSVCSTARTUPTYPE="Automatic" /TCPENABLED="1" /NPENABLED="1"
exit''')
    SQLInstallationBatchFile.close()
    
    file_exists = os.path.exists(DBInstallFile)
    if (file_exists==True):
         print("SQLServer Installation Batch File ready")
    else:
        print("SQLServer Installation Batch File Create Error")
    
    
    
    
def createSQLServerConfigurationBatchFile(directory):
    DBConfigurationFile=directory+"\SQLServerConfiguration.bat"
    #print(DBConfigurationFile)
    DBConfigurationFileBatch = open(DBConfigurationFile,'w')
    
    # Write BATCH fill by using Raw mode "r", Note: Do not change style
    DBConfigurationFileBatch.write(r'''

cd /d %~dp0

net stop MSSQL$SQLEXPRESS2008R2 

reg add "HKLM\SOFTWARE\Microsoft\Microsoft SQL Server\MSSQL10_50.SQLEXPRESS2008R2\MSSQLServer\SuperSocketNetLib\Tcp\IPAll" /v TcpPort /t REG_SZ /d "9899" /f 
reg add "HKLM\SOFTWARE\Microsoft\Microsoft SQL Server\MSSQL10_50.SQLEXPRESS2008R2\MSSQLServer\SuperSocketNetLib\Tcp\IPAll" /v TcpDynamicPorts /t REG_SZ /d "0" /f 
reg add "HKLM\SOFTWARE\Microsoft\Microsoft SQL Server\MSSQL10_50.SQLEXPRESS2008R2\MSSQLServer\SuperSocketNetLib\Tcp\IPAll" /v DisplayName /t REG_SZ /d "Any IP Address" /f 

net start MSSQL$SQLEXPRESS2008R2 

"C:\Program Files\Microsoft SQL Server\100\Tools\Binn\sqlcmd.exe" -S localhost\SQLEXPRESS2008R2 -i ziiposAccount.sql

netsh advfirewall firewall add rule name = SQLServer_Port dir = in protocol = tcp action = allow localport = 9899 profile = DOMAIN,PRIVATE,PUBLIC 
netsh advfirewall firewall add rule name = SQLServer_Port dir = out protocol = tcp action = allow localport = 9899 profile = DOMAIN,PRIVATE,PUBLIC 
netsh advfirewall firewall add rule name = DDA_iPad_Tools_Port dir = in protocol = tcp action = allow localport = 8787 profile = DOMAIN,PRIVATE,PUBLIC 
netsh advfirewall firewall add rule name = DDA_iPad_Tools_Port dir = out protocol = tcp action = allow localport = 8787 profile = DOMAIN,PRIVATE,PUBLIC 
netsh advfirewall firewall add rule name = PDA_Server_Port dir = in protocol = tcp action = allow localport = 8085 profile = DOMAIN,PRIVATE,PUBLIC 
netsh advfirewall firewall add rule name = PDA_Server_Port dir = out protocol = tcp action = allow localport = 8085 profile = DOMAIN,PRIVATE,PUBLIC 
exit''')
    DBConfigurationFileBatch.close()
    file_exists = os.path.exists(DBConfigurationFile)
    if (file_exists==True):
         print("SQLServer Configuration Batch File ready")
    else:
        print("SQLServer Configuration Batch File Create Error")
        


  
    
def createSystemConfigurationBatchFile(directory):
    SystemConfigurationFile=directory+"\SystemConfiguration.bat"
    #print(DBConfigurationFile)
    systemConfigFile = open(SystemConfigurationFile,'w')
    
    # Write BATCH fill by using Raw mode "r", Note: Do not change style
    systemConfigFile.write(r'''
cd /d %~dp0
netsh advfirewall firewall set rule group="File and Printer Sharing" new enable=Yes
netsh advfirewall set currentprofile state on
powercfg /S 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c
powercfg /change standby-timeout-ac 0
powercfg /change standby-timeout-dc 0
powercfg /change monitor-timeout-ac 0
powercfg /change monitor-timeout-dc 0
powercfg /change hibernate-timeout-ac 0
powercfg /change hibernate-timeout-dc 0
powercfg -setacvalueindex SCHEME_CURRENT 4f971e89-eebd-4455-a8de-9e59040e7347 7648efa3-dd9c-4e3e-b566-50f929386280 0
powercfg -setdcvalueindex SCHEME_CURRENT 4f971e89-eebd-4455-a8de-9e59040e7347 7648efa3-dd9c-4e3e-b566-50f929386280 0

reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f

netsh advfirewall firewall set rule group="remote desktop" new enable=Yes

reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-TCP" /v UserAuthentication /t REG_DWORD /d "0" /f

reg add "HKCU\SOFTWARE\Microsoft\TabletTip\1.7" /v TipbandDesiredVisibility /t REG_DWORD /d 1 /f

reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\HideDesktopIcons\NewStartPanel" /v "{20D04FE0-3AEA-1069-A2D8-08002B30309D}" /t REG_DWORD /d "00000000" /f

reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\HideDesktopIcons\ClassicStartMenu" /v "{20D04FE0-3AEA-1069-A2D8-08002B30309D}" /t REG_DWORD /d "00000000"/f

reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\HideDesktopIcons\NewStartPanel" /v "{5399E694-6CE5-4D6C-8FCE-1D8870FDCBA0}" /t REG_DWORD /d "00000000"/f

reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\HideDesktopIcons\ClassicStartMenu" /v "{5399E694-6CE5-4D6C-8FCE-1D8870FDCBA0}" /t REG_DWORD /d "00000000"/f

exit''')
    systemConfigFile.close()
    file_exists = os.path.exists(SystemConfigurationFile)
    if (file_exists==True):
         print("SQLServer Configuration Batch File ready")
    else:
        print("SQLServer Configuration Batch File Create Error")
           
    
def createSQLServerAccountFile(directory):
    DBAccountSQLFile=directory+"\ziiposAccount.sql"
    #print(DBAccountSQLFile)
    DBAccountSQLFileSQL = open(DBAccountSQLFile,'w')
       
    DBAccountSQLFileSQL.write(r'''USE [master] 
GO 
CREATE LOGIN [ZiiPos] WITH PASSWORD=N'ZiiPos884568', DEFAULT_DATABASE=[master], CHECK_EXPIRATION=OFF, CHECK_POLICY=OFF 
GO 
EXEC master..sp_addsrvrolemember @loginame = N'ZiiPos', @rolename = N'sysadmin' 
GO 
''')
    DBAccountSQLFileSQL.close()
    file_exists = os.path.exists(DBAccountSQLFile)
    if (file_exists==True):
         print("SQLServer Account SQL File ready")
    else:
        print("SQLServer Account SQL File Create Error")
   
def createKillScriptFile(directory): 
    killScript=directory+"\killProcess.bat"
    KillFile = open(killScript,'w')
       
    KillFile.write(r'''
taskkill /IM "AssistantServer(v1.2.1).exe" /F
taskkill /IM "AssistantServer.exe" /F
taskkill /IM "ZiiPOSClassicRetail.exe" /F
taskkill /IM "PDAServer.exe" /F
exit
''')
    KillFile.close()
    file_exists = os.path.exists(killScript)
    if (file_exists==True):
         print("killScript File ready")
    else:
        print("killScript Create Error")   


def downloadZiiPOSRetail(downloadURL,filePath):
    #filePath = path+"\ZiiPOSRetail"+version+".exe"
    wget.download(downloadURL, filePath)
    print(filePath)
    file_exists = os.path.exists(filePath)
    if (file_exists==True):
        DDAInstallationProcess(filePath)
    else:
        print("Error")
        
        
def downloadSyncTools(directory):
    downloadURL='https://download.ziicloud.com/programs/ziisync/ZiiSyncSetup-x86(v2.1.1).exe'
    filePath=directory+'\ZiiSyncSetup-x86(v2.1.1).exe'
    print("Start to download Sync Tools ")
    wget.download(downloadURL, filePath)
    file_exists = os.path.exists(filePath)
    if (file_exists==True):
       print("\nSync Tools Ready")
    else:
        print("\nError")
        
def downloadSQLServerX64(directory):
    #SQLEXPRWT_2008R2_x64_ENU.exe
    downloadURL='https://download.ziicloud.com/databases/SQLEXPRWT_x64_ENU.exe'
    filePath=directory+'\SQLEXPRWT_2008R2_x64_ENU.exe'
    print("Start to download SQL Server X64 ")
    wget.download(downloadURL, filePath)
    file_exists = os.path.exists(filePath)
    if (file_exists==True):
        print("\nSQL Server X64 Ready")
    else:
        print("\nError")
        
def downloadSQLServerX86(directory):
    downloadURL='https://download.ziicloud.com/databases/SQLEXPRWT_x86_ENU.exe'
    filePath=directory+'\SQLEXPRWT_2008R2_x86_ENU.exe'
    
    print("Start to download SQL Server X86 ")
    wget.download(downloadURL, filePath)
    file_exists = os.path.exists(filePath)
    if (file_exists==True):
        print("\nSQL Server X86 Ready")
    else:
        print("\nError")
        
def downloadAccessDatabaseEngine(directory):
    #filePath = path+"\ZiiPOSRetail"+version+".exe"
    downloadURL='https://download.ziicloud.com/other/AccessDatabaseEngine.rar'
    filePath=filePath=directory+'\AccessDatabaseEngine.rar'
    print("Start to Download AccessDatabaseEngine")
    wget.download(downloadURL, filePath)
    file_exists = os.path.exists(filePath)
    if (file_exists==True):
       print("\nAccessDatabaseEngine Ready")
    else:
        print("\nError")
        

def download7Zip(directory):
    #filePath = path+"\ZiiPOSRetail"+version+".exe"
    downloadURL='https://www.7-zip.org/a/7z2201-x64.exe'
    filePath=directory+'\z7z2201.exe'
    wget.download(downloadURL, filePath)
    print("Start to Download AccessDatabaseEngine")
    
    file_exists = os.path.exists(filePath)
    if (file_exists==True):
       print("\ndownload 7zip Ready")
    else:
        print("\nError: 7 zip downlad Failed")
        
def download7Zipx86(directory):
    #filePath = path+"\ZiiPOSRetail"+version+".exe"
    downloadURL='https://www.7-zip.org/a/7z2201.exe'
    filePath=filePath=directory+'\z7z2201.exe'
    print("Start to Download AccessDatabaseEngine")
    wget.download(downloadURL, filePath)
    file_exists = os.path.exists(filePath)
    if (file_exists==True):
       print("\ndownload 7zip Ready")
    else:
        print("\nError: 7 zip downlad Failed")
        


def DDAInstallationProcess(FileToInstall):
    print("start")
    runCMD1='cmd /c C:\Ziitech\killProcess.bat'
    runCMD4="cmd /c" + FileToInstall + " /S"
    os.system(runCMD1)
    os.system(runCMD4)

    messagebox.showinfo(title="Installation Complete", message="ZiiPOS Retail Installation Complete")


    
def SyncToolsInstallationProcess(directory):
    filePath=directory+'\ZiiSyncSetup-x86(v2.1.1).exe'
    file_exists = os.path.exists(filePath)
    if (file_exists==True):
        print("AccessDatabaseEngine Ready")
        runCMD1='cmd /c C:\Ziitech\ZiiSyncSetup-x86(v2.1.1).exe /S'
        os.system(runCMD1)
    else:
        print("Error: ZiiSyncSetup not exist")

def AccessDatabaseEngineInstallationProcess(directory):
    filePath=directory+'\AccessDatabaseEngine.rar'
    _7zipInstallProcess(directory)

    patoolib.extract_archive(filePath, outdir=directory)
    installFille=directory+'\AccessDatabaseEngine.exe'
    
    file_exists = os.path.exists(installFille)
    if (file_exists==True):
        print("AccessDatabaseEngine Ready")
        runCMD1='cmd /c C:\Ziitech\AccessDatabaseEngine.exe /quiet'
        os.system(runCMD1)
    else:
        print("Error: AccessDatabaseEngine.exe not exist")
        
        AccessDatabaseEngineInstallationProcess(directory)

        



def _7zipInstallProcess(directory):
    filePath=directory+'\z7z2201.exe'
    file_exists = os.path.exists(filePath)
    if (file_exists==True):
        print("7zip Ready")
        runCMD1='cmd /c C:\Ziitech\z7z2201.exe /S'
        os.system(runCMD1)
    else:
        print("Error: AccessDatabaseEngine.exe not exist")
        


def SQLServerInstallationProcess(directory):
    filePath1=directory+'\SQLServerInstall.bat'
    filePath2=directory+'\SQLServerConfiguration.bat'
    file_exists1 = os.path.exists(filePath1)
    if (file_exists1==True):
        print("SQL Server X86 Ready")
        runCMD1='cmd /c C:\Ziitech\SQLServerInstall.bat'
        os.system(runCMD1)
    else:
        print("Error: SQLServerInstall.bat not exist")
    file_exists2 = os.path.exists(filePath2)
    if (file_exists2==True):
        print("SQL Server X86 Ready")
        runCMD2='cmd /c C:\Ziitech\SQLServerConfiguration.bat'
        os.system(runCMD2)
    else:
        print("Error: SQLServerConfiguration.bat not exist")


def windowsSystemConfiguration(directory):
    filePath1=directory+'\SystemConfiguration.bat'
    file_exists1 = os.path.exists(filePath1)
    if (file_exists1==True):
        print("SQL Server X86 Ready")
        runCMD1='cmd /c C:\Ziitech\SystemConfiguration.bat'
        os.system(runCMD1)
    else:
        print("Error: SystemConfiguration.bat not exist")

def InstallDotNet35(directory):
  
    filePath1=directory+"\dotNet35Install.bat"
    file_exists1 = os.path.exists(filePath1)
    if (file_exists1==True):
        runCMD1='cmd /c C:\Ziitech\dotNet35Install.bat'
        os.system(runCMD1)
    else:
        print("Error: dotNet35Install.bat not exist")



def startZiiPOSFullDeployment():
    directory ="C:\Ziitech"
    print("Start Deployment")
    
    # ------------Create necessary files-----------------------
    #createTempFolder(directory)
    #createDotNet35InstallFile(directory)
    #createSQLServerInstallationBatchFile(directory)
    #createSQLServerConfigurationBatchFile(directory)
    #createSQLServerAccountFile(directory)
    #createSystemConfigurationBatchFile(directory)
    #createKillScriptFile(directory)
    
    # ------------Download files-----------------------
    #downloadAccessDatabaseEngine(directory)
    #downloadSyncTools(directory)
    systemVersion=checkSystem()
    if systemVersion==64:
        print("going to x64 DB Server")
        #downloadSQLServerX64(directory)
        download7Zip(directory)
    else:
        print("going to x86 DB Server")
        #downloadSQLServerX86(directory)
        download7Zipx86(directory)
        
    # -----------Start Installation-------------------------
    #windowsSystemConfiguration(directory)
    #installZiiPOSRetail()
    AccessDatabaseEngineInstallationProcess(directory)
    #InstallDotNet35(directory)
    #SQLServerInstallationProcess(directory)
    #SyncToolsInstallationProcess(directory)
    



    messagebox.showinfo(title="Installation Complete", message="ZiiPOS Retail FULL System Deployment Complete")




def installZiiPOSRetail():
    URL = "https://wombat-api.ziicloud.com/api/vs/client-version/version?clientName=Zii.Retail_Classic&version=1"
    r = requests.get(url = URL)
    data = r.json()
    version = str(data['data']['versionValue'])
    downloadUrl=data['data']['upgradeUrl']
    print(downloadUrl)
    directory ="C:\Ziitech"
    createTempFolder(createKillScriptFile)
    createKillScriptFile(createKillScriptFile)
    
    filePath = "C:\Ziitech\ZiiPOSRetail"+version+".exe"
    downloadZiiPOSRetail(downloadUrl,filePath)
    


class App:
    def __init__(self, root):
        #setting title
        root.title("ZiiPOS Retail Upgrade")
        #setting window size
        width=229
        height=146
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        
        
        GButton_ZiiPOSDeployment=tk.Button(root)
        GButton_ZiiPOSDeployment["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_ZiiPOSDeployment["font"] = ft
        GButton_ZiiPOSDeployment["fg"] = "#000000"
        GButton_ZiiPOSDeployment["justify"] = "center"
        GButton_ZiiPOSDeployment["text"] = "Deploy ZiiPOS Retail FULL"
        GButton_ZiiPOSDeployment.place(x=40,y=80,width=153,height=52)
        GButton_ZiiPOSDeployment["command"] = self.GButton_ZiiPOSDeployment_command
        

        GButton_ZiiPOSUpgrade=tk.Button(root)
        GButton_ZiiPOSUpgrade["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_ZiiPOSUpgrade["font"] = ft
        GButton_ZiiPOSUpgrade["fg"] = "#000000"
        GButton_ZiiPOSUpgrade["justify"] = "center"
        GButton_ZiiPOSUpgrade["text"] = "Install latest version"
        GButton_ZiiPOSUpgrade.place(x=40,y=20,width=153,height=52)
        GButton_ZiiPOSUpgrade["command"] = self.GButton_ZiiPOSUpgrade_command
        

    def GButton_ZiiPOSUpgrade_command(self):
        installZiiPOSRetail()
        
    def GButton_ZiiPOSDeployment_command(self):
        startZiiPOSFullDeployment()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
