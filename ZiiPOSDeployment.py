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
GlobalDirectory ="C:\\Ziitech\\download"
ZiiPOSdownloadUrl = "https://download.ziicloud.com/programs/ziipos/ZiiLocalServerSetup(v2.6.1.2).exe"
syncToolDownloadURL='https://download.ziicloud.com/programs/ziisync/ZiiSyncSetup-x86(v2.1.1).exe'
_7Zipx64DownloadURL='https://www.7-zip.org/a/7z2201-x64.exe'
DBx64downloadURL='https://download.ziicloud.com/databases/SQLEXPRWT_x64_ENU.exe'
DBScript='https://download.ziicloud.com/other/ziipos_init_script_v2.4.2.sql'
anydeskDownloadURL="https://download.anydesk.com/AnyDesk.msi"
dotnetCore301x64DownloadURL="https://download.visualstudio.microsoft.com/download/pr/e0f36c72-8edf-4c6b-a835-e74cfcc6fc23/b5e69be920e77652ce6f31a0f48ab71d/dotnet-sdk-3.1.426-win-x86.exe"
dotnetCore301x86DownloadURL="https://download.visualstudio.microsoft.com/download/pr/b70ad520-0e60-43f5-aee2-d3965094a40d/667c122b3736dcbfa1beff08092dbfc3/dotnet-sdk-3.1.426-win-x64.exe"

