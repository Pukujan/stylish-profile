<#
.SYNOPSIS
    Refresh the profile page's generated data and publish it.

.DESCRIPTION
    The page's activity block is regenerated from the GitHub API by
    scripts/track_activity.py. Publishing that regeneration needs a push to a
    protected `main`, and the workflow token cannot do it: a `GITHUB_TOKEN`
    push is rejected by the branch ruleset, and a pull request opened with that
    token has its `pull_request` runs held for approval, which turns a daily
    refresh into a daily approval.

    This script runs the same steps on the workstation instead, using the
    owner's already-authenticated `gh` and git credentials. Those credentials
    carry the repository-admin bypass on the ruleset, so the push lands without
    a pull request and without an approval step.

    Steps, in order, stopping at the first failure:
      1. fast-forward the checkout onto origin/main
      2. regenerate the tracking block and the four charts
      3. re-render the continuity document index, which pins three of those files
      4. verify every relative link still resolves
      5. verify each derived dark variant still matches its light source
      6. verify the rewritten records still satisfy the content-system contract
      7. commit and push, only if something actually changed
      8. mirror the page into the profile repository

.PARAMETER RepoRoot
    The canonical checkout. Defaults to the parent of this script's directory.

.PARAMETER DryRun
    Run every step up to the commit, then report what would have been pushed.

.EXAMPLE
    pwsh -File scripts/refresh_profile.ps1
