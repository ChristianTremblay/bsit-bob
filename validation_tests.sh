#!/bin/bash

pytest 'validate_cicd/test_1_create_samples.py'
pytest -vvv -s -n auto 'validate_cicd/test_2_infer_and_validate.py'
pytest -v 'validate_cicd/test_3_run_queries_on_inferred_ttl'