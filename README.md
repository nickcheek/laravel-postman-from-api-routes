# Laravel Routes to Postman Collection Converter

Convert Laravel API routes to a Postman collection automatically. This tool parses your Laravel routes file and creates a structured Postman collection with proper request methods, headers, and parameters.

## Features

- Converts Laravel route definitions to Postman collection format
- Supports route groups with prefixes
- Handles resource routes (GET, POST, PUT, DELETE)
- Converts Laravel route parameters to Postman variables
- Organizes routes by base path
- Includes standard headers for API requests
- Adds request body templates for POST/PUT/PATCH methods

## Installation & Usage Options

### Option 1: Install via pip
```bash
# Install from GitHub
python3 -m pip install git+https://github.com/nickcheek/laravel-postman-from-api-routes.git

# Then use via command line
laravel2postman "/path/to/routes/api.php" "/path/to/output/collection.json"

# Or in a Python script
from laravel_to_postman.main import convert_routes
convert_routes("/path/to/routes/api.php", "/path/to/output/collection.json")
```

### Option 2: Direct Script Usage
```bash
# Clone the repository
git clone https://github.com/nickcheek/laravel-postman-from-api-routes.git
cd laravel-postman-from-api-routes

# Edit convert.py to set your paths
nano convert.py

# Run the script
python3 convert.py
```

Here's how convert.py should look:
```python
from laravel_to_postman.main import convert_routes

# Update these paths to match your system
convert_routes(
    "/path/to/your/api.php",
    "/path/to/your/output.json"
)
```

## Development Setup

If you want to contribute or modify the package:

```bash
# Clone the repository
git clone https://github.com/nickcheek/laravel-postman-from-api-routes.git
cd laravel-postman-from-api-routes

# Install in development mode
python3 -m pip install --upgrade pip
python3 -m pip install -e . --use-pep517
```

## Example

This tool will convert Laravel routes like this:
```php
Route::get('/users', [UserController::class, 'index']);
Route::post('/users', [UserController::class, 'store']);
Route::resource('/posts', PostController::class);

Route::prefix('/admin')->group(function () {
    Route::get('/settings', [AdminController::class, 'settings']);
});
```

Into a Postman collection with:
- Proper HTTP methods (GET, POST, etc.)
- Route parameters converted to Postman variables
- Organized folder structure
- Pre-configured headers
- Request body templates for POST/PUT methods

## Requirements
- Python 3.6 or higher
- pip (Python package installer)

## License

MIT License - See LICENSE file for details

## Author

Nicholas Cheek - [nick@nicholascheek.com](mailto:nick@nicholascheek.com)