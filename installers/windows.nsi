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

;--------------------------------


; The name of the installer
Name "@SLUM@"

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
  File /r "@SLUM@"

  ; set maya and slum environment vars
  ${EnvVarUpdate} $0 "MAYA_PLUG_IN_PATH" 	"P" "HKLM" "$INSTDIR/python"
  ${EnvVarUpdate} $0 "SLUM_PATH" 			"P" "HKLM" "$INSTDIR"
  ${EnvVarUpdate} $0 "SLUM_SEARCH_PATH" 	"P" "HKLM" "$INSTDIR/shader"
  ;${EnvVarUpdate} $0 "PATH" "P" "HKCU" "%WinDir%\System32"                            ; Prepend
  ;${EnvVarUpdate} $0 "LIB"  "R" "HKLM" "C:\MyLib"                                     ; Remove
  ;${EnvVarUpdate} $0 "PATH" "R" "HKLM" "C:\Program Files\MyApp-v1.0"  ; Remove path of old rev
  ;${EnvVarUpdate} $0 "PATH" "A" "HKLM" "C:\Program Files\MyApp-v2.0"  ; Append the new one

  ; Write the uninstall keys for Windows
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\@SLUM@" "DisplayName" "SLUM (@SLUM@) - Shader Language Unified Manager"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\@SLUM@" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\@SLUM@" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\@SLUM@" "NoRepair" 1
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
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\@SLUM@"

  ${un.EnvVarUpdate} $0 "MAYA_PLUG_IN_PATH" 	"R" "HKLM" "$INSTDIR/python"
  ${un.EnvVarUpdate} $0 "SLUM_PATH" 			"R" "HKLM" "$INSTDIR"
  ${un.EnvVarUpdate} $0 "SLUM_SEARCH_PATH" 		"R" "HKLM" "$INSTDIR/shader"

  ; Remove files and uninstaller
  RMDir /r $INSTDIR\slumAlphaG
  Delete $INSTDIR\uninstall.exe

  ; Remove directories used
  RMDir "$INSTDIR"

SectionEnd
