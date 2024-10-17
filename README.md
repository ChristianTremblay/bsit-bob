# si-builder

This Python package makes it easier to build SI-WG models.

Build Samples by running

```python
pytest -v .\validate_cicd\test_create_samples.py
```

Validate by running

```python
pytest -s -vvvv -n auto validate_cicd/test_validation.py
```

# Querying sample models
Using `query_model` you can execute queries found in the sparql folder of sample and generate the result html files

```
query_model path_to_ttl_file path_to_sparql_queries
```