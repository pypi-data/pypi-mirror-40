# Flask-Philo-PynamoDB

![Flask-Philo Logo](https://raw.githubusercontent.com/Riffstation/Flask-Philo-Core/master/documentation/source/_static/banner_1.png)

Flask-Philo-PynamoDB is a [Flask-Philo-Core](http://flask-philo-core.readthedocs.io/en/latest/)  extension that use [PynamoDB](https://pynamodb.readthedocs.io/en/latest/) 
to connect to DynamoDB AWS.


## Configuration

[PynamoDB](https://pynamodb.readthedocs.io/en/latest/) is a great library that provides [Amazon DynamoDB](https://aws.amazon.com/dynamodb/) support out of the box.


You need to define the following configuration parameters in your Flask-Philo project:

```

    config = {
        'AWS': {
            'AWS_REGION': '',
            'AWS_ACCESS_KEY_ID': ,
            'AWS_SECRET_ACCESS_KEY': ,
        },
        'PYNAMODB': {
            'host': 'http://db:8000'
        }

    }
```


## Running Test Suite

We use docker and docker-compose for development, therefore you will need to install those two tools if you
want to run the test suite for this project. The following command runs the tests:


```
cd tests
python3 run_tests
```

## Resources

* [PynamoDB](https://pynamodb.readthedocs.io/en/latest/)

* [Amazon DynamoDB](https://aws.amazon.com/dynamodb/)

* [Flask-Philo-Core](http://flask-philo-core.readthedocs.io/en/latest/)
