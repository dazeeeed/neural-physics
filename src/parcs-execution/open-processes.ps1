﻿Clear-Host
$calcs = $args[0]
$prefix = $args[1]
$beavrs_conf = 'BEAVRS_20_HFP_MULTI_5_2018.INP'

$current_path = $MyInvocation.MyCommand.Path

$parcs_configs = Join-Path $current_path ..\..\..\data | Join-Path -ChildPath ($prefix + "PARCS-configs")

$exec_path = '..\..\..\..\PARCS\' + 'p320mXX.exe' #location relative to \PARCS-configs\configX
 

for($i = 0; $i -lt $calcs; $i++){ 
    $config = Join-Path $parcs_configs -ChildPath ('\config' + $i)
    Set-Location $config
    
    powershell "$exec_path $beavrs_conf"

}