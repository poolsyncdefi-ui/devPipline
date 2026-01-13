# Activate.ps1 for Windows
function global:deactivate ([switch]$NonDestructive) {
    if (Test-Path variable:_OLD_VIRTUAL_PATH) {
        $env:PATH = $variable:_OLD_VIRTUAL_PATH
        Remove-Variable "_OLD_VIRTUAL_PATH" -Scope global
    }

    if (Test-Path variable:_OLD_VIRTUAL_PYTHONHOME) {
        $env:PYTHONHOME = $variable:_OLD_VIRTUAL_PYTHONHOME
        Remove-Variable "_OLD_VIRTUAL_PYTHONHOME" -Scope global
    }

    if (Test-Path function:_old_virtual_prompt) {
        $function:prompt = $function:_old_virtual_prompt
        Remove-Item function:\_old_virtual_prompt
    }

    if (!$NonDestructive) {
        Remove-Item function:deactivate
    }
}

deactivate -nondestructive
$env:VIRTUAL_ENV = "C:\Web3Projects\NFTMarketplace\venv"
$env:PYTHONHOME = ""
$env:_OLD_VIRTUAL_PATH = $env:PATH
$env:PATH = "$env:VIRTUAL_ENV\Scripts;" + $env:PATH

function _old_virtual_prompt {
    ""
}
$function:_old_virtual_prompt = $function:prompt

function global:prompt {
    Write-Host "(venv) " -NoNewline
    _old_virtual_prompt
}
