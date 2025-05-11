#MYPOS deployment tool
#V1.7.2
#change anydesk download url


from ast import Global
import os
import os.path
import sys
import struct 
import wget
import subprocess
import winreg
import ssl
import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont
import shutil
import ctypes, os

ssl._create_default_https_context = ssl._create_unverified_context

config_name = 'myapp.cfg'

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

config_path = os.path.join(application_path, config_name)


#-------glob var -------------
GlobalDirectory ="C:\\MyPOSZero\\download"
ZiiPOSdownloadUrl = "https://download-myposzero.ziicloud.com/programs/mypos/MyPosZeroLocalServerSetup(v2.6.7.3).exe"
_7Zipx64DownloadURL='https://www.7-zip.org/a/7z2201-x64.exe'
DBx64downloadURL='https://download.ziicloud.com/databases/SQLEXPRWT_x64_ENU.exe'
DBScript='https://download.ziicloud.com/other/ziipos_init_script_v2.4.2.sql'
anydeskDownloadURL="https://download.ziicloud.com/other/AnyDesk.exe"
#anydeskDownloadURL="https://download.anydesk.com/AnyDesk.msi"
dotnetCore301x64DownloadURL="https://download.visualstudio.microsoft.com/download/pr/e0f36c72-8edf-4c6b-a835-e74cfcc6fc23/b5e69be920e77652ce6f31a0f48ab71d/dotnet-sdk-3.1.426-win-x86.exe"
dotnetCore301x86DownloadURL="https://download.visualstudio.microsoft.com/download/pr/b70ad520-0e60-43f5-aee2-d3965094a40d/667c122b3736dcbfa1beff08092dbfc3/dotnet-sdk-3.1.426-win-x64.exe"

LocalFileSqlFile="C:\\MyPOSZero\\download\\SQLEXPRWT_2008R2_x64_ENU.exe"


#---- check is admin
def checkIsAdmin():
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    print(is_admin)
    return is_admin

#------------Check Sql server installed---------------------------------------
def SqlServer_statues():
    sqlserverStatus=0
    SQLserverInstalledFilePath="C:\\Program Files\\Microsoft SQL Server\\MSSQL15.SQLEXPRESS\\MSSQL"
    if not os.path.exists(SQLserverInstalledFilePath):
        print("SQLServer not Installed")
        sqlserverStatus=1
    else:
        sqlserverStatus=0

    return sqlserverStatus

#------------check pending restart------------------
def restart_statues():
     # we know that we're running under windows at this point so it's safe to do these imports
    #from winreg import ConnectRegistry, HKEY_LOCAL_MACHINE, OpenKeyEx, QueryValueEx, REG_EXPAND_SZ, REG_SZ

    try:
        root = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        policy_key = winreg.OpenKeyEx(root, r"Software\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired")
        restart=1
        #user_data_dir, type_ = winreg.QueryValueEx(policy_key, "UserDataDir")
       
    except:
        restart=0
        
   
    return restart

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
        
#----------------Create CMD Batch File-------------------------------

def createDBSQLFile(directory):
    createDBSQLQueryFile=directory+"\\createDB.sql"
    dbsqlquery=open(createDBSQLQueryFile,'w')
    dbsqlquery.write(r'''
USE tempdb;

DECLARE @SQL nvarchar(max);

IF EXISTS (SELECT 1 FROM sys.databases WHERE [name] = 'MYPOSZero_DB')
BEGIN
SET @SQL =
N'USE MYPOSZero_DB;
ALTER DATABASE MYPOSZero_DB SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
USE master;
DROP DATABASE MYPOSZero_DB;';
EXEC (@SQL);
USE tempdb;
END;


CREATE DATABASE [MYPOSZero_DB] ON  PRIMARY 
( NAME = N'MYPOSZero_DB', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL10_50.SQLEXPRESS2008R2\MSSQL\DATA\MYPOSZero_DB.mdf' , SIZE = 3072KB , FILEGROWTH = 1024KB )
 LOG ON 
( NAME = N'MYPOSZero_DB_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL10_50.SQLEXPRESS2008R2\MSSQL\DATA\MYPOSZero_DB.ldf' , SIZE = 1024KB , FILEGROWTH = 10%)
GO
ALTER DATABASE [MYPOSZero_DB] SET COMPATIBILITY_LEVEL = 100
GO
ALTER DATABASE [MYPOSZero_DB] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [MYPOSZero_DB] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [MYPOSZero_DB] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [MYPOSZero_DB] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [MYPOSZero_DB] SET ARITHABORT OFF 
GO
ALTER DATABASE [MYPOSZero_DB] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [MYPOSZero_DB] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [MYPOSZero_DB] SET AUTO_CREATE_STATISTICS ON
GO
ALTER DATABASE [MYPOSZero_DB] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [MYPOSZero_DB] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [MYPOSZero_DB] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [MYPOSZero_DB] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [MYPOSZero_DB] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [MYPOSZero_DB] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [MYPOSZero_DB] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [MYPOSZero_DB] SET  DISABLE_BROKER 
GO
ALTER DATABASE [MYPOSZero_DB] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [MYPOSZero_DB] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [MYPOSZero_DB] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [MYPOSZero_DB] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [MYPOSZero_DB] SET  READ_WRITE 
GO
ALTER DATABASE [MYPOSZero_DB] SET RECOVERY SIMPLE 
GO
ALTER DATABASE [MYPOSZero_DB] SET  MULTI_USER 
GO
ALTER DATABASE [MYPOSZero_DB] SET PAGE_VERIFY CHECKSUM  
GO
USE [MYPOSZero_DB]
GO
IF NOT EXISTS (SELECT name FROM sys.filegroups WHERE is_default=1 AND name = N'PRIMARY') ALTER DATABASE [MYPOSZero_DB] MODIFY FILEGROUP [PRIMARY] DEFAULT
GO

    ''')



def createDisablewin(directory):
    DisableWFile=directory+"\\DisableWindows.bat"
   
    DisableW = open(DisableWFile,'w')
    
                     
    # Write BATCH fill by using Raw mode "r", Note: Do not change style
    DisableW.write(r'''
cd /d %~dp0
                                    
net stop wuauserv
sc config wuauserv start= disabled
reg add "HKLM\Software\Policies\Microsoft\Windows\WindowsUpdate\AU" /v NoAutoUpdate /t REG_DWORD /d "1" /f
reg add "HKLM\Software\Policies\Microsoft\Windows\WindowsUpdate\AU" /v AllowMUUpdateService /t REG_DWORD /d "1" /f
reg add "HKLM\Software\Policies\Microsoft\Windows\WindowsUpdate\AU" /v AUOptions /t REG_DWORD /d "1" /f

reg add "HKLM\SOFTWARE\Policies\Microsoft\WindowsStore" /v AutoDownload /t REG_DWORD /d "2" /f

schtasks /Change /TN "\Microsoft\Windows\WindowsUpdate\Scheduled Start" /Disable
schtasks /Change /TN "\Microsoft\Windows\Windows Defender\Windows Defender Scheduled Scan" /Disable
exit''')
    
    DisableW.close()

    file_exists = os.path.exists(DisableWFile)
    if (file_exists==True):
         print("DisableWindows File ready")
    else:
        print("DisableWindows File Error")
       




def runDisablewin():
    DisableWFile=GlobalDirectory+"\\DisableWindows.bat"
   
    createDisablewin(GlobalDirectory)

    file_exists = os.path.exists(DisableWFile)
    if (file_exists==True):
        runCMD2='cmd /c '+DisableWFile
        
        os.system(runCMD2)
        messagebox.showinfo(title="Disabled Windows", message="Windows Update has been disabled") 
    else:
        print("Error")
        messagebox.showinfo(title="Error: Cannot Disabled Windows", message="Cannot Disable Windows Update please reboot and try again") 


def createDotNet35InstallFile(directory):
    DotNet35InstallFile=directory+"\\dotNet35Install.bat"
   
    dotnet35 = open(DotNet35InstallFile,'w')
    
    # Write BATCH fill by using Raw mode "r", Note: Do not change style
    dotnet35.write(r'''Dism /online /Enable-Feature /FeatureName:"NetFx3"''')
    dotnet35.close()
    
    file_exists = os.path.exists(DotNet35InstallFile)
    if (file_exists==True):
         print(".Net 3.5 File ready")
    else:
        print(".Net 3.5 File File Create Error")

def createDotNet31CoreInstallFile(directory):
    DotNet31CoreInstallFile=directory+"\\DotNet31CoreInstallFile.bat"
   
    dotnet31core = open(DotNet31CoreInstallFile,'w')
    
    # Write BATCH fill by using Raw mode "r", Note: Do not change style
    dotnet31core.write(r''' 
cd /d %~dp0
dotnet-sdk-3.1.426-win-x86.exe /install /S /norestart
dotnet-sdk-3.1.426-win-x64.exe /install /S /norestart
exit''')
    dotnet31core.close()
    
    file_exists = os.path.exists(DotNet31CoreInstallFile)
    if (file_exists==True):
         print(".Net 3.1 File ready")
    else:
        print(".Net 3.1 File File Create Error")


def createSQLServerInstallationBatchFile(directory):
    DBInstallFile=directory+"\\SQLServerInstall.bat"
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
 
    
    
def createSQLServerConfigurationBatchFile(directory):
    DBConfigurationFile=directory+"\\SQLServerConfiguration.bat"
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

netsh advfirewall firewall add rule name = SQLServer_Port dir = in protocol = tcp action = allow localport = 9899 profile = ALL 
netsh advfirewall firewall add rule name = SQLServer_Port dir = out protocol = tcp action = allow localport = 9899 profile = ALL 

                                
exit''')
    DBConfigurationFileBatch.close()
    file_exists = os.path.exists(DBConfigurationFile)
    if (file_exists==True):
         print("SQLServer Configuration Batch File ready")
    else:
        print("SQLServer Configuration Batch File Create Error")
        


def createDBBuildFile(directory):
    DBBuildFile=directory+"\\SQLDBBuild.bat"
    #print(DBConfigurationFile)
    DBConfigurationFileBatch = open(DBBuildFile,'w')
    
    # Write BATCH fill by using Raw mode "r", Note: Do not change style
    DBConfigurationFileBatch.write(r'''

cd /d %~dp0

"C:\Program Files\Microsoft SQL Server\100\Tools\Binn\sqlcmd.exe" -S localhost\SQLEXPRESS2008R2 -i createDB.sql
"C:\Program Files\Microsoft SQL Server\100\Tools\Binn\sqlcmd.exe" -S localhost\SQLEXPRESS2008R2 -d MYPOSZero_DB -i ziipos_init_script_v2.4.2.sql

