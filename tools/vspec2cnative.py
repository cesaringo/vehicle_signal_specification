#!/usr/bin/python

#
# (C) 2018 Volvo Cars
# (C) 2016 Jaguar Land Rover
#
# All files and artifacts in this repository are licensed under the
# provisions of the license provided by the LICENSE file in this repository.
#
#
# Convert vspec file to a platform native format.
#

import sys
import os
import vspec
import json
import getopt
import ctypes

def usage():
    print(("Usage:", sys.argv[0], "[-I include_dir] ... [-i prefix:id_file] vspec_file franca_file"))
    print ("  -I include_dir       Add include directory to search for included vspec")
    print ("                       files. Can be used multiple timees.")
    print ("\n")
    print ("  -i prefix:uuid_file  File to use for storing generated UUIDs for signals with")
    print ("                       a given path prefix. Can be used multiple times to store")
    print ("                       UUIDs for signal sub-trees in different files.")
    print ("\n")
    print (" vspec_file            The vehicle specification file to parse.")
    print (" franca_file           The file to output the Franca IDL spec to.")
    sys.exit(255)

import os.path
dllName = "c_native/cnativenodelib.so"
dllAbsPath = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + dllName
_cnative = ctypes.CDLL(dllAbsPath)

#void createNativeCnode(char* fname, char* name, char* type, char* uuid, char* descr, int children, char* datatype, char* min, char* max, char* unit, char* enums, char* function);
_cnative.createNativeCnode.argtypes = (ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_int,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p)

#void createNativeCnodeRbranch(char* fname, char* name, char* type, char* uuid, char* descr, int children, char* childType, int numOfProperties, char** propNames, char** propDescrs, char** propTypes, char** propFormats, char** propUnits, char** propValues);
_cnative.createNativeCnodeRbranch.argtypes = (ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_int,ctypes.c_char_p,ctypes.c_int,ctypes.POINTER(ctypes.c_char_p),ctypes.POINTER(ctypes.c_char_p),ctypes.POINTER(ctypes.c_char_p),ctypes.POINTER(ctypes.c_char_p),ctypes.POINTER(ctypes.c_char_p),ctypes.POINTER(ctypes.c_char_p))


#void createNativeCnodeElement(char* fname, char* name, char* type, char* uuid, char* descr, int children, int numOfElems, char** memberName, char** memberValue);
_cnative.createNativeCnodeElement.argtypes = (ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_int,ctypes.c_int,ctypes.POINTER(ctypes.c_char_p),ctypes.POINTER(ctypes.c_char_p))


def createNativeCnode(fname, nodename, nodetype, uuid, description, children, nodedatatype, nodemin, nodemax, unit, enums, function):
    global _cnative
    _cnative.createNativeCnode(fname, nodename, nodetype, uuid, description, children, nodedatatype, nodemin, nodemax, unit, enums, function)


def createNativeCnodeRbranch(fname, nodename, nodetype, uuid, nodedescr, children, childType, numOfProperties, propNames, propDescrs, propTypes, propFormats, propUnits, propValues):
    global _cnative
    numofPropNames = len(propNames)
    propNamesArrayType = ctypes.c_char_p*numofPropNames
    propNamesArray = propNamesArrayType()
    for i, param in enumerate(propNames):
        propNamesArray[i] = param

    numofPropDescrs = len(propDescrs)
    propDescrsArrayType = ctypes.c_char_p*numofPropDescrs
    propDescrsArray = propDescrsArrayType()
    for i, param in enumerate(propDescrs):
        propDescrsArray[i] = param

    numofPropTypes = len(propTypes)
    propTypesArrayType = ctypes.c_char_p*numofPropTypes
    propTypesArray = propTypesArrayType()
    for i, param in enumerate(propTypes):
        propTypesArray[i] = param

    numofPropFormats = len(propFormats)
    propFormatsArrayType = ctypes.c_char_p*numofPropFormats
    propFormatsArray = propFormatsArrayType()
    for i, param in enumerate(propFormats):
        propFormatsArray[i] = param

    numofPropUnits = len(propUnits)
    propUnitsArrayType = ctypes.c_char_p*numofPropUnits
    propUnitsArray = propUnitsArrayType()
    for i, param in enumerate(propUnits):
        propUnitsArray[i] = param

    numofPropValues = len(propValues)
    propValuesArrayType = ctypes.c_char_p*numofPropValues
    propValuesArray = propValuesArrayType()
    for i, param in enumerate(propValues):
        propValuesArray[i] = param

    _cnative.createNativeCnodeRbranch(fname, nodename, nodetype, uuid, nodedescr, children, childType, numOfProperties, propNamesArray, propDescrsArray, propTypesArray, propFormatsArray, propUnitsArray, propValuesArray)


def createNativeCnodeElement(fname, name, nodetype, uuid, description, children, numOfElems, keys, values):
    global _cnative
    numofKeys = len(keys)
    keysArrayType = ctypes.c_char_p*numofKeys
    keysArray = keysArrayType()
    for i, param in enumerate(keys):
        keysArray[i] = param

    numofValues = len(values)
    valuesArrayType = ctypes.c_char_p*numofValues
    valuesArray = valuesArrayType()
    for i, param in enumerate(values):
        valuesArray[i] = param

    _cnative.createNativeCnodeElement(fname, name, nodetype, uuid, description, children, numOfElems, keysArray, valuesArray)


def enumString(enumList):
    enumStr = "/"
    for elem in enumList:
        enumStr += elem + "/"
    return enumStr

