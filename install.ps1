# Cài ttm-telegram (binary đã build sẵn) trên Windows. Không cần Python hay uv.
#   irm https://raw.githubusercontent.com/toantranmei/ttm-telegram/main/install.ps1 | iex
# Biến tùy chọn: $env:TTM_VERSION, $env:TTM_INSTALL_DIR, $env:TTM_BASE_URL
$ErrorActionPreference = "Stop"
$Name = "ttm-telegram"
$Repo = "toantranmei/ttm-telegram"
$InstallDir = if ($env:TTM_INSTALL_DIR) { $env:TTM_INSTALL_DIR } else { Join-Path $env:LOCALAPPDATA "ttm\bin" }
$Base = if ($env:TTM_BASE_URL) { $env:TTM_BASE_URL } elseif ($env:TTM_VERSION) { "https://github.com/$Repo/releases/download/$($env:TTM_VERSION)" } else { "https://github.com/$Repo/releases/latest/download" }

$arch = $env:PROCESSOR_ARCHITECTURE
if ($arch -ne "AMD64") { throw "Kiến trúc chưa hỗ trợ: $arch" }

$archive = "$Name-windows-x64.zip"
$tmp = Join-Path ([IO.Path]::GetTempPath()) ([Guid]::NewGuid())
New-Item -ItemType Directory -Path $tmp | Out-Null
try {
  Write-Host "Tải $archive ..."
  Invoke-WebRequest -Uri "$Base/$archive" -OutFile (Join-Path $tmp $archive) -UseBasicParsing
  Invoke-WebRequest -Uri "$Base/$archive.sha256" -OutFile (Join-Path $tmp "$archive.sha256") -UseBasicParsing

  $expected = (Get-Content (Join-Path $tmp "$archive.sha256") -Raw).Trim()
  $actual = (Get-FileHash (Join-Path $tmp $archive) -Algorithm SHA256).Hash.ToLower()
  if ($expected.ToLower() -ne $actual) { throw "Sai checksum. Dừng cài đặt." }

  Expand-Archive -Path (Join-Path $tmp $archive) -DestinationPath $tmp -Force
  New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
  Copy-Item -Path (Join-Path $tmp "$Name.exe") -Destination (Join-Path $InstallDir "$Name.exe") -Force
} finally {
  Remove-Item -Recurse -Force $tmp -ErrorAction SilentlyContinue
}

$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if (($userPath -split ";") -notcontains $InstallDir) {
  [Environment]::SetEnvironmentVariable("Path", (($userPath, $InstallDir) -join ";").TrimStart(";"), "User")
  Write-Host "Đã thêm $InstallDir vào PATH (mở lại terminal để có hiệu lực)."
}

Write-Host ""
Write-Host "Đã cài: $(Join-Path $InstallDir "$Name.exe")"
Write-Host "Chạy bước đăng nhập một lần trước: lệnh `ttm-telegram login` (xem README)."
Write-Host ""
Write-Host "Claude Desktop: tải bundle .mcpb ở trang Releases và mở file, rồi điền cấu hình trong giao diện."
