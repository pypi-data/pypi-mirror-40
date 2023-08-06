# AWS Jar
[![PyPI version](https://badge.fury.io/py/awsjar.svg)](https://badge.fury.io/py/awsjar)
[![Python 3.6](https://img.shields.io/badge/python-3.5+-blue.svg)](https://www.python.org/downloads/release/python-360/)
<a href="https://github.com/ambv/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
[Jar](https://github.com/ysawa0/awsjar) makes it easy to save the state of your AWS Lambda functions.
The data (either a dict or list) can be saved with the Lambda itself as an Environment Variable or on S3.

```
pip install awsjar
```

```
import awsjar as aj

# Save your data with the Lambda itself, as an Environment Variable.
jar = aj.Jar(lambda_name='sams-lambda')
data = {'num_acorns': 50, 'acorn_hideouts': ['tree', 'lake', 'backyard']}
jar.put(data)

state = jar.get()
>> {'num_acorns': 50, 'acorn_hideouts': ['tree', 'lake', 'backyard']}

```

```
import awsjar as aj

# Save your data to an S3 object - s3://my-bucket/state.json 
bkt = aj.Bucket(bucket='my-bucket', key='state.json')

data = {'num_acorns': 50, 'acorn_hideouts': ['tree', 'lake', 'backyard']}
bkt.put(data)

state = bkt.get()
>> {'num_acorns': 50, 'acorn_hideouts': ['tree', 'lake', 'backyard']}
```

## Docs
[User Guide](guide.md)

## Contributing

Please see the [contributing guide](CONTRIBUTING.md) for more specifics.

## Contact

Please use the [Issues](https://github.com/edmunds/shadowreader/issues) page

## License

Distributed under the Apache License 2.0. See [`LICENSE`](LICENSE) for more information.