exit''')
    DBConfigurationFileBatch.close()
    file_exists = os.path.exists(DBBuildFile)
    if (file_exists==True):
         print("SQLServer DB Build Batch File ready")
    else:
        print("SQLServer DB Build File Create Error")
        


    
def createSystemConfigurationBatchFile(directory):
    SystemConfigurationFile=directory+"\\SystemConfiguration.bat"
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


netsh advfirewall firewall add rule name="MyPosZero.LocalServer" dir=in protocol=tcp program="C:\program files (x86)\MyPosZero\MyPosZero.LocalServer\MyPosZero.LocalServer.exe" action=allow
netsh advfirewall firewall add rule name="MyPosZero.LocalServer" dir=in protocol=udp program="C:\program files (x86)\MyPosZero\MyPosZero.LocalServer\MyPosZero.LocalServer.exe" action=allow
   


net stop wuauserv
sc config wuauserv start= disabled
reg add "HKEY_LOCAL_MACHINE\Software\Policies\Microsoft\Windows\WindowsUpdate\AU" /v NoAutoUpdate /t REG_DWORD /d "1" /f
reg add "HKEY_LOCAL_MACHINE\Software\Policies\Microsoft\Windows\WindowsUpdate\AU" /v AllowMUUpdateService /t REG_DWORD /d "1" /f
reg add "HKEY_LOCAL_MACHINE\Software\Policies\Microsoft\Windows\WindowsUpdate\AU" /v AUOptions /t REG_DWORD /d "1" /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\WindowsStore" /v AutoDownload /t REG_DWORD /d "2" /f
                           
schtasks /Change /TN "\Microsoft\Windows\WindowsUpdate\Scheduled Start" /Disable
schtasks /Change /TN "\Microsoft\Windows\Windows Defender\Windows Defender Scheduled Scan" /Disable


echo shutdown /r /f /t 10 > C:\MyPOSZero\Restart.bat
SCHTASKS /CREATE /SC DAILY /TN "ScheduledReboot" /TR "'C:\MyPOSZero\Restart.bat'" /ST 04:00 /RL HIGHEST /f
SCHTASKS /CREATE /SC DAILY /TN "TimeResync" /TR "w32tm /resync" /ST 23:00 /RL HIGHEST /f

reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\AppPrivacy" /v LetAppsAccessLocation /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\tzautoupdate" /v Start /t REG_DWORD /d 3 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\location" /v Value /t REG_SZ /d Allow /f

exit''')
    systemConfigFile.close()
    file_exists = os.path.exists(SystemConfigurationFile)
    if (file_exists==True):
         print("System Configuration Batch File ready")
    else:
        print("System Configuration Batch File Create Error")
           





def createProfilSettingFile():
    directory1="C:\\Program Files (x86)\\MyPosZero\\MyPosZero.LocalServer"
    profilesFile=directory1+"\\profilesettings.json"
    #print(DBAccountSQLFile)
    if not os.path.exists(directory1):
        os.makedirs(directory1)
        
    profilesFileSet = open(profilesFile,'w')
    profilesFileSet.write(r'''
{
  "ProfileSetting": {
    "HttplistenPrefixes": "http://127.0.0.1:8082/",
    "MerchantId": "Fill-YOUR-MERCHANT-NAME",
    "BranchId": "FILL-YOUR-BRANCH-NAME",
    "DBType": "0",
    "DataSource": "localhost\\sqlexpress2008r2",
    "InitialCatalog": "MYPOSZero_DB",
    "AuthEntication": "1",
    "UserName": "sa",
    "EncryptUserPwd": "idhDSRYZ54Y=",
    "EncryptSystemToken": "GPg4lqCsrP2Fd1lvwjMv4w==",
    "DBFile": null
  }
}
''')
    profilesFileSet.close()
    file_exists = os.path.exists(profilesFile)
    
    if (file_exists==True):
         print("SQLServer Profile File ready")
    else:
        print("SQLServer Profile File Create Error")




#-------------------------Download files-------------------------------------------------------------



def downloadZiiPOS(downloadURL,filePath):
    #filePath = path+"\ZiiPOSRetail"+version+".exe"
    file_exists = os.path.exists(filePath)
    if (file_exists==True):
        ZiiPOSInstallationProcess(filePath)
    else:
        wget.download(downloadURL, filePath)
        print(filePath)
        

        
def downloadZiiPOSSQL(directory):
    downloadURL=DBScript
    filePath=directory+'\\ziipos_init_script_v2.4.2.sql'
    
    file_exists = os.path.exists(filePath)
    if (file_exists==True):
       print("\nZiiPOS DB SQL file Ready")
    else:
        print("Start to download ZiiPOS DB SQL Tools ")

        try:
            wget.download(downloadURL, filePath)
        except:
            print("download ZiiPOS Error")
        


def downloadSQLServerX64(directory):
    #SQLEXPRWT_2008R2_x64_ENU.exe
    downloadURL=DBx64downloadURL
    filePath1=directory+'\\SQLEXPRWT_2008R2_x64_ENU.exe'
    SQLserverInstalledFilePath="C:\\Program Files\\Microsoft SQL Server\\MSSQL15.SQLEXPRESS\\MSSQL"

    
    file_exists = os.path.exists(filePath1)
    sqlinstalltion =  os.path.exists(SQLserverInstalledFilePath)
    localSqlinstallFileExist = os.path.exists(LocalFileSqlFile)


    if (file_exists==True):
        print("\nSQL Server X64 file Ready")
    elif(sqlinstalltion==True):    
        print("\nSQL Server X64 file Ready")

    elif(localSqlinstallFileExist==True):
        print("\nSQL Server X64 file Ready")
    else:
        print("\nStart to download SQL Server X64 ")

        try:
            wget.download(downloadURL, filePath1)
        except:
            print("download SQL Server Error")
        
=
        
       

def download7Zip(directory):
    #filePath = path+"\ZiiPOSRetail"+version+".exe"
    downloadURL=_7Zipx64DownloadURL
    filePath=directory+'\\z7z2201.exe'
    file_exists = os.path.exists(filePath)
    if (file_exists==True):
       print("\ndownload 7zip file Ready")
    else:
        print("\nStart to download 7Zip ")

        
        try:
            wget.download(downloadURL, filePath)
        except:
            print("download 7Zip Error")

        
def downloadAnydesk(directory):
    #filePath = path+"\ZiiPOSRetail"+version+".exe"
    downloadURL=anydeskDownloadURL
    #filePath=directory+'\\anydesk.msi'
    filePath=directory+'\\anydesk.exe'
    file_exists = os.path.exists(filePath)
    if (file_exists==True):
       print("\ndownload anydesk file Ready")
    else:
        print("\nStart to download anydesk ")

        try:
            wget.download(downloadURL, filePath)
        except:
            print("download anydesk Error")
       

   

def downloaddotnetcore31(directory):
    #filePath = path+"\ZiiPOSRetail"+version+".exe"
    #dotnetCore301x64DownloadURL="https://download.visualstudio.microsoft.com/download/pr/e0f36c72-8edf-4c6b-a835-e74cfcc6fc23/b5e69be920e77652ce6f31a0f48ab71d/dotnet-sdk-3.1.426-win-x86.exe"
    #dotnetCore301x86DownloadURL="https://download.visualstudio.microsoft.com/download/pr/b70ad520-0e60-43f5-aee2-d3965094a40d/667c122b3736dcbfa1beff08092dbfc3/dotnet-sdk-3.1.426-win-x64.exe"



    downloadURLx86=dotnetCore301x86DownloadURL
    filePathx86=directory+'\\dotnet-sdk-3.1.426-win-x86.exe'
    file_exists = os.path.exists(filePathx86)
    if (file_exists==True):
       print("\ndownload dotnetcore31_x86 file Ready")
    else:
        print("\nStart to download dotnetcore31_x86 ")

        try:
            wget.download(downloadURLx86, filePathx86)
        except:
            print("download DotnetCore31 x86 Error")
        

    downloadURLx64=dotnetCore301x64DownloadURL
    filePathx64=directory+'\\dotnet-sdk-3.1.426-win-x64.exe'
    file_exists = os.path.exists(downloadURLx64)
    if (file_exists==True):
       print("\ndownload dotnetcore31_64 file Ready")
    else:
        print("\nStart to download dotnetcore31_64 ")

       
        try:
             wget.download(downloadURLx64, filePathx64)
        except:
            print("download dotnetcore31_64 Error")


#-----------------------------------------Install process------------------------------------------------------------------------------

def AnydeskInstallationProcess(directory):
    #filePath=directory+'\\anydesk.msi'
    filePath=directory+'\\anydesk.exe'
    
    file_exists = os.path.exists(filePath)
    if (file_exists==True):
        print("anydesk Ready")
        #runCMD1='cmd /c msiexec /i '+filePath+' /QN'
        runCMD1='cmd /c '+filePath+' --install  "C:\Program Files (x86)\AnyDesk" --start-with-win --create-desktop-icon'
        os.system(runCMD1)
        runCMD2='cmd /c echo Mypos123! | "C:\Program Files (x86)\AnyDesk\AnyDesk.exe" --set-password'
        os.system(runCMD2)
    else:
        print("Error: anydesk not exist")


def ZiiPOSInstallationProcess(FileToInstall):
    print("start")
    #runCMD1='cmd /c C:\MyPOSZero\killProcess.bat'
    runCMD4="cmd /c" + FileToInstall + " /S"
    #os.system(runCMD1)
    os.system(runCMD4)
    

        
def SyncToolsInstallationProcess(directory):
    filePath=directory+'\\ZiiSyncSetup-x86.exe'
    
    file_exists = os.path.exists(filePath)
    if (file_exists==True):
        print("SyncToolsInstallation Ready")
        runCMD1='cmd /c '+filePath+' /S'
        os.system(runCMD1)
    else:
        print("Error: ZiiSyncSetup not exist")
     
       
def runSQLDBBuild(directory):
    filePath1=directory+'\\SQLDBBuild.bat'
    file_exists1 = os.path.exists(filePath1)
    if (file_exists1==True):
        print("Start to run DB Build File ")
        runCMD1='cmd /c '+filePath1
       
        os.system(runCMD1)
    else:
        print("Error: SQLDBBuild.bat not exist")

def runChocoinstall(directory):
    filePath1=directory+'\\choco.bat'
    file_exists1 = os.path.exists(filePath1)
    if (file_exists1==True):
        print("Start to run Choco File ")
        runCMD1='cmd /c '+filePath1
       
        os.system(runCMD1)
    else:
        print("Error: choco.bat not exist")



def _7zipInstallProcess(directory):
    filePath=directory+'\\z7z2201.exe'
    file_exists = os.path.exists(filePath)
    if (file_exists==True):
        print("7zip Ready")
        runCMD1='cmd /c '+filePath+' /S'
        os.system(runCMD1)
    else:
        print("Error: 7zip not exist")
        




def SQLServerInstallationProcess(directory):
    filePath1=directory+'\\SQLServerInstall.bat'
    filePath2=directory+'\\SQLServerConfiguration.bat'
    file_exists1 = os.path.exists(filePath1)
    if (file_exists1==True):
        SQLserverInstalledFilePath="C:\\Program Files\\Microsoft SQL Server\\MSSQL15.SQLEXPRESS\\MSSQL"
        if not os.path.exists(SQLserverInstalledFilePath):
            print("Start to Install SQLServer")
            runCMD1='cmd /c '+filePath1
            os.system(runCMD1)          
        else:
            print("SQLServer Ready")         
    else:
        print("Error: SQLServerInstall.bat not exist")
        
    file_exists2 = os.path.exists(filePath2)
    if (file_exists2==True):
        runCMD2='cmd /c '+filePath2
       
        os.system(runCMD2)
    else:
        print("Error: SQLServerConfiguration.bat not exist")


def windowsSystemConfiguration(directory):
    filePath1=directory+'\\SystemConfiguration.bat'
    file_exists1 = os.path.exists(filePath1)
    if (file_exists1==True):
        print("Start to run windows configuration ")
        runCMD1='cmd /c '+filePath1
   
        os.system(runCMD1)
    else:
        print("Error: SystemConfiguration.bat not exist")

def InstallDotNet35(directory):
  
    filePath1=directory+"\\dotNet35Install.bat"
    file_exists1 = os.path.exists(filePath1)
    if (file_exists1==True):
        print("Start to Install .net 3.5")
        runCMD1='cmd /c '+filePath1
   
        os.system(runCMD1)
    else:
        print("Error: dotNet35Install.bat not exist")

