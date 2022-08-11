$root = $PSScriptRoot
Write-Host "<<<register_tls>>>"
if (-not (Test-Path $root\powershell-yaml-0.4.2\powershell-yaml.psd1)) {
    Expand-Archive $root\powershell-yaml-0.4.2.zip -DestinationPath $root
}
Import-Module $root\powershell-yaml-0.4.2\powershell-yaml.psd1

$content = Get-Content -raw "$((Get-ChildItem 'Env:\ProgramFiles(x86)').value)\checkmk\service\install\check_mk.install.yml"
$updateState = "C:\ProgramData\CheckMK\Agent\config\cmk-update-agent.state"
$yaml = ConvertFrom-Yaml -Yaml $content
$tls_site = $yaml.register_tls.tls_site
$tls_password = $yaml.register_tls.tls_password
$tls_server = $yaml.register_tls.tls_server
$tls_username = $yaml.register_tls.tls_username
$tls_usedevicehostname = $yaml.register_tls.tls_usedevicehostname
$exe = "$((Get-ChildItem 'Env:\ProgramFiles(x86)').value)\checkmk\service\cmk-agent-ctl.exe"

if ([string]::IsNullOrEmpty($tls_site)) {
    $json = (Get-Content -Raw -Path $updateState  | Out-String).Replace(": None", ": 'None'")  | ConvertFrom-Json
    $tls_site = $json.site
}


$status = & $exe  status
if (($status | Out-String) -notlike "*$tls_server*$tls_site*") {
    Write-Host "Not TLS registered"

    
    if ((Test-Path $updateState) -and ($tls_usedevicehostname -notlike "True")) {
        $json = (Get-Content -Raw -Path $updateState  | Out-String).Replace(": None", ": 'None'")  | ConvertFrom-Json
        $hostname = $json.host_name
    }
    else {
        $hostname = $($env:COMPUTERNAME).ToLower()
    }
    $reg = & $exe  register --trust-cert -H $hostname -s $tls_server -P $tls_password -U $tls_username -i $tls_site
}
else {
    Write-Host "TLS registered"
}
