curl -X POST \
  'https://testabcd.mocoapp.com/api/v1/users/employments' \
  -H 'Authorization: Token token=73c0d89f04b8914d79312239e3e4ca1b' \
  -H 'Content-Type: application/json' \
  -x http://127.0.0.1:8080 \
  -k \
  -d '{
        "user_id": 933665669,
        "pattern": {
          "am": [2,2,2,2,2],
          "pm": [2,2,2,2,2]
        }
      }'
