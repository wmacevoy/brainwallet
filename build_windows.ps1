# Build a zipped windows release of brainwallet
# For this script to work properly, the build system needs to be Windows 10(with Powershell >= v5.0) and have python installed
# If Powershell complains about being unable to execute scripts, open an administrative powershell terminal, navigate to the cloned repo, and run "Unblock-File -Path .\build_windows.ps1"

# Variables: Change these to your installed python version of choice and the name for the zip file
$PYTHON_VERSION="Python36"
$Release_Name="brainwallet"

cd $PSScriptRoot\brainwallet

# The python "scripts" directory and Windows 10 DLLs directory needed to be added to the PATH for pyinstaller to build properly on my machine
$env:PATH="$env:PATH%;$env:LocalAppData\Programs\Python\$PYTHON_VERSION\Scripts;C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x64"

# Test if pyinstaller is installed and install it if not
pyinstaller --version 2>&1 > $null

if (-Not ($?)) {
    echo "Installing pyinstaller"
    py -m pip install pyinstaller > $null
}

# Generate a Windows distribution
echo "Generating a spec"
pyinstaller --onefile brainwallet.py > $null

# Edit the spec to generate a binary containing all required libraries
# and datafiles, and move the binary to the root of the repo
echo "Editing spec and generating executable"

(Get-Content .\brainwallet.spec) -replace "datas=\[],", "datas=[('wordlist\*', 'wordlist')]," | Set-Content ".\brainwallet.spec" -Encoding Default

pyinstaller --onefile brainwallet.spec > $null

Move-Item "dist\brainwallet.exe" -Destination "..\$Release_Name.exe" -Force > $null

# Clean up remaining junk files from pyinstaller
  echo "Cleaning up"
  Remove-Item 'dist','build','brainwallet.spec' -Force -Recurse > $null
