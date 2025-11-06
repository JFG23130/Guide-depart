# Script de compression des images
# Réduit automatiquement les images de plus de 300KB

Write-Host "🖼️  Compression des images volumineuses..." -ForegroundColor Cyan

$imageDir = ".\images"
$targetSizeKB = 300

# Vérifier si ImageMagick est installé
$magick = Get-Command magick -ErrorAction SilentlyContinue

if (-not $magick) {
    Write-Host "❌ ImageMagick n'est pas installé." -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Solutions :" -ForegroundColor Yellow
    Write-Host "   1. Installer ImageMagick : https://imagemagick.org/script/download.php" -ForegroundColor Yellow
    Write-Host "   2. Utiliser un script alternatif basé sur Python PIL" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

Get-ChildItem -Path $imageDir -File | Where-Object {
    $_.Extension -match '\.(jpg|jpeg|png|JPG|JPEG|PNG)$'
} | ForEach-Object {
    $sizeKB = [math]::Round($_.Length / 1KB, 2)
    
    if ($sizeKB -gt $targetSizeKB) {
        Write-Host "📸 $($_.Name) : $sizeKB KB → compression..." -ForegroundColor Yellow
        
        $inputFile = $_.FullName
        $outputFile = [System.IO.Path]::Combine([System.IO.Path]::GetDirectoryName($inputFile), [System.IO.Path]::GetFileNameWithoutExtension($inputFile) + "_compressed" + $_.Extension)
        
        try {
            # Compression avec ImageMagick (qualité 80)
            if ($_.Extension -match '\.jpg|\.jpeg|\.JPG|\.JPEG') {
                & magick $inputFile -quality 80 $outputFile
            } else {
                # Pour PNG : conversion en JPG si > 500KB, sinon compression PNG
                if ($sizeKB -gt 500) {
                    $outputFile = $outputFile -replace '\.png$','.jpg'
                    & magick $inputFile -quality 85 $outputFile
                } else {
                    & magick $inputFile -quality 90 $outputFile
                }
            }
            
            $newSizeKB = [math]::Round((Get-Item $outputFile).Length / 1KB, 2)
            $reduction = [math]::Round((1 - ($newSizeKB / $sizeKB)) * 100, 1)
            
            Write-Host "   ✅ $($_.Name) : $sizeKB KB → $newSizeKB KB (-$reduction%)" -ForegroundColor Green
            
            # Remplacer l'original par la version compressée
            Remove-Item $inputFile -Force
            Rename-Item $outputFile $_.Name
            
        } catch {
            Write-Host "   ❌ Erreur lors de la compression de $($_.Name)" -ForegroundColor Red
        }
    }
}

Write-Host ""
Write-Host "✅ Compression terminée !" -ForegroundColor Green




