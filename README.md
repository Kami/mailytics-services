# Token Storage

Service for storing and retrieving user tokens.

## Generating Dummy Certificates (for testing)

http://lakm.us/logit/2013/01/https-server-client-certificate-pair-1-generate-openssl/

## Testing with cURL

```bash
curl -vvv https://localhost:8888/ --cert client/certs/client1.crt --key client/keys/client1.key --cacert ca/myCA.crt
```