def InstallDotNetCore31(directory):
  
    filePath1=directory+"\\DotNet31CoreInstallFile.bat"
    file_exists1 = os.path.exists(filePath1)
    if (file_exists1==True):
        print("Start to Install .net 3.1 Core")
        runCMD1='cmd /c '+filePath1
    
        os.system(runCMD1)
    else:
        print("Error: dotNet35Install.bat not exist")


def syncDateAndTime():
    runCMD1='cmd /c net start w32time && w32tm /resync'
  
    os.system(runCMD1)




def installZiiPOS(directory):
    downloadUrl=ZiiPOSdownloadUrl
    filePath = directory+"\\MyPosZeroLocalServerSetup.exe"
    file_exists1 = os.path.exists(filePath)
    if (file_exists1==True):
        print("\nMyPosZeroLocalServerSetup is ready")
        runCMD1='cmd /c '+filePath+' /S'
        os.system(runCMD1)

        
    else:
        print("\nStart to download ZiiLocalServerSetup")
        downloadZiiPOS(downloadUrl,filePath)
        runCMD1='cmd /c '+filePath+' /S'
        os.system(runCMD1)


def createChocoInstallBatch(directory):
    softwareInstallFile=directory+"\\choco.bat"
    #print(DBConfigurationFile)
    chocoFileBatch = open(softwareInstallFile,'w')
    
    # Write BATCH fill by using Raw mode "r", Note: Do not change style
    chocoFileBatch.write(r'''
cd /d %~dp0
rmdir /S /Q C:\ProgramData\chocolatey
@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "[System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"

choco install -y 7zip.install 
choco install -y googlechrome 
choco install -y firefox 
chocho install -y vscode
exit''')
    chocoFileBatch.close()
    file_exists = os.path.exists(softwareInstallFile)
    if (file_exists==True):
         print("choco install File ready")
    else:
        print("choco install File Create Error")







#--------------------- Run Deployment-----------------------------------------------

def startZiiPOSFullDeployment():

    #directory ="C:\\Ziitech"
    directory=GlobalDirectory
    print("Start Deployment")
    
    syncDateAndTime()
    # ------------Create necessary files-----------------------
    createTempFolder(directory)
    createDBSQLFile(directory)
    createDBBuildFile(directory)
    createDotNet35InstallFile(directory)
    createDotNet31CoreInstallFile(directory)
    createSQLServerInstallationBatchFile(directory)
    createSQLServerConfigurationBatchFile(directory)

    createSystemConfigurationBatchFile(directory)
    createChocoInstallBatch(directory)
    
    
    # ------------Download files-----------------------
    downloadZiiPOSSQL(directory)
    downloaddotnetcore31(directory)
    downloadSQLServerX64(directory)
    downloadAnydesk(directory)

        
    # -----------Start Installation-------------------------
    windowsSystemConfiguration(directory)
    AnydeskInstallationProcess(directory)
    InstallDotNet35(directory)    
    InstallDotNetCore31(directory)
    SQLServerInstallationProcess(directory)
    runSQLDBBuild(directory)
    installZiiPOS(directory)
    createProfilSettingFile()
    #runChocoinstall(directory)
    runDisablewin()



    

#----------------------Server and Sync Tools only---------------------------------------------------------
     
def ZiiPOSDeployment():
    directory=GlobalDirectory
    print("Start Deployment")

    syncDateAndTime()
    # ------------Create necessary files-----------------------
    createTempFolder(directory)
    createDBSQLFile(directory)
    createDBBuildFile(directory)
    
    
    # ------------Download files-----------------------
    downloadZiiPOSSQL(directory)



        
    # -----------Start Installation-------------------------
    runSQLDBBuild(directory)
    installZiiPOS(directory)
    createProfilSettingFile()
    runDisablewin()   
        
 
    


 
#======================================= MAIN UI ===================================================================