def create_node_legacy(key, val, b_nodename, b_nodetype, b_nodeuuid, b_nodedescription, children):
    nodedatatype = ""
    nodemin = ""
    nodemax = ""
    nodeunit = ""
    nodeenum = ""
    nodefunction = ""

    if "datatype" in val:
        nodedatatype = str(val["datatype"])

    if "min" in val:
        nodemin = str(val["min"])

    if "max" in val:
        nodemax = str(val["max"])

    if "unit" in val:
        nodeunit = val["unit"]

    if "enum" in val:
        nodeenum = enumString(val["enum"])

    if "function" in val:
        nodefunction = val["function"]

    b_nodedatatype = nodedatatype.encode('utf-8')
    b_nodemin = nodemin.encode('utf-8')
    b_nodemax = nodemax.encode('utf-8')
    b_nodeunit = nodeunit.encode('utf-8')
    b_nodeenum = nodeenum.encode('utf-8')
    b_nodefunction = nodefunction.encode('utf-8')

    b_fname = args[1].encode('utf-8')

    createNativeCnode(b_fname, b_nodename, b_nodetype, b_nodeuuid, b_nodedescription, children, b_nodedatatype, b_nodemin, b_nodemax, b_nodeunit, b_nodeenum, b_nodefunction)


def create_node_rbranch(key, val, b_nodename, b_nodetype, b_nodeuuid, b_nodedescription, children):
    childType = ""
    childProperties = 0
    propNames = {}
    propDescriptions = {}
    propTypes = {}
    propFormats = {}
    propUnits = {}
    propValues = {}

    if "child-type" in val:
        childType = val["child-type"]

    if "child-properties" in val:
        childProperties = val["child-properties"]

    if "prop-name" in val:
        propNames = val["prop-name"]

    if "prop-description" in val:
        propDescriptions = val["prop-description"]

    if "prop-type" in val:
        propTypes = val["prop-type"]

    if "prop-format" in val:
        propFormats = val["prop-format"]

    if "prop-unit" in val:
        propUnits = val["prop-unit"]

    if "prop-value" in val:
        propValues = val["prop-value"]


    b_childType = childType.encode('utf-8')

    b_names = []
    for elem in propNames:
        b_names.append(elem.encode('utf-8'))

    b_descrs = []
    for elem in propDescriptions:
        b_descrs.append(elem.encode('utf-8'))

    b_types = []
    for elem in propTypes:
        b_types.append(elem.encode('utf-8'))

    b_formats = []
    for elem in propFormats:
        b_formats.append(elem.encode('utf-8'))

    b_units = []
    for elem in propUnits:
        b_units.append(elem.encode('utf-8'))

    b_values = []
    for elem in propValues:
        b_values.append(elem.encode('utf-8'))

    b_fname = args[1].encode('utf-8')

    createNativeCnodeRbranch(b_fname, b_nodename, b_nodetype, b_nodeuuid, b_nodedescription, children, b_childType, childProperties, b_names, b_descrs, b_types, b_formats, b_units, b_values)


def create_node_element(nodekey, val, b_nodename, b_nodetype, b_nodeuuid, b_nodedescription, children):
    keys = []
    values = []

    del val["type"]
    del val["description"]

    numOfElems = len(val)

    for key, value in list(val.items()):
        keys.append(key)
        values.append(str(value))

    b_keys = []
    for elem in keys:
        b_keys.append(elem.encode('utf-8'))

    b_values = []
    for elem in values:
            b_values.append(elem.encode('utf-8'))

    b_fname = args[1].encode('utf-8')

    createNativeCnodeElement(b_fname, b_nodename, b_nodetype, b_nodeuuid, b_nodedescription, children, numOfElems, b_keys, b_values)


def create_node(key, val):
    nodename = key
    b_nodename = nodename.encode('utf-8')
    nodetype = val['type']
    b_nodetype = nodetype.encode('utf-8')
    nodeuuid = val['uuid']
    b_nodeuuid = nodeuuid.encode('utf-8')
    nodedescription = val['description']
    b_nodedescription = nodedescription.encode('utf-8')
    children = 0
    if "children" in val:
        children = len(list(val["children"].keys()))
    if (nodetype != "rbranch") and (nodetype != "element"):
        create_node_legacy(key, val, b_nodename, b_nodetype, b_nodeuuid, b_nodedescription, children)
    if (nodetype == "rbranch"):
        create_node_rbranch(key, val, b_nodename, b_nodetype, b_nodeuuid, b_nodedescription, children)
    if (nodetype == "element"):
        create_node_element(key, val, b_nodename, b_nodetype, b_nodeuuid, b_nodedescription, children)


def traverse_tree(tree):
    # Traverse all elemnts in tree.
    for key, val in tree.items():
        # Is this a branch?
        if "children" in val:
            # Yes. Recurse
            create_node(key, val)
            traverse_tree(val['children'])
            continue
        create_node(key, val)


if __name__ == "__main__":
    #
    # Check that we have the correct arguments
    #
    opts, args= getopt.getopt(sys.argv[1:], "I:i:v:")

    # Always search current directory for include_file
    vss_version = "unspecified version"
    include_dirs = ["."]
    for o, a in opts:
        if o == "-I":
            include_dirs.append(a)
        elif o == "-v":
            vss_version = a
        elif o == "-i":
            id_spec = a.split(":")
            if len(id_spec) != 2:
                print ("ERROR: -i needs a 'prefix:id_file' argument.")
                usage()

            [prefix, file_name] = id_spec
            vspec.db_mgr.create_signal_uuid_db(prefix, file_name)
        else:
            usage()

    if len(args) != 2:
        usage()

    try:
        tree = vspec.load(args[0], include_dirs)
    except vspec.VSpecError as e:
        print(("Error: {}".format(e)))
        exit(255)

    traverse_tree(tree)

