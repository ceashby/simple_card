# simple_card

The server is online at http://138.68.176.243/

## Example api usage
```
curl 127.0.0.1:8000/api/create_card/    -d '{"card_number":1234}'
curl 127.0.0.1:8000/api/load/           -d '{"card_number": 1234, "amount":100}'

curl 127.0.0.1:8000/api/authorise/      -d '{"card_number": 1234, "amount":20}'
responds with transaction_id

curl 127.0.0.1:8000/api/capture/        -d '{"card_number": 1234, "transaction_id":1, "amount":20}'
curl 127.0.0.1:8000/api/refund/         -d '{"card_number": 1234, "transaction_id":1, "amount":20}'
curl 127.0.0.1:8000/api/reverse/        -d '{"card_number": 1234, "transaction_id":1, "amount":20}'
```
