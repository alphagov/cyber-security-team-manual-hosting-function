# firebreak-q1-faas

Just run this to build and deploy:
``` shell
make
```

To run the tests

``` shell
tox
```

To Deploy
Assume your STS Credentials

``` shell
cd terraform/firebreak-q1-event-normalisation/
terraform init
terraform apply
```

# Developing

Please add tests and documentation for your code.
Format all python code with [black](https://github.com/ambv/black)