class App:
    def __init__(self, root):
        
        #setting title

        root.title("MyPOS F&B Tool V1.7.2")

        #setting window size
        width=350
        height=300
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
        GButton_ZiiPOSDeployment["text"] = "Deploy MyPOS FB Server Only"
        GButton_ZiiPOSDeployment.place(x=40,y=90,width=250,height=52)
        GButton_ZiiPOSDeployment["command"] = self.GButton_ZiiPOSDeployment_command
        

        GButton_ZiiPOSRemoteFULL=tk.Button(root)
        GButton_ZiiPOSRemoteFULL["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_ZiiPOSRemoteFULL["font"] = ft
        GButton_ZiiPOSRemoteFULL["fg"] = "#000000"
        GButton_ZiiPOSRemoteFULL["justify"] = "center"
        GButton_ZiiPOSRemoteFULL["text"] = "Install MyPOS F&B FULL"
        GButton_ZiiPOSRemoteFULL.place(x=40,y=20,width=250,height=52)
        GButton_ZiiPOSRemoteFULL["command"] = self.GButton_ZiiPOSRemoteFULL_command
        


        GButton_ZiiPOSDW=tk.Button(root)
        GButton_ZiiPOSDW["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_ZiiPOSDW["font"] = ft
        GButton_ZiiPOSDW["fg"] = "#000000"
        GButton_ZiiPOSDW["justify"] = "center"
        GButton_ZiiPOSDW["text"] = "DISABLE WIN UPDATE"
        GButton_ZiiPOSDW.place(x=40,y=220,width=250,height=52)
        GButton_ZiiPOSDW["command"] = self.GButton_DisableWin_command
        

    def GButton_ZiiPOSRemoteFULL_command(self):

        status=checkIsAdmin()
        if "True"==str(status):
            getRestartStatus=restart_statues()
            SystemVersion=checkSystem()

            if SystemVersion==64:    
                if getRestartStatus==0:
                    startZiiPOSFullDeployment()
                    messagebox.showinfo(title="Installation Complete", message="MyPOS F&B FULL System Deployment Complete")
                else:
                    print("windows system need REBOOT" )
                    messagebox.showinfo(title="PLease REBOOT", message="Windows has a pending restart process, you must REBOOT WINDOES before we start") 
            else:
                print("windows system: " + SystemVersion)
                messagebox.showinfo(title="Windows System not compatible", message="Windows system not compatible! Win X64 ONLY") 

        else:
            print("You Must run as administrator" )
            messagebox.showinfo(title="run as admin", message="You Must run as administrator") 

        
        


        
        
      
        

    def GButton_ZiiPOSDeployment_command(self):
        status=checkIsAdmin()
        if "True"==str(status):
            getRestartStatus=restart_statues()
            SystemVersion=checkSystem()
            SqlserverST=SqlServer_statues()
            print("SqlServer status" + str(SqlserverST))

            if SystemVersion==64:    
                if getRestartStatus==0:
                    if SqlserverST==1:
                        
                        ZiiPOSDeployment()
                        messagebox.showinfo(title="Installation Complete", message="ZiiPOS System Deployment Complete")
                    else:
                        messagebox.showinfo(title="SQL Server Note ready", message="SQL Server Note ready Please Cleck 'Install FULL'")
                    
                    
                else:
                    print("windows system need REBOOT" )
                    messagebox.showinfo(title="PLease REBOOT", message="Windows has a pending restart process, you must REBOOT WINDOES before we start") 
            else:
                print("windows system: " + SystemVersion)
                messagebox.showinfo(title="Windows System not compatible", message="Windows system not compatible! Win X64 ONLY") 

        else:
            print("You Must run as administrator" )
            messagebox.showinfo(title="run as admin", message="You Must run as administrator") 

        
        


     
    


    def GButton_DisableWin_command(self):
        status=checkIsAdmin()
        if "True"==str(status):
            runDisablewin()
        else:
            print("You Must run as administrator" )
            messagebox.showinfo(title="run as admin", message="You Must run as administrator") 

        
        
        
        
        
        
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
