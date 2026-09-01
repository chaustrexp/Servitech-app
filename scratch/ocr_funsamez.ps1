Add-Type -AssemblyName System.Drawing
[Windows.Globalization.Language,Windows.Foundation.UniversalApiContract,ContentType=WindowsRuntime] | Out-Null
[Windows.Media.Ocr.OcrEngine,Windows.Foundation.UniversalApiContract,ContentType=WindowsRuntime] | Out-Null
[Windows.Graphics.Imaging.BitmapDecoder,Windows.Foundation.UniversalApiContract,ContentType=WindowsRuntime] | Out-Null

function Get-OcrText($imagePath) {
    $resolved = (Resolve-Path $imagePath).Path
    $file = [Windows.Storage.StorageFile]::GetFileFromPathAsync($resolved).GetAwaiter().GetResult()
    $stream = $file.OpenAsync([Windows.Storage.FileAccessMode]::Read).GetAwaiter().GetResult()
    $decoder = [Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream).GetAwaiter().GetResult()
    $bitmap = $decoder.GetSoftwareBitmapAsync().GetAwaiter().GetResult()
    $engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
    if (-not $engine) {
        $lang = [Windows.Globalization.Language]::new('es')
        $engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage($lang)
    }
    $ocrResult = $engine.RecognizeAsync($bitmap).GetAwaiter().GetResult()
    return $ocrResult.Text
}

Write-Output "=== OCR SLIDE 14 (Matriz Stakeholders) ==="
Get-OcrText "scratch\funsamez_img\slide_14_Marcador de contenido 5.png"

Write-Output "`n=== OCR SLIDE 15 (Herramienta Captura 1) ==="
Get-OcrText "scratch\funsamez_img\slide_15_Marcador de contenido 2.png"

Write-Output "`n=== OCR SLIDE 16 (Herramienta Captura 2) ==="
Get-OcrText "scratch\funsamez_img\slide_16_Marcador de contenido 6.png"

Write-Output "`n=== OCR SLIDE 17 (Requerimientos Funcionales) ==="
Get-OcrText "scratch\funsamez_img\slide_17_Imagen 6.png"

Write-Output "`n=== OCR SLIDE 18 (Requerimientos No Funcionales) ==="
Get-OcrText "scratch\funsamez_img\slide_18_Imagen 8.png"

Write-Output "`n=== OCR SLIDE 19 (Priorización MoSCoW) ==="
Get-OcrText "scratch\funsamez_img\slide_19_Imagen 2.png"
