#!/usr/bin/python3
"""objects that handle all default REStfull APi actions for states"""
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def count(self, cls=None):
    """counts objects in the database"""
    my_dict = self.all(cls)
    return (len(my_dict))
