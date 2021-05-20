Clear-Host
$calcs = $args[0]
$prefix = $args[1]
$beavrs_conf = 'BEAVRS_20_HFP_MULTI_5_2018.INP'

$current_path = $MyInvocation.MyCommand.Path

$parcs_configs = Join-Path $current_path ..\..\..\data

for($i = 0; $i -lt $calcs; $i++){
    Set-Location $parcs_configs

    $exec_path = '..\..\..\PARCS\' + 'p320mXX.exe'
    $parcs_config = $parcs_configs +'\'+ $prefix +'PARCS-configs\config' + $i
    Set-Location $parcs_config 
    $pwd
    
    powershell "$exec_path $beavrs_conf"
}