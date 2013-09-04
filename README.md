# Token Storage

Service for storing and retrieving user tokens.

## Generating Dummy Certificates (for testing)

http://lakm.us/logit/2013/01/https-server-client-certificate-pair-1-generate-openssl/

## Testing with cURL

```bash
curl -vvv https://localhost:7878/ --cert fixtures/client/certs/client1.crt --key fixtures/client/keys/client1.key --cacert fixtures/ca/myCA.crt
```
