Clear-Host
$calcs = $args[0]
$prefix = $args[1]
$beavrs_conf = 'BEAVRS_20_HFP_MULTI_5_2018.INP'

$current_path = $MyInvocation.MyCommand.Path

$parcs_configs = Join-Path $current_path ..\..\..\data | Join-Path -ChildPath ($prefix + "PARCS-configs")

$exec_path = '..\..\..\..\PARCS\' + 'p320mXX.exe' #location relative to \PARCS-configs\configX
 
<#
for($i = 0; $i -lt $calcs; $i++){ 
    $config = Join-Path $parcs_configs -ChildPath ('\config' + $i)
    Set-Location $config
    
    #powershell "$exec_path $beavrs_conf"

}
#>

Set-Location (Join-Path $current_path ..\ )
$nums = 0..$calcs

foreach ($num in $nums) {
    $running = @(Get-Job | Where-Object { $_.State -eq 'Running' })
    if ($running.Count -ge 4) {
        $running | Wait-Job -Any | Out-Null
    }

    Write-Host "Starting job for $num"
    Start-Job {
        Set-Location E:
        #$config = Join-Path $parcs_configs -ChildPath ('\config' + $num)
        pwd
        
        
        Start-Sleep 0
        
    } | Out-Null
}

# Wait for all jobs to complete and results ready to be received
Wait-Job * | Out-Null

# Process the results
foreach($job in Get-Job)
{
    $result = Receive-Job $job
    Write-Host $result
}

Remove-Job -State Completed