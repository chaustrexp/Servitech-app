Add-Type -AssemblyName System.Runtime.WindowsRuntime
$asTaskGeneric = [System.WindowsRuntimeSystemExtensions].GetMethods() | ? { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' }

function Await-WinRt($asyncOp, $type) {
    $asTask = $asTaskGeneric.MakeGenericMethod($type)
    $task = $asTask.Invoke($null, @($asyncOp))
    $task.Wait()
    return $task.Result
}

[Windows.Globalization.Language,Windows.Foundation.UniversalApiContract,ContentType=WindowsRuntime] | Out-Null
[Windows.Media.Ocr.OcrEngine,Windows.Foundation.UniversalApiContract,ContentType=WindowsRuntime] | Out-Null
[Windows.Graphics.Imaging.BitmapDecoder,Windows.Foundation.UniversalApiContract,ContentType=WindowsRuntime] | Out-Null
[Windows.Storage.StorageFile,Windows.Foundation.UniversalApiContract,ContentType=WindowsRuntime] | Out-Null

function Get-Ocr($path) {
    $fullPath = (Resolve-Path $path).Path
    $fileOp = [Windows.Storage.StorageFile]::GetFileFromPathAsync($fullPath)
    $file = Await-WinRt $fileOp ([Windows.Storage.StorageFile])
    
    $streamOp = $file.OpenAsync([Windows.Storage.FileAccessMode]::Read)
    $stream = Await-WinRt $streamOp ([Windows.Storage.Streams.IRandomAccessStream])
    
    $decOp = [Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)
    $decoder = Await-WinRt $decOp ([Windows.Graphics.Imaging.BitmapDecoder])
    
    $bmpOp = $decoder.GetSoftwareBitmapAsync()
    $bitmap = Await-WinRt $bmpOp ([Windows.Graphics.Imaging.SoftwareBitmap])
    
    $lang = [Windows.Globalization.Language]::new('es')
    $engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage($lang)
    if (-not $engine) {
        $engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
    }
    
    $ocrOp = $engine.RecognizeAsync($bitmap)
    $res = Await-WinRt $ocrOp ([Windows.Media.Ocr.OcrResult])
    return $res.Text
}

foreach ($f in (Get-ChildItem scratch\funsamez_img\*.png)) {
    Write-Output "========================================"
    Write-Output "FILE: $($f.Name)"
    Write-Output "========================================"
    Get-Ocr $f.FullName
}