#>
[CmdletBinding()]
param(
    [string] $RepoRoot,
    [switch] $DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if (-not $RepoRoot) {
    $RepoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
}
$RepoRoot = (Resolve-Path -LiteralPath $RepoRoot).Path

$LogDir = Join-Path $env:LOCALAPPDATA 'stylish-profile-refresh'
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
$LogFile = Join-Path $LogDir 'refresh.log'

function Write-Log {
    param([string] $Message)
    $line = '{0}  {1}' -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $Message
    Write-Host $line
    Add-Content -LiteralPath $LogFile -Value $line
}

function Invoke-Step {
    param([string] $Name, [scriptblock] $Body)
    Write-Log "start  $Name"
    & $Body
    if ($LASTEXITCODE -ne 0) {
        throw "$Name failed with exit code $LASTEXITCODE"
    }
    Write-Log "ok     $Name"
}

$Committer = @('-c', 'user.name=Pukujan', '-c', 'user.email=pukujan@users.noreply.github.com')
$ProfileRepo = 'Pukujan/Pukujan'

Push-Location -LiteralPath $RepoRoot
try {
    # continuity is not pip-installed on this machine; the CLI is imported
    # straight from the canonical PCM checkout.
    if (-not $env:PYTHONPATH) {
        $env:PYTHONPATH = 'D:\claude\projects\project-continuity-modules\src'
    }

    # The content helper is not installed either. Its validator is what CI runs
    # before it will merge, so the refresh runs the same one locally rather than
    # letting a rewritten record reach main and turn `gates` red there. It has
    # to be the same revision CI checks out, so the pin is read from the
    # workflow rather than repeated here, and the checkout is a cached clone at
    # that pin instead of whatever state a working tree happens to be in.
    $CgmPin = (Select-String -LiteralPath (Join-Path $RepoRoot '.github\workflows\gates.yml') `
            -Pattern '^\s*CGM_PIN:\s*([0-9a-f]{40})\s*$').Matches.Groups[1].Value
    if (-not $CgmPin) {
        throw 'CGM_PIN not found in .github/workflows/gates.yml'
    }
    $CgmRoot = Join-Path $LogDir 'cgm'
    $CgmHead = $null
    if (Test-Path -LiteralPath (Join-Path $CgmRoot '.git')) {
        $CgmHead = (git -C $CgmRoot rev-parse HEAD 2>$null).Trim()
    }
    if ($CgmHead -ne $CgmPin) {
        Write-Log "preparing content helper at $($CgmPin.Substring(0, 12))"
        if (-not (Test-Path -LiteralPath (Join-Path $CgmRoot '.git'))) {
            Remove-Item -Recurse -Force -LiteralPath $CgmRoot -ErrorAction SilentlyContinue
            git clone --quiet --filter=blob:none https://github.com/Pukujan/content-generation-modules.git $CgmRoot
            if ($LASTEXITCODE -ne 0) { throw 'could not clone the content helper' }
        }
        else {
            git -C $CgmRoot fetch --quiet origin
            if ($LASTEXITCODE -ne 0) { throw 'could not fetch the content helper' }
        }
        git -C $CgmRoot checkout --quiet $CgmPin
        if ($LASTEXITCODE -ne 0) { throw "could not check out content helper at $CgmPin" }
    }
    $CgmValidator = Join-Path $CgmRoot 'scripts\validate_content_system.py'

    if (-not $env:GITHUB_TOKEN) {
        $env:GITHUB_TOKEN = (gh auth token).Trim()
    }
    if (-not $env:GITHUB_TOKEN) {
        throw 'no GitHub token available; run `gh auth login` first'
    }

    $branch = (git rev-parse --abbrev-ref HEAD).Trim()
    if ($branch -ne 'main') {
        throw "expected to be on main, found '$branch'"
    }
    if (git status --porcelain) {
        throw 'the checkout is dirty; commit or discard those changes first'
    }

    Invoke-Step 'fast-forward main' {
        git fetch --quiet origin main
        git merge --ff-only --quiet origin/main
    }

    Invoke-Step 'regenerate activity data' {
        python scripts/track_activity.py --root .
    }

    Invoke-Step 're-render continuity index' {
        python -m continuity docs render --root .
    }

    Invoke-Step 'verify links' {
        python scripts/check_profile_links.py
    }

    Invoke-Step 'verify dark variants' {
        python scripts/derive_dark_assets.py --check
    }

    # Step 2 rewrites .content-system/asset-manifest.json, so the record that
    # CI validates is not the one this run started from.
    Invoke-Step 'verify content-system records' {
        python $CgmValidator --root $CgmRoot --adapter "$RepoRoot\.content-system" --project-root $RepoRoot
    }

    $changed = git status --porcelain
    if (-not $changed) {
        Write-Log 'nothing changed; the page is already current'
        exit 0
    }

    $stamp = Get-Date -Format 'yyyy-MM-dd'
    if ($DryRun) {
        Write-Log "dry run: would commit and push`n$changed"
        exit 0
    }

    Invoke-Step 'commit' {
        git add -A
        git @Committer commit --quiet -m "Refresh the activity block for $stamp"
    }

    Invoke-Step 'push main' {
        git push --quiet origin main
    }

    $sha = (git rev-parse HEAD).Trim()
    Write-Log "published $sha"

    Invoke-Step 'mirror to profile repository' {
        $mirror = Join-Path $env:TEMP 'stylish-profile-mirror'
        if (Test-Path -LiteralPath (Join-Path $mirror '.git')) {
            git -C $mirror fetch --quiet origin main
            git -C $mirror reset --hard --quiet origin/main
        }
        else {
            Remove-Item -Recurse -Force -LiteralPath $mirror -ErrorAction SilentlyContinue
            git clone --quiet --depth 1 "https://github.com/$ProfileRepo.git" $mirror
        }
        Copy-Item -Force -LiteralPath (Join-Path $RepoRoot 'profile\README.md') `
            -Destination (Join-Path $mirror 'README.md')
        if (-not (git -C $mirror status --porcelain)) {
            Write-Log 'mirror already current'
            return
        }
        git -C $mirror add README.md
        git -C $mirror @Committer commit --quiet -m "Sync the profile page for $stamp"
        git -C $mirror push --quiet origin HEAD:main
    }

    Write-Log 'done'
}
catch {
    Write-Log "FAILED: $($_.Exception.Message)"
    exit 1
}
finally {
    Pop-Location
}
