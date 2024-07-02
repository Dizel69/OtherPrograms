$headers = @{
    "Content-Type" = "application/json"
}

$body = @{
    "key" = "value"
}

Invoke-WebRequest -Uri "http://127.0.0.1:8000/data" -Method POST -Headers $headers -Body ($body | ConvertTo-Json)