LocalFileDirectory="C:\\Ziitech_D"
LocalFileSqlFile=LocalFileDirectory+"\\01_Softwares\\AutoInstall\\SQLServer2008R2\\SQLEXPRWT_2008R2_x64_ENU.exe"


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
CREATE DATABASE [ZiiPOS_DB] ON  PRIMARY 
( NAME = N'ZiiPOS_DB', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL10_50.SQLEXPRESS2008R2\MSSQL\DATA\ZiiPOS_DB.mdf' , SIZE = 3072KB , FILEGROWTH = 1024KB )
 LOG ON 
( NAME = N'ZiiPOS_DB_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL10_50.SQLEXPRESS2008R2\MSSQL\DATA\ZiiPOS_DB_log.ldf' , SIZE = 1024KB , FILEGROWTH = 10%)
GO
ALTER DATABASE [ZiiPOS_DB] SET COMPATIBILITY_LEVEL = 100
GO
ALTER DATABASE [ZiiPOS_DB] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [ZiiPOS_DB] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [ZiiPOS_DB] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [ZiiPOS_DB] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [ZiiPOS_DB] SET ARITHABORT OFF 
GO
ALTER DATABASE [ZiiPOS_DB] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [ZiiPOS_DB] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [ZiiPOS_DB] SET AUTO_CREATE_STATISTICS ON
GO
ALTER DATABASE [ZiiPOS_DB] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [ZiiPOS_DB] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [ZiiPOS_DB] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [ZiiPOS_DB] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [ZiiPOS_DB] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [ZiiPOS_DB] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [ZiiPOS_DB] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [ZiiPOS_DB] SET  DISABLE_BROKER 
GO
ALTER DATABASE [ZiiPOS_DB] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [ZiiPOS_DB] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [ZiiPOS_DB] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [ZiiPOS_DB] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [ZiiPOS_DB] SET  READ_WRITE 
GO
ALTER DATABASE [ZiiPOS_DB] SET RECOVERY SIMPLE 
GO
ALTER DATABASE [ZiiPOS_DB] SET  MULTI_USER 
GO
ALTER DATABASE [ZiiPOS_DB] SET PAGE_VERIFY CHECKSUM  
GO
USE [ZiiPOS_DB]
GO
IF NOT EXISTS (SELECT name FROM sys.filegroups WHERE is_default=1 AND name = N'PRIMARY') ALTER DATABASE [ZiiPOS_DB] MODIFY FILEGROUP [PRIMARY] DEFAULT
GO

    ''')



def createDisablewin(directory):
    DisableWFile=GlobalDirectory+"\\DisableWindows.bat"
   
    DisableW = open(DisableWFile,'w')
    
                     
    # Write BATCH fill by using Raw mode "r", Note: Do not change style
    DisableW.write(r'''net stop wuauserv
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
    dotnet31core.write(r'''cd /d %~dp0
.\dotnet-sdk-3.1.426-win-x86.exe /install /S /norestart
.\dotnet-sdk-3.1.426-win-x64.exe /install /S /norestart
exit''')
    dotnet31core.close()
    
    file_exists = os.path.exists(dotnet31core)
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
cd c:\ziitech\download
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

cd c:\ziitech\download

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
        


def createDBBuildFile(directory):
    DBBuildFile=directory+"\\SQLDBBuild.bat"
    #print(DBConfigurationFile)
    DBConfigurationFileBatch = open(DBBuildFile,'w')
    
    # Write BATCH fill by using Raw mode "r", Note: Do not change style
    DBConfigurationFileBatch.write(r'''

cd c:\ziitech\download

"C:\Program Files\Microsoft SQL Server\100\Tools\Binn\sqlcmd.exe" -S localhost\SQLEXPRESS2008R2 -i createDB.sql
"C:\Program Files\Microsoft SQL Server\100\Tools\Binn\sqlcmd.exe" -S localhost\SQLEXPRESS2008R2 -d ZiiPOS_DB -i ziipos_init_script_v2.4.2.sql

exit''')
    DBConfigurationFileBatch.close()
    file_exists = os.path.exists(DBBuildFile)
    if (file_exists==True):
         print("SQLServer DB Build Batch File ready")
    else:
        print("SQLServer DB Build File Create Error")
        

def createChocoInstallBatch(directory):
    softwareInstallFile=directory+"\\choco.bat"
    #print(DBConfigurationFile)
    chocoFileBatch = open(softwareInstallFile,'w')
    
    # Write BATCH fill by using Raw mode "r", Note: Do not change style
    chocoFileBatch.write(r'''
cd c:\ziitech\download

@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "[System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"

choco upgrade chocolatey
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





    
def createSystemConfigurationBatchFile(directory):
    SystemConfigurationFile=directory+"\\SystemConfiguration.bat"
    #print(DBConfigurationFile)
    systemConfigFile = open(SystemConfigurationFile,'w')
    
    # Write BATCH fill by using Raw mode "r", Note: Do not change style
    systemConfigFile.write(r'''
cd c:\ziitech\download
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

reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f

netsh advfirewall firewall set rule group="remote desktop" new enable=Yes

reg add "HKEY_CURRENT_USER\SOFTWARE\Microsoft\TabletTip\1.7" /v TipbandDesiredVisibility /t REG_DWORD /d 1 /f


netsh advfirewall firewall add rule name = ZiiPOS_DB_Port dir = in protocol = tcp action = allow localport = 9899 profile = DOMAIN,PRIVATE,PUBLIC
netsh advfirewall firewall add rule name = ZiiPOS_DB_Port dir = out protocol = tcp action = allow localport = 9899 profile = DOMAIN,PRIVATE,PUBLIC
netsh advfirewall firewall add rule name = ZiiPOS_Port dir = in protocol = tcp action = allow localport = 8082 profile = DOMAIN,PRIVATE,PUBLIC
netsh advfirewall firewall add rule name = ZiiPOS_Port dir = out protocol = tcp action = allow localport = 8082  profile = DOMAIN,PRIVATE,PUBLIC


reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\HideDesktopIcons\NewStartPanel" /v "{20D04FE0-3AEA-1069-A2D8-08002B30309D}" /t REG_DWORD /d "00000000" /f
reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\HideDesktopIcons\ClassicStartMenu" /v "{20D04FE0-3AEA-1069-A2D8-08002B30309D}" /t REG_DWORD /d "00000000"/f
reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\HideDesktopIcons\NewStartPanel" /v "{5399E694-6CE5-4D6C-8FCE-1D8870FDCBA0}" /t REG_DWORD /d "00000000"/f
reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\HideDesktopIcons\ClassicStartMenu" /v "{5399E694-6CE5-4D6C-8FCE-1D8870FDCBA0}" /t REG_DWORD /d "00000000"/f


net stop wuauserv
sc config wuauserv start= disabled
reg add "HKEY_LOCAL_MACHINE\Software\Policies\Microsoft\Windows\WindowsUpdate\AU" /v NoAutoUpdate /t REG_DWORD /d "1" /f
reg add "HKEY_LOCAL_MACHINE\Software\Policies\Microsoft\Windows\WindowsUpdate\AU" /v AllowMUUpdateService /t REG_DWORD /d "1" /f
reg add "HKEY_LOCAL_MACHINE\Software\Policies\Microsoft\Windows\WindowsUpdate\AU" /v AUOptions /t REG_DWORD /d "1" /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\WindowsStore" /v AutoDownload /t REG_DWORD /d "2" /f
                           
schtasks /Change /TN "\Microsoft\Windows\WindowsUpdate\Scheduled Start" /Disable
schtasks /Change /TN "\Microsoft\Windows\Windows Defender\Windows Defender Scheduled Scan" /Disable


echo shutdown /r /f /t 10 > C:\Ziitech\Restart.bat
SCHTASKS /CREATE /SC DAILY /TN "ScheduledReboot" /TR "'C:\Ziitech\Restart.bat'" /ST 04:00 /RL HIGHEST
SCHTASKS /CREATE /SC DAILY /TN "TimeResync" /TR "w32tm /resync" /ST 23:00 /RL HIGHEST



exit''')
    systemConfigFile.close()
    file_exists = os.path.exists(SystemConfigurationFile)
    if (file_exists==True):
         print("SQLServer Configuration Batch File ready")
    else:
        print("SQLServer Configuration Batch File Create Error")
           
    
def createSQLServerAccountFile(directory):
    DBAccountSQLFile=directory+"\\ziiposAccount.sql"
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
   








def createProfilSettingFile():
    directory1="C:\\Program Files (x86)\\ZiiForce\\Zii.LocalServer"
    profilesFile=directory1+"\\profilesettings.json"
    #print(DBAccountSQLFile)
    profilesFileSet = open(profilesFile,'w')
    profilesFileSet.write(r'''
{
  "ProfileSetting": {
    "HttplistenPrefixes": "http://127.0.0.1:8082/",
    "MerchantId": "Fill-YOUR-MERCHANT-NAME",
    "BranchId": "FILL-YOUR-BRANCH-NAME",
    "DBType": "0",
    "DataSource": "localhost\\sqlexpress2008r2",
    "InitialCatalog": "ZiiPOS_DB",
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
        wget.download(downloadURL, filePath)


def downloadSyncTools(directory):
    downloadURL=syncToolDownloadURL
    filePath=directory+'\\ZiiSyncSetup-x86.exe'
    
    file_exists = os.path.exists(filePath)
    if (file_exists==True):
       print("\nSync Tools file Ready")
    else:
        print("Start to download Sync Tools ")
        wget.download(downloadURL, filePath)
        
def downloadSQLServerX64(directory):
    #SQLEXPRWT_2008R2_x64_ENU.exe
    downloadURL=DBx64downloadURL
    filePath1=directory+'\\SQLEXPRWT_2008R2_x64_ENU.exe'
    SQLserverInstalledFilePath="C:\\Program Files\\Microsoft SQL Server\\MSSQL15.SQLEXPRESS\\MSSQL"

    
    file_exists = os.path.exists(filePath1)
    sqlinstalltion =  os.path.exists(SQLserverInstalledFilePath)
    USBFileExist = os.path.exists(LocalFileSqlFile)


    if (file_exists==True):
        print("\nSQL Server X64 file Ready")
    elif(sqlinstalltion==True):    
        print("\nSQL Server X64 file Ready")

    elif(USBFileExist==True):
        shutil.copyfile(LocalFileSqlFile, filePath1)
    else:
        print("\nStart to download SQL Server X64 ")
        wget.download(downloadURL, filePath1)
 
        
       

def download7Zip(directory):
    #filePath = path+"\ZiiPOSRetail"+version+".exe"
    downloadURL=_7Zipx64DownloadURL
    filePath=directory+'\\z7z2201.exe'
    file_exists = os.path.exists(filePath)
    if (file_exists==True):
       print("\ndownload 7zip file Ready")
    else:
        print("\nStart to download 7Zip ")
        wget.download(downloadURL, filePath)
        
def downloadAnydesk(directory):
    #filePath = path+"\ZiiPOSRetail"+version+".exe"
    downloadURL=anydeskDownloadURL
    filePath=directory+'\\anydesk.msi'
    file_exists = os.path.exists(filePath)
    if (file_exists==True):
       print("\ndownload anydesk file Ready")
    else:
        print("\nStart to download anydesk ")
        wget.download(downloadURL, filePath)



#-----------------------------------------Install process------------------------------------------------------------------------------

def AnydeskInstallationProcess(directory):
    filePath=directory+'\\anydesk.msi'
    
    file_exists = os.path.exists(filePath)
    if (file_exists==True):
        print("anydesk Ready")
        runCMD1='cmd /c msiexec /i '+filePath+' /QN'
        os.system(runCMD1)
        runCMD2='cmd /c echo Ziitech123! | "C:\Program Files (x86)\AnyDeskMSI\AnyDeskMSI.exe" --set-password'
        os.system(runCMD2)
    else:
        print("Error: anydesk not exist")


def ZiiPOSInstallationProcess(FileToInstall):
    print("start")
    #runCMD1='cmd /c C:\Ziitech\killProcess.bat'
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
        #runCMD2='cmd /c C:\Ziitech\SQLServerConfiguration.bat'
        os.system(runCMD2)
    else:
        print("Error: SQLServerConfiguration.bat not exist")


def windowsSystemConfiguration(directory):
    filePath1=directory+'\\SystemConfiguration.bat'
    file_exists1 = os.path.exists(filePath1)
    if (file_exists1==True):
        print("Start to run windows configuration ")
        runCMD1='cmd /c '+filePath1
        #runCMD1='cmd /c C:\Ziitech\SystemConfiguration.bat'
        os.system(runCMD1)
    else:
        print("Error: SystemConfiguration.bat not exist")

def InstallDotNet35(directory):
  
    filePath1=directory+"\\dotNet35Install.bat"
    file_exists1 = os.path.exists(filePath1)
    if (file_exists1==True):
        print("Start to Install .net 3.5")
        runCMD1='cmd /c '+filePath1
        #runCMD1='cmd /c C:\Ziitech\dotNet35Install.bat'
        os.system(runCMD1)
    else:
        print("Error: dotNet35Install.bat not exist")

def InstallDotNetCore31(directory):
  
    filePath1=directory+"\\dotNet35Install.bat"
    file_exists1 = os.path.exists(filePath1)
    if (file_exists1==True):
        print("Start to Install .net 3.5")
        runCMD1='cmd /c '+filePath1
        #runCMD1='cmd /c C:\Ziitech\dotNet35Install.bat'
        os.system(runCMD1)
    else:
        print("Error: dotNet35Install.bat not exist")


def syncDateAndTime():
  
    runCMD1='cmd /c w32tm /resync'
    os.system(runCMD1)




def installZiiPOS(directory):
    downloadUrl=ZiiPOSdownloadUrl
    filePath = directory+"\\ZiiLocalServerSetup.exe"
    file_exists1 = os.path.exists(filePath)
    if (file_exists1==True):
        print("\nZiiLocalServerSetup is ready")
        runCMD1='cmd /c '+filePath+' /S'
        os.system(runCMD1)
        
    else:
        print("\nStart to download ZiiLocalServerSetup")
        downloadZiiPOS(downloadUrl,filePath)
        runCMD1='cmd /c '+filePath+' /S'
        os.system(runCMD1)



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
    createSQLServerInstallationBatchFile(directory)
    createSQLServerConfigurationBatchFile(directory)
    createSQLServerAccountFile(directory)
    createSystemConfigurationBatchFile(directory)
    createChocoInstallBatch(directory)

    
    
    # ------------Download files-----------------------
    downloadZiiPOSSQL(directory)
    downloadSyncTools(directory)
    downloadSQLServerX64(directory)
    downloadAnydesk(directory)

        
    # -----------Start Installation-------------------------
    AnydeskInstallationProcess(directory)
    InstallDotNet35(directory)    
    SQLServerInstallationProcess(directory)
    windowsSystemConfiguration(directory)
    installZiiPOS(directory)
    SyncToolsInstallationProcess(directory)
    runSQLDBBuild(directory)
    createProfilSettingFile()
    runChocoinstall(directory)



    

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
    downloadSyncTools(directory)

        
    # -----------Start Installation-------------------------
    
    installZiiPOS(directory)
    SyncToolsInstallationProcess(directory)
    runSQLDBBuild(directory)
    createProfilSettingFile()   
        
        
        
        
        
#-------------------------USB INSTALLATION--------------------------------------

def checkUSBFiles():
    returnFileValue=0
    #dir_path= os.path.dirname(os.path.realpath(__file__))
    dir_path=LocalFileDirectory
    filename1=dir_path+"\\03_Softwares\\AutoInstall\\00_InstallApps.bat"
    filename2=dir_path+"\\01_Softwares\\AutoInstall\\00_InstallApps.bat"
    #cwd = os.getcwd()
    print(dir_path)
    file_exists1 = os.path.exists(filename1)
    file_exists2 = os.path.exists(filename2)
    if (file_exists1==True):
        print(file_exists1)
        returnFileValue=filename1
        
    elif(file_exists2==True):
        print(file_exists2)
        returnFileValue=filename2
    else:
        returnFileValue=0
        
    return returnFileValue
    

    
    


 
#======================================= MAIN UI ===================================================================


class App:
    def __init__(self, root):
        
        #setting title
        root.title("ZiiPOS FB Deployment Tool V1.5")
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
        GButton_ZiiPOSDeployment["text"] = "Deploy ZiiPOS FB Server & SyncTool Only"
        GButton_ZiiPOSDeployment.place(x=40,y=90,width=250,height=52)
        GButton_ZiiPOSDeployment["command"] = self.GButton_ZiiPOSDeployment_command
        

        GButton_ZiiPOSRemoteFULL=tk.Button(root)
        GButton_ZiiPOSRemoteFULL["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_ZiiPOSRemoteFULL["font"] = ft
        GButton_ZiiPOSRemoteFULL["fg"] = "#000000"
        GButton_ZiiPOSRemoteFULL["justify"] = "center"
        GButton_ZiiPOSRemoteFULL["text"] = "Install ZiiPOS FB FULL"
        GButton_ZiiPOSRemoteFULL.place(x=40,y=20,width=250,height=52)
        GButton_ZiiPOSRemoteFULL["command"] = self.GButton_ZiiPOSRemoteFULL_command
        
        
        GButton_ZiiPOSUSB=tk.Button(root)
        GButton_ZiiPOSUSB["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_ZiiPOSUSB["font"] = ft
        GButton_ZiiPOSUSB["fg"] = "#000000"
        GButton_ZiiPOSUSB["justify"] = "center"
        GButton_ZiiPOSUSB["text"] = "Install ZiiPOS FB FULL From C:\\Ziitech_D"
        GButton_ZiiPOSUSB.place(x=40,y=160,width=250,height=52)
        GButton_ZiiPOSUSB["command"] = self.GButton_ZiiPOSInstallWithUSB


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
                    messagebox.showinfo(title="Installation Complete", message="ZiiPOS FULL System Deployment Complete")
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

        
        


       

    
    def GButton_ZiiPOSInstallWithUSB(self):
        status=checkIsAdmin()
        if "True"==str(status):
            getRestartStatus=restart_statues()
            SystemVersion=checkSystem()
            usbInstallFilePath=checkUSBFiles()

            if SystemVersion==64:    
                if getRestartStatus==0:
                    usbInstallFilePath=checkUSBFiles()
                    if usbInstallFilePath ==0:
                        messagebox.showinfo(title="File not exist", message="ZiiPOS Files are not exist, Please COPY Ziitech_D folder to C:\\")
                    else:
                        runCMD1='cmd /c '+usbInstallFilePath+' /S'
                        os.system(runCMD1)
                        print("Stage 1 Completed")
                        ZiiPOSDeployment()
                    
                        messagebox.showinfo(title="Installation Complete", message="ZiiPOS FB with USB Installation Complete")
                    
                    
                    
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
