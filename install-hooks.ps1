#!/usr/bin/env pwsh

<#
.SYNOPSIS
Install Git hooks from this collection into a Git repository

.DESCRIPTION
This script copies the Git hooks from this collection into the .git/hooks directory
of a specified Git repository, making them executable and removing any suffixes.

.PARAMETER RepoPath
The path to the Git repository where hooks should be installed

.PARAMETER HookTypes
Array of hook types to install (e.g., @("pre-commit", "commit-msg"))
If not specified, will install all available hooks

.EXAMPLE
.\install-hooks.ps1 -RepoPath "C:\path\to\your\repo"

.EXAMPLE
.\install-hooks.ps1 -RepoPath "C:\path\to\your\repo" -HookTypes @("pre-commit", "commit-msg")
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$RepoPath,
    
    [Parameter(Mandatory=$false)]
    [string[]]$HookTypes = @()
)

# Function to check if a directory is a Git repository
function Test-GitRepository {
    param([string]$Path)
    
    if (-not (Test-Path $Path)) {
        return $false
    }
    
    $gitDir = Join-Path $Path ".git"
    return (Test-Path $gitDir)
}

# Function to get all available hook types
function Get-AvailableHookTypes {
    $hookDirs = Get-ChildItem -Path $PSScriptRoot -Directory | Where-Object { $_.Name -ne ".git" -and $_.Name -ne "node_modules" }
    return $hookDirs.Name
}

# Main installation logic
function Install-GitHooks {
    param(
        [string]$RepoPath,
        [string[]]$HookTypes
    )
    
    # Validate repository
    if (-not (Test-GitRepository $RepoPath)) {
        Write-Error "The specified path is not a Git repository: $RepoPath"
        return
    }
    
    $hooksDir = Join-Path $RepoPath ".git\hooks"
    
    # Get hook types to install
    if ($HookTypes.Count -eq 0) {
        $HookTypes = Get-AvailableHookTypes
        Write-Host "Installing all available hook types: $($HookTypes -join ', ')" -ForegroundColor Green
    } else {
        Write-Host "Installing specified hook types: $($HookTypes -join ', ')" -ForegroundColor Green
    }
    
    foreach ($hookType in $HookTypes) {
        $sourceDir = Join-Path $PSScriptRoot $hookType
        
        if (-not (Test-Path $sourceDir)) {
            Write-Warning "Hook type directory not found: $hookType"
            continue
        }
        
        # Get hook files (exclude README.md)
        $hookFiles = Get-ChildItem -Path $sourceDir -File | Where-Object { $_.Name -ne "README.md" }
        
        foreach ($hookFile in $hookFiles) {
            # Remove any suffix from the hook name (e.g., format-code.hook becomes pre-commit)
            $hookName = $hookType
            $destPath = Join-Path $hooksDir $hookName
            
            # If multiple hooks of the same type exist, we'll need to choose one or combine them
            if ($hookFiles.Count -gt 1) {
                Write-Host "Multiple $hookType hooks found:" -ForegroundColor Yellow
                for ($i = 0; $i -lt $hookFiles.Count; $i++) {
                    Write-Host "  [$i] $($hookFiles[$i].Name)" -ForegroundColor Yellow
                }
                
                $choice = Read-Host "Select which $hookType hook to install (0-$($hookFiles.Count-1)), or 'skip' to skip this hook type"
                
                if ($choice -eq "skip") {
                    Write-Host "Skipping $hookType" -ForegroundColor Yellow
                    break
                }
                
                try {
                    $selectedIndex = [int]$choice
                    if ($selectedIndex -ge 0 -and $selectedIndex -lt $hookFiles.Count) {
                        $hookFile = $hookFiles[$selectedIndex]
                    } else {
                        Write-Warning "Invalid selection for $hookType. Skipping."
                        continue
                    }
                } catch {
                    Write-Warning "Invalid selection for $hookType. Skipping."
                    continue
                }
            }
            
            # Copy the hook file
            try {
                Copy-Item -Path $hookFile.FullName -Destination $destPath -Force
                Write-Host "Installed: $hookType ($($hookFile.Name))" -ForegroundColor Green
                
                # On Windows, we don't need to set execute permissions like on Unix systems
                # But we can verify the file was copied correctly
                if (Test-Path $destPath) {
                    Write-Host "  -> Successfully copied to $destPath" -ForegroundColor Gray
                }
            } catch {
                Write-Error "Failed to install $hookType`: $($_.Exception.Message)"
            }
        }
    }
    
    Write-Host "`nHook installation completed!" -ForegroundColor Green
    Write-Host "Hooks installed in: $hooksDir" -ForegroundColor Gray
}

# Execute the installation
try {
    Install-GitHooks -RepoPath $RepoPath -HookTypes $HookTypes
} catch {
    Write-Error "Installation failed: $($_.Exception.Message)"
    exit 1
}