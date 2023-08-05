# pyfluentformio

Python version of FluentJS. Allows users to perform GET and POST requests to Form.io resources and forms. It also allows the use of filters and method chaining.

## Usage

```python
from pyfluent-formio import Fluent

connector = Fluent(baseUrl = 'FORMIO BASE URL', resourcePath='FORMIO RESOURCE PATH', token='FORMIO API TOKEN')

connector.get()
```

## License

MIT
