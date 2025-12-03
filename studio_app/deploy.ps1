# Google Cloud Run Deployment Script

Write-Host "🚀 Starting Deployment to Google Cloud Run..." -ForegroundColor Green

# 1. Check Authentication
Write-Host "Checking gcloud authentication..."
gcloud auth print-identity_token > $null 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  You are not logged in. Opening login window..." -ForegroundColor Yellow
    gcloud auth login
}

# 2. Set Project
Write-Host "Setting project to musaix-pro..."
gcloud config set project musaix-pro

# 3. Deploy
Write-Host "Deploying to Cloud Run (this may take a few minutes)..."
# Note: We are not setting env vars here to keep them secure. 
# You should set them in the Cloud Console or via --set-env-vars
gcloud run deploy elevenlabs-studio `
    --source . `
    --region us-central1 `
    --allow-unauthenticated `
    --port 8080

Write-Host "✅ Deployment Complete!" -ForegroundColor Green
