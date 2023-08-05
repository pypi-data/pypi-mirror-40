import base64 as b64
import pickle
import json
from cryptography.fernet import Fernet
from functools import partial
import sys

from ..Printer import get_printer

def _serialize(obj,pickle_spec=pickle.DEFAULT_PROTOCOL):
    return pickle.dumps(obj,pickle_spec)

def _secure_serialize(obj, password, pickle_spec=pickle.DEFAULT_PROTOCOL):
    serialized = pickle.dumps(obj,pickle_spec)
    return Fernet(password).encrypt(serialized)

def pipeline2json(pipeline,
                    password=None,
                    pickle_spec=pickle.DEFAULT_PROTOCOL,
                    ):
    """

    """
    header = {}
    header[name] = pipeline.name
    header[num_blocks] = len(pipeline.blocks)
    header[pickle_spec] = pickle_spec
    header[encrypted] = False if (password is None) else True

    # define serialization function
    if header[encrypted]:
        serialize = lambda obj: _secure_serialize(obj, password, pickle_spec)
    else:
        serialize = lambda obj: _serialize(obj, pickle_spec)

    blocks = {}
    for i,block in enumerate(pipeline.blocks):
        block_data = {}
        block.prep_for_serialization()

        for key,val in block.__dict__.items():
            try:
                block_data[key] = serialize(val)
            except pickle.PickleError as e:
                # print out the traceback
                traceback.print_tb( sys.exc_info()[2] )
                # print out a message for debuggin
                printer = get_printer("{} - Serializer".format(block.name))
                printer.error("unable to serialize '{}', you may ".format(key),
                                "have to modify this variable in this block's",
                                " 'prep_for_serialization' function")
                del printer
                sys.exit(1)


        blocks[block.name] = block_data

    block_indicies = dict( enumerate(pipeline.names) )
    # forceably delete any variable containing a password
    del password
    del serialize

    pipeline_str = json.dumps(header)\
                    + json.dumps(block_indicies)\
                    + json.dumps(block_data)
    return pipeline_str
