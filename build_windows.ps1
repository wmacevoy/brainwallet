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
pyinstaller --version > $null

if (-Not ($?)) {
    py -m pip install pyinstaller
}

# Generate a Windows distribution
pyinstaller brainwallet.py -y

# Copy the wordlist into the brainwallet distribution directory
Copy-Item -recurse "wordlist" -Destination "dist\brainwallet\wordlist"

# Make a zip in the root of the repo with the desired name
Compress-Archive -Path ".\dist\brainwallet\*" -CompressionLevel Optimal -DestinationPath "..\$Release_Name" -Force

# Clean up remaining junk files from pyinstaller
Remove-Item 'dist','build','brainwallet.spec' -Force -Recurse
