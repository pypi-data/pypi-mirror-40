#!/usr/bin/env python3
import json
import logging

# import connexion
from connexion import NoContent

# Import utils
from tmlib.eiutils import toJson
# import db connection functions
from tmlib.tm_db import open_db


def get_schemas():
    logging.debug("In get_regokey")
    db_trading_minions = open_db()
    col_schemas = db_trading_minions.schemas
    logging.debug("Retrieving all schemas")
    results = list(col_schemas.find({}))
    logging.debug(str(len(results)) + " results returned.")
    if results:
        error_code = 200
        schemas = [json.loads(toJson(r)) for r in results]
        return schemas, error_code
    else:
        return NoContent, 404
