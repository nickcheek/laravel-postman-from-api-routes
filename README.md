# Laravel to Postman Collection Converter

Convert Laravel route definitions to a Postman collection.

## Installation

```bash
pip install git+https://github.com/nickcheek/laravel-postman-from-api-routes.git
```

## Usage

```bash
# Convert routes file to Postman collection
laravel2postman /path/to/routes.php /path/to/output.json

# Or use as a Python module
from laravel_to_postman.main import convert_routes
convert_routes("/path/to/routes.php", "/path/to/output.json")
```

## Features

- Converts Laravel routes to Postman collection format
- Supports route groups with prefixes
- Handles resource routes
- Converts Laravel route parameters to Postman variables
- Organizes routes by base path
- Adds appropriate headers for JSON APIs
- Includes request body templates for POST/PUT/PATCH methods

## License

MIT License