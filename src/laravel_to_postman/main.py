import re
import json
from collections import defaultdict
import os
import argparse
import sys

def extract_prefix(line):
    prefix_match = re.search(r'prefix\(\'([^\']+)\'', line)
    if prefix_match:
        return prefix_match.group(1).rstrip('/')
    return None

def process_group_routes(content):
    routes = []
    current_prefix = None

    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if 'prefix(' in line:
            prefix = extract_prefix(line)
            if prefix:
                current_prefix = prefix
                bracket_count = 1
                group_lines = []
                i += 1
                while i < len(lines) and bracket_count > 0:
                    if '{' in lines[i]:
                        bracket_count += 1
                    if '}' in lines[i]:
                        bracket_count -= 1
                    if bracket_count > 0:
                        group_lines.append(lines[i].strip())
                    i += 1

                for route_line in group_lines:
                    if re.match(r'^\s*Route::(get|post|put|patch|delete)', route_line):
                        path_match = re.search(r'\(\'([^\']+)\'', route_line)
                        if path_match:
                            original_path = path_match.group(1)
                            new_path = f"{current_prefix}{original_path}"
                            modified_line = route_line.replace(f"('{original_path}'", f"('{new_path}'")
                            routes.append(modified_line)

        elif re.match(r'^\s*Route::(get|post|put|patch|delete)', line):
            routes.append(line)
        elif re.match(r'^\s*Route::resource', line):
            routes.extend(expand_resource_route(line))

        i += 1

    return routes

def read_routes_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        return process_group_routes(content)

def expand_resource_route(resource_line):
    path_match = re.search(r'resource\(\'([^\']+)\'', resource_line)
    if not path_match:
        return []

    base_path = path_match.group(1)

    names = {}
    names_match = re.search(r'\[\'names\'=>\[(.*?)\]\]', resource_line)
    if names_match:
        names_str = names_match.group(1)
        name_pairs = re.findall(r'\'([^\']+)\'=>\'([^\']+)\'', names_str)
        names = dict(name_pairs)

    resource_routes = [
        ('get', '', 'index'),
        ('post', '', 'store'),
        ('get', '/{id}', 'show'),
        ('put', '/{id}', 'update'),
        ('delete', '/{id}', 'destroy')
    ]

    expanded_routes = []
    for method, path_suffix, action in resource_routes:
        full_path = base_path.rstrip('/') + path_suffix
        route_name = names.get(action, f"{base_path.strip('/')}.{action}")
        expanded_routes.append(f"Route::{method}('{full_path}')->name('{route_name}');")

    return expanded_routes

def parse_route(route_line):
    method_match = re.search(r'Route::(get|post|put|patch|delete)\(\'([^\']+)\'', route_line)
    if not method_match:
        return None

    method = method_match.group(1).upper()
    path = method_match.group(2)

    path = re.sub(r'{([^}]+)}', r':\1', path)

    name_match = re.search(r'->name\(\'([^\']+)\'\)', route_line)
    name = name_match.group(1) if name_match else path.replace('/', ' ').strip()

    return {
        'method': method,
        'path': path,
        'name': name
    }

def group_routes_by_base_path(routes):
    grouped_routes = defaultdict(list)

    for route in routes:
        if route:
            path_parts = route['path'].split('/')
            if len(path_parts) > 1:
                base_path = path_parts[1]
                grouped_routes[base_path].append(route)

    return grouped_routes

def create_postman_collection(grouped_routes):
    collection = {
        "info": {
            "name": "API Routes Collection",
            "description": "Generated from Laravel routes",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": []
    }

    for base_path, routes in sorted(grouped_routes.items()):
        folder = {
            "name": base_path.capitalize(),
            "item": []
        }

        sorted_routes = sorted(routes, key=lambda x: (x['method'], x['path']))

        for route in sorted_routes:
            request = {
                "name": f"{route['method']} {route['name']}",
                "request": {
                    "method": route['method'],
                    "url": {
                        "raw": "{{base_url}}/api" + route['path'],
                        "host": ["{{base_url}}"],
                        "path": ["api"] + [segment for segment in route['path'].strip('/').split('/') if segment]
                    },
                    "header": [
                        {
                            "key": "Accept",
                            "value": "application/json"
                        },
                        {
                            "key": "Content-Type",
                            "value": "application/json"
                        },
                        {
                            "key": "Authorization",
                            "value": "Bearer {{token}}"
                        }
                    ]
                }
            }

            if route['method'] in ['POST', 'PUT', 'PATCH']:
                request["request"]["body"] = {
                    "mode": "raw",
                    "raw": "{\n    \n}",
                    "options": {
                        "raw": {
                            "language": "json"
                        }
                    }
                }

            folder["item"].append(request)

        collection["item"].append(folder)

    return collection

def convert_routes(input_path, output_path):
    """Main function to convert routes file to Postman collection."""
    route_lines = read_routes_file(input_path)
    parsed_routes = [parse_route(line) for line in route_lines if line.strip()]
    parsed_routes = [r for r in parsed_routes if r is not None]
    grouped_routes = group_routes_by_base_path(parsed_routes)
    collection = create_postman_collection(grouped_routes)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(collection, f, indent=2)

def cli():
    """Command line interface for the converter."""
    parser = argparse.ArgumentParser(description='Convert Laravel routes to Postman collection')
    parser.add_argument('input_file', help='Path to Laravel routes.php file')
    parser.add_argument('output_file', help='Path to save Postman collection JSON')

    args = parser.parse_args()

    try:
        convert_routes(args.input_file, args.output_file)
        print(f"Successfully created Postman collection at {args.output_file}")
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    cli()