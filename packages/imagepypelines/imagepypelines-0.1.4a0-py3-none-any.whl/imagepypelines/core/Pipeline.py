# @Email: jmaggio14@gmail.com
# @Website: https://www.imagepypelines.org/
# @License: https://github.com/jmaggio14/imagepypelines/blob/master/LICENSE
# @github: https://github.com/jmaggio14/imagepypelines
#
# Copyright (c) 2018 Jeff Maggio, Nathan Dileas, Ryan Hartzell
from __future__ import print_function
from .Printer import get_printer
from .Printer import set_global_printout_level
from .BaseBlock import BaseBlock
from .BaseBlock import ArrayType
from .Exceptions import CrackedPipeline
from .Exceptions import IncompatibleTypes
import collections
from .util.timing import Timer
import pickle
import collections
import copy
import numpy as np

def restore_from_file(filename):
    """restores a pipeline from a pickled file

    Args:
        filename(str): the pipeline filename

    Returns:
        pipeline(ip.Pipeline): the loaded pipeline
    """
    with open(filename,'rb') as f:
        raw = f.read()
    return restore_from_pickle(raw)


def restore_from_pickle(pickled_pipeline):
    """restores a pipeline from a pickled state

    Args:
        pickled_pipeline(pickled obj): a pickled pipeline

    Returns:
        pipeline(ip.Pipeline): the loaded pipeline
    """
    pipeline = pickle.loads(pickled_pipeline)
    for b in pipeline.blocks:
        b.restore_from_serialization()

    return pipeline


def get_type(datum):
    """retrieves the block data type of the input datum"""
    if isinstance(datum,(str,)):
        return (str,)

    elif isinstance(datum,float):
        return (float,)

    elif isinstance(datum,int):
        return (int,)

    elif isinstance(datum,(np.ndarray,)):
        return (ArrayType(datum.shape,dtypes=datum.dtype),)

    else:
        msg = "only acceptable input datatypes are numpy arrays, floats, ints and strings"
        raise ValueError(msg)

class Pipeline(object):
    """
        Pipeline object to apply a sequence of algorithms to input data

        Pipelines pass data between block objects and validate the integrity
        of a data processing pipeline. it is intended to be a quick, flexible, and
        modular approach to creating a processing graph. It also contains helper
        functions for documentation and saving these pipelines for use by other
        researchers/users.

        Args:
            name(str): name for this pipeline that will be enumerated to be unique,
                defaults to the name of the subclass<index>
            blocks(list): list of blocks to instantiate this pipeline with, shortcut
                to the 'add' function. defaults to []
            verbose(bool): whether or not to enable printouts for this pipeline,
                defaults to True
            enable_text_graph(bool): whether or not to print out a graph of
                pipeline blocks and outputs

        Attributes:
            name(str): unique name for this pipeline
            blocks(list): list of block objects being used by this pipeline,
                in order of their processing sequence
            verbose(bool): verbose(bool): whether or not this pipeline with print
                out its status
            enable_text_graph(bool): whether or not to print out a graph of
                pipeline blocks and outputs
            printer(ip.Printer): printer object for this pipeline,
                registered with 'name'
    """
    EXTANT = {}
    def __init__(self,
                    blocks=[],
                    name=None,
                    verbose=True,
                    enable_text_graph=False):
        if name is None:
            name = self.__class__.__name__

        # keeping track of names internally in a class variable
        if name in self.EXTANT:
            self.EXTANT[name] += 1
        else:
            self.EXTANT[name] = 1
        name = name + ':{}'.format( self.EXTANT[name] )

        self.name = name
        self.verbose = verbose
        self.enable_text_graph = enable_text_graph
        self.printer = get_printer(self.name)
        self.names_to_extract = []
        self.intermediate_data = {}

        # set log level to infinity if non-verbose is desired
        if not self.verbose:
            self.printer.set_log_level(float('inf'))

        # checking to make sure blocks is a list
        if not isinstance(blocks, (list,tuple)):
            error_msg = "'blocks' must be a list"
            self.printer.error(error_msg)
            raise TypeError(error_msg)

        self.blocks = []
        for b in blocks:
            self.add(b)

    def add(self, block):
        """adds processing block to the pipeline processing chain

        Args:
            block (ip.BaseBlock): block object to add to this pipeline

        Returns:
            None

        Raise:
            TypeError: if 'block' is not a subclass of BaseBlock
        """
        # checking to make sure block is a real block
        if not isinstance(block, BaseBlock):
            error_msg = "'block' must be a subclass of ip.BaseBlock"
            self.printer.error(error_msg)
            raise TypeError(error_msg)

        # appends to instance block list
        self.printer.info("adding block {} to the pipeline".format(block.name))
        self.blocks.append(block)

    def insert(self, index, block):
        """inserts processing block into the pipeline processing chain

        Args:
            index (int): index at which block object is to be inserted

            block (ip.BaseBlock): block object to add to this pipeline

        Returns:
            None

        Raise:
            TypeError: if 'block' is not a subclass of BaseBlock, or 'index' is not instance of int
        """
        # checking to make sure block is a real block
        if (not isinstance(block, BaseBlock)):
            error_msg = "'block' must be a subclass of ip.BaseBlock"
            self.printer.error(error_msg)
            raise TypeError(error_msg)

        # checking to make sure index is integer
        if (isinstance(index, int)):
            error_msg = "'index' must be int"
            self.printer.error(error_msg)
            raise TypeError(error_msg)

        self.printer.info("inserting block {0} into pipeline at index {1}".format(block.name, index))

        self.blocks.insert(index, block)

    def remove(self, block_name):
        """removes processing block from the pipeline processing chain

        Args:
            block_name (str): unique string name of block object to remove

        Returns:
            None

        Raise:
            TypeError: if 'block_name' is not an instance of str

            ValueError: if 'block_name' is not member of list self.names
        """
        # checking to make sure block_name is string
        if (not isinstance(block_name, str)):
            error_msg = "'block_name' must be a string"
            self.printer.error(error_msg)
            raise TypeError(error_msg)

        # checking to make sure block_name is member of self.names
        if (block_name in self.names):
            error_msg = "'block_name' must be member of list self.names"
            self.printer.error(error_msg)
            raise ValueError(error_msg)

        self.printer.info("removing block {} from the pipeline".format(block_name))

        # get index from block name and delete corresponding item from self.blocks
        i = self.names.index(block_name)
        self.__delitem__(i)

    def copy(self):
        """provides deepcopy of pipeline processing chain

        Args:
            None

        Returns:
            deepcopy: a deepcopy of the entire pipeline instance, 'self'

        Raise:
            None
        """
        # returns a deepcopy of entire pipeline (this will be useful for cache?)
        return copy.deepcopy(self)

    def clear(self):
        """clears all processing blocks from the pipeline processing chain

        Args:
            None

        Returns:
            None

        Raise:
            None
        """
        # cycle through blocks and handle individual deletion, reset empty list
        for i in range(len(self.blocks)):
            self.__delitem__(i)

        self.blocks = []

    def validate(self,data):
        """validates the integrity of the pipeline

        verifies all input-output shapes are compatible with each other

        Developer Note:
            this function could use a full refactor, especially with regards
            to printouts when an error is raised - Jeff

            Type comparison between Blocks is complicated and I suspect more
            bugs are still yet to be discovered.

        Raises:
            CrackedPipeline: if there is a input-output shape
                incompatability
            TypeError: if 'data' isn't a list or tuple
            RuntimeError: if more than one block in the pipeline has the same
                name, or not all objects in the block list are BaseBlock
                subclasses
        """

        # assert that every element in the blocks list is a BaseBlock subclass
        if not all(isinstance(b,BaseBlock) for b in self.blocks):
            error_msg = \
               "all elements of the pipeline must be subclasses of ip.BaseBlock"
            self.printer.error(error_msg)
            raise RuntimeError(error_msg)


        # make sure data is a list
        if not isinstance(data,list):
            raise TypeError("'data' must be list")

        # make sure every block has a unique name
        if len(set(self.names)) != len(self.names):
            error_msg = "every block in the pipeline must have a different name"
            self.printer.error(error_msg)
            raise RuntimeError(error_msg)

        # JM: get shape of every datum
        # get unique shapes so we don't have to test every single shape
        data_types = set([get_type(datum) for datum in data])

        all_type_chains = []
        for data_type in data_types:
            type_chain = collections.OrderedDict(pipeline_input=data_type)
            input_type = data_type

            for block in self.blocks:
                try:
                    output_type = block.io_map.output_given_input(input_type)
                    broken_pair = False
                    type_chain[str(block)] = output_type
                    input_type = output_type

                except IncompatibleTypes as e:
                    msg = []
                    for b,t in zip(list(type_chain.keys())[:-1],list(type_chain.values())[:-1]):
                        msg.append(b)
                        buf = ' ' * (len(msg[-1]) // 2)
                        msg.append("{}|".format(buf))
                        msg.append("{}| {}".format(buf,t))
                        msg.append("{}|".format(buf))

                    msg.append(list(type_chain.keys())[-1])
                    buf = ' ' * (len(msg[-1]) // 2)
                    msg.append("{}|".format(buf))
                    msg.append("{}X {}".format(buf,input_type))
                    msg.append("{}|".format(buf))
                    msg.append(str(block))
                    msg = '\n'.join(msg)
                    print(msg)
                    broken_pair = True


                if broken_pair:
                    error_msg = "{} - acceptable types are {}".format(block.name,
                            list(block.io_map.inputs))
                    self.printer.error(error_msg)
                    raise CrackedPipeline("Incompatible types passed between blocks")

            type_chain['pipeline_output'] = ''
            all_type_chains.append(type_chain)

        if self.enable_text_graph:
            self._text_graph(all_type_chains)

    def _step(self):
        """

        """
        block = self.blocks[self.step_index]
        self.step_data,self.step_labels = self._run_block(block,
                                                            self.step_data,
                                                            self.step_labels)

        self.step_index += 1

        if block.name in self.names_to_extract:
            self.intermediate_data[block.name] = self.step_data

        return self.step_data,self.step_labels

    def _run_block(self,block,data,labels=None):
        t = Timer()

        # processing data using the block
        processed,labels = block._pipeline_process(data,labels)

        # printing out process time to the terminal
        b_time = t.lap() # processing time for this block
        datum_time_ms = round(1000 * b_time / len(data), 3)
        debug_msg = "{}: processed {}datums in {} seconds".format(block.name,
                                                                    len(data),
                                                                    b_time)
        datum_msg = " (approx {}ms per datum)".format(datum_time_ms)
        self.printer.debug(debug_msg, datum_msg)
        return processed,labels

    def _before_process(self,data,labels=None):
        # check to make sure all blocks have been trained if required
        if not self.trained:
            for b in self.blocks:
                if not b.trained:
                    err_msg = "requires training, but hasn't yet been trained"
                    self.printer.error("{}: ".format(b.name), err_msg)

            raise RuntimeError("you must run Pipeline.train before processing")

        # validate pipeline integrity
        self.validate(data)

        # set initial conditions for the _step function
        self.step_index = 0
        self.step_data = data
        self.step_labels = labels

    def _process(self,data):
        # step through each block
        for i in range( len(self.blocks) ):
            self._step()

    def _after_process(self):
        # remove step data and labels memory footprint
        self.step_data = None
        self.step_labels = None

    def process(self,data):
        self._before_process(data,None)
        self._process(data)
        processed = self.step_data
        self._after_process()
        return processed



    def _before_train(self,data,labels=None):
        # validate pipeline integrity
        self.validate(data)

        # set initial conditions for the _step function
        self.step_index = 0
        self.step_data = data
        self.step_labels = labels

    def _train(self,data,labels=None):
        # TODO Add a check to see throw an error if self.requires_labels == True
        # and no labels are passed into this function
        t = Timer()
        for b in self.blocks:
            self.printer.debug("training {}...".format(b.name))
            b._pipeline_train(self.step_data,self.step_labels)
            self._step() #step the block processing forward

            self.printer.info("{}: trained in {} sec".format(b.name,t.lap()))

        self.printer.info("Pipeline trained in {}seconds".format(t.time()))

    def _after_train(self):
        # remove step data and labels memory footprint
        self.step_data = None
        self.step_labels = None

    def train(self,data,labels=None):
        self._before_train(data,labels)
        self._train(data,labels)

        processed,labels = self.step_data,self.step_labels
        self._after_train()
        return processed,labels


    def set_intermediate_data(self,names_to_extract):
        self.names_to_extract = names_to_extract
        self.intermediate_data = {}

    def get_intermediate_data(self):
        """retrieves the intermediate block data specified in
        set_intermediate_data

        Args:
            None

        Returns:
            intermediate_data(dict): dictionary of intermediate block data,
                key is block name,
        """
        return self.intermediate_data

    def graph(self):
        """TODO: Placeholder function for @Ryan to create"""
        pass

    def save(self, filename=None):
        """
        pickles and saves the entire pipeline as a pickled object, so it can
        be used by others or at another time

        Args:
            filename (string): filename to save pipeline to, defaults to
                pipeline.name + '.pck'
        """

        # prepping each block for serialization
        for b in self.blocks:
            b.prep_for_serialization()

        if filename is None:
            filename = self.name + '.pck'

        self.printer.info("saving {} to {}".format(self,filename))
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

        return filename

    def _text_graph(self,type_chains):
        for chain in type_chains:
            print("type-chain1:")
            buf = ' ' * 6
            for b,output in chain.items():
                print('  ', b )
                if b == 'pipeline_output':
                    break
                print('  ',buf,'|')
                print('  ',buf,'|',',  '.join(str(o) for o in output))
                print('  ',buf,'|')

    def debug(self):
        """enables debug mode which turns on all printouts for this pipeline
        to aide in debugging
        """
        set_global_printout_level('debug')
        self.printer.set_log_level('debug')
        self.verbose = True
        self.enable_text_graph = True
        self.printer.warning("debug mode enabled!")
        return self

    def join(self,pipeline):
        """adds the blocks from the pipeline passed in to this pipeline
        """
        for b in pipeline.blocks:
            self.add(b)

    def rename(self,name):
        assert isinstance(name,str),"name must be a string"
        self.name = name
        self.printer = get_printer(self.name)
        return self

    @property
    def names(self):
        """returns the names of all blocks"""
        return [b.name for b in self.blocks]

    @property
    def trained(self):
        """returns whether or not this pipeline has been trained"""
        return all(b.trained for b in self.blocks)

    @property
    def requires_labels(self):
        """returns whether or not this pipeline requires labels"""
        return any(b.requires_labels for b in self.blocks)

    def __str__(self):
        out = "{}: '{}'  ".format(self.__class__.__name__,self.name) \
                + '(' + "->".join(b.name for b in self.blocks) + ')'
        return out

    def __repr__(self):
        return str(self)

    def __delitem__(self, i):
        # Method for cleaning up file io and multiprocessing with caching revamp
        self.blocks.pop(i)

    def __getitem__(self,index):
        return self.blocks[index]

    def __setitem__(self,index,block):
        if not isinstance(block, BaseBlock):
            error_msg = "'block' must be a subclass of ip.BaseBlock"
            self.printer.error(error_msg)
            raise TypeError(error_msg)

        self.printer.info("{} replaced with {}".format(self.blocks[index],block.name))
        self.blocks[index] = block

    def __iter__(self):
        """generator to return all blocks in the pipeline"""
        return (b for b in self.blocks)
