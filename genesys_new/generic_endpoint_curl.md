curl -X POST http://10.35.130.34:5050/generic_endpoint \
-H "Content-Type: application/json" \
-d '{
  "user_id": "test_user",
  "query": "give me good SVG for CHAT icon in 20x20"
}'


curl -X POST http://10.35.130.34:5050/getSVG \
-H "Content-Type: application/json" \
-d '{
  "user_id": "test_user",
  "data": "CHAT APP"
}'
