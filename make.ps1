#requires -version 3
<#
.SYNOPSIS
  <Overview of script>
.DESCRIPTION
  <Brief description of script>
.PARAMETER <Parameter_Name>
    <Brief description of parameter input required. Repeat this attribute if required>
.INPUTS
  <Inputs if any, otherwise state None>
.OUTPUTS
  <Outputs if any, otherwise state None - example: Log file stored in C:\Windows\Temp\<name>.log>
.NOTES
  Version:        1.0
  Author:         <Name>
  Creation Date:  <Date>
  Purpose/Change: Initial script development

.EXAMPLE
  <Example goes here. Repeat this attribute for more than one example>
#>

#-----------------------------------------------------------[Parameters]-----------------------------------------------------------

param(
  [switch]$clean = $false,
  [switch]$test = $false,
  [switch]$build = $false,
  [switch]$deploy = $false,
  [switch]$plandeploy = $false,
  [switch]$run = $false
)

#---------------------------------------------------------[Initialisations]--------------------------------------------------------

$PWD = Split-Path -parent $PSCommandPath
cd $PWD

#Set Error Action to Silently Continue
$ErrorActionPreference = "SilentlyContinue"

$TARGET_DIR = ".target"

#-----------------------------------------------------------[Execution]------------------------------------------------------------

if ($run -or (!$deploy -and !$build -and !$clean -and !$test -and !$plandeploy -and !$run)) {
  $build = $true
}

if ($clean) {
  Remove-Item -Recurse -Force .target, *.egg-info, .tox, venv, *.zip, .pytest_cache, htmlcov, **/__pycache__, **/*.pyc
}

if ($test) {
  $TEST_OUTPUT = tox 5>&1

  if ($TEST_OUTPUT -like "*commands failed*") {
    Write-Host -ForegroundColor Red "Tests failed."
    $TEST_OUTPUT
    exit
  } else {
    Write-Host -ForegroundColor Green "Tests passed!"
  }
}

if ($build) {

  if (Test-Path $TARGET_DIR) { Remove-Item $TARGET_DIR -Force -Recurse }
  mkdir $TARGET_DIR
  mkdir $TARGET_DIR\static

  cp -R firebreakq1faas/static/* .\$TARGET_DIR\static\
  cp firebreakq1faas/*.py .\$TARGET_DIR

  pip3 install -r requirements.txt -t $TARGET_DIR

  if (!$run) {
    $ZIPFILE = ".\firebreakq1faas.zip"
    if (Test-Path $ZIPFILE) { Remove-Item $ZIPFILE -Force }
    Compress-Archive .\$TARGET_DIR\* -DestinationPath $ZIPFILE
  }
}

if ($run) {
  python $TARGET_DIR\app.py
}

if ($plandeploy) {
  cd terraform/firebreak-q1-event-normalisation
  terraform plan
  cd ../../
}

if ($deploy) {
  cd terraform/firebreak-q1-event-normalisation
  terraform apply
  cd ../../
}
