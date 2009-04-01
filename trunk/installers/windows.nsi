; slum.nsi
;
; This script is based on example2.nsi, but it remember the directory,
; has uninstall support and (optionally) installs start menu shortcuts.
;
; It will install example2.nsi into a directory that the user selects,

;--------------------------------


;--------------------------------
;Include Modern UI

  !include "MUI2.nsh"
  !include "installers\nsi_include\envVarUpdate.nsh"


Function .onInit
 
  ReadRegStr $R0 HKLM \
  "Software\Microsoft\Windows\CurrentVersion\Uninstall\slum" \
  "UninstallString"
  StrCmp $R0 "" done
 
  MessageBox MB_OKCANCEL|MB_ICONEXCLAMATION \
  "Slum is already installed. $\n$\nClick `OK` to remove the \
  previous version or `Cancel` to cancel this upgrade." \
  IDOK uninst
  Abort
 
;Run the uninstaller
uninst:
  ClearErrors
  ExecWait '$R0 _?=$INSTDIR' $0 ;$INSTDIR\uninst.exe ; instead of the ExecWait line
  
  DetailPrint "some program returned $0"

  ;ExecWait '$R0 _?=$INSTDIR' ;Do not copy the uninstaller to a temp file
 
  ;IfErrors no_remove_uninstaller
    ;You can either use Delete /REBOOTOK in the uninstaller or add some code
    ;here to remove the uninstaller. Use a registry key to check
    ;whether the user has chosen to uninstall. If you are using an uninstaller
    ;components page, make sure all sections are uninstalled.
  ;no_remove_uninstaller:
 
done:
 
FunctionEnd
;--------------------------------



; The name of the installer
Name "slum"

; The file to write
OutFile "@SLUM@_Windows.exe"

; The default installation directory
InstallDir $PROGRAMFILES\slum


; Request application privileges for Windows Vista
RequestExecutionLevel admin
;RequestExecutionLevel user


;--------------------------------
;Interface Settings

  !define MUI_ABORTWARNING

;--------------------------------
;Pages

  !insertmacro MUI_PAGE_LICENSE "license.txt"
  !insertmacro MUI_PAGE_COMPONENTS
  !insertmacro MUI_PAGE_DIRECTORY
  !insertmacro MUI_PAGE_INSTFILES

  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES

;--------------------------------
;Languages

  !insertmacro MUI_LANGUAGE "English"

;--------------------------------
;Installer Sections
;--------------------------------

; Pages

;Page components
;Page directory
;Page instfiles

;UninstPage uninstConfirm
;UninstPage instfiles

;--------------------------------

; The stuff to install
Section "Slum (required)"

  SectionIn RO

  ; Set output path to the installation directory.
  SetOutPath $INSTDIR

  ; Put file there
  File /r @SLUM@\*.*

  ; create custom shader dir
  CreateDirectory $DOCUMENTS\slum
  
  ; set maya and slum environment vars
  ${EnvVarUpdate} $0 "PYTHONPATH"		 	"P" "HKLM" "$INSTDIR\python"
  ${EnvVarUpdate} $0 "MAYA_PLUG_IN_PATH" 	"P" "HKLM" "$INSTDIR\python"
  ${EnvVarUpdate} $0 "SLUM_PATH" 			"P" "HKLM" "$INSTDIR"
  ${EnvVarUpdate} $0 "SLUM_SEARCH_PATH" 	"P" "HKLM" "$DOCUMENTS\slum"
  ${EnvVarUpdate} $0 "SLUM_SEARCH_PATH" 	"P" "HKLM" "$INSTDIR\shader"
  ;${EnvVarUpdate} $0 "PATH" "P" "HKCU" "%WinDir%\System32"                            ; Prepend
  ;${EnvVarUpdate} $0 "LIB"  "R" "HKLM" "C:\MyLib"                                     ; Remove
  ;${EnvVarUpdate} $0 "PATH" "R" "HKLM" "C:\Program Files\MyApp-v1.0"  ; Remove path of old rev
  ;${EnvVarUpdate} $0 "PATH" "A" "HKLM" "C:\Program Files\MyApp-v2.0"  ; Append the new one

  ; Write the uninstall keys for Windows
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\slum" "DisplayName" "SLUM (@SLUM@) - Shader Language Unified Manager"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\slum" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\slum" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\slum" "NoRepair" 1
  WriteUninstaller "uninstall.exe"

SectionEnd

; Optional section (can be disabled by the user)
;Section "Start Menu Shortcuts"
;
;  CreateDirectory "$SMPROGRAMS\Example2"
;  CreateShortCut "$SMPROGRAMS\Example2\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
;  CreateShortCut "$SMPROGRAMS\Example2\Example2 (MakeNSISW).lnk" "$INSTDIR\example2.nsi" "" "$INSTDIR\example2.nsi" 0
;
;SectionEnd

;--------------------------------

; Uninstaller

Section "Uninstall"
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\slum"

  ${un.EnvVarUpdate} $0 "PYTHONPATH" 			"R" "HKLM" "$INSTDIR\python"
  ${un.EnvVarUpdate} $0 "MAYA_PLUG_IN_PATH" 	"R" "HKLM" "$INSTDIR\python"
  ${un.EnvVarUpdate} $0 "SLUM_PATH" 			"R" "HKLM" "$INSTDIR"
  ${un.EnvVarUpdate} $0 "SLUM_SEARCH_PATH" 		"R" "HKLM" "$DOCUMENTS\slum"
  ${un.EnvVarUpdate} $0 "SLUM_SEARCH_PATH" 		"R" "HKLM" "$INSTDIR\shader"

  ; Remove files and uninstaller
  RMDir /r $INSTDIR\@SLUM@
  ;RMDir /r  $DOCUMENTS\slum
  Delete $INSTDIR\uninstall.exe

  ; Remove directories used
  RMDir /r "$INSTDIR"

SectionEnd
