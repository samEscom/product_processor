# Product Processor

This lambda try create a product into a ecommerce platform using a SQS

## Getting started

Make sure you have installed

- [Python 3.9+](https://www.python.org/downloads/)


Install and use venv local:

```sh
git clone https://github.com/samEscom/product_processor.git
cd product_processor
make setup
```

## Testing

To run your tests, execute:

```sh
make tests
```
You can change the scope of the tests you want to run with the variable `TEST`:

```sh
make tests TEST=tests/routes
```

To run one specific test function, run:
```sh
make tests TEST={test/file.py}::{specific_test}
```

## Validations

To check your code against everything, run:

```sh
make lint
```

Some of the errors can be fixed automatically through:

```sh
make lint-fix
```

#### Contact

- Email: `# sa5m.escom@gmail.com`
