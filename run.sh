PATH="CHROME/PATH/HERE"

echo Starting Flask Server...
python3 app.py &

echo Starting Application...
$PATH --user-data-dir="C://Chrome dev session" --disable-web-security