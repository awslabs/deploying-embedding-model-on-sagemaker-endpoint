## Execution Guide
### Run Flask directly on local
```shell
$ make run
```
This command runs Flask directly without using nginx - gunicorn - wsgi - flask call layers, \
so it is useful when testing the operation of the inference code itself.

It uses port 5001 by default, and can be tested as follows:

#### Test `/ping`
```shell
$ curl -XGET localhost:5001/ping

OK 
```

#### Test `/invocation`
```shell
$ curl -XPOST localhost:5001/invocations -H 'Content-Type:application/json' -d'{"message": "Hello World"}'

[
  0.00121,
  -0.0023401
]
```

### Build Dockerize container on local environment
```shell
$ make build 
```

### Build and run container on local Docker environment
````shell
$ make docker-run 
````
This follows the nginx - gunicorn - wsgi - flask call structure. \
It has the same structure as calling a SageMaker endpoint, so it can be used to test before deploying to ECR.

### Build and push to ECR after building on local environment
```shell
$ make build_and_push image=<IMAGE_NAME_TO_PUSH>
```
This builds the container image on the local Docker environment and pushes it to ECR. \
To upload to ECR, the AWS authentication profile must be set up. \
If you want to use a separate profile instead of the default, run it as follows to specify the profile.

```shell
$ AWS_PROFILE=<PROFILE_NAME_TO_USE> make build_and_push image=<IMAGE_NAME_TO_PUSH>
```

---

---

## Test by invoking deployed endpoint
```python
import boto3

payload = "HelloWorld"
endpoint_name = "sample-embedding-model"

sm_runtime = boto3.client("runtime.sagemaker")
response = sm_runtime.invoke_endpoint(
    EndpointName=endpoint_name,
    Body=payload
)
response_str = response["Body"].read().decode()
print(response_str)
```

---


## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

