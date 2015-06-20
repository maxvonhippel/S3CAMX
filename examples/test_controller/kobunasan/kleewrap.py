#!/usr/bin/env python

import os
import struct
import sys
import logging
import glob

#import c_info as c
#import fileOps as fp
#import utils as U

#logger = logging.getLogger(__name__)

version_no = 3

FILE_UNDER_TEST = 'controller_main'
CONTROLLER = 'demo_controller'
FINAL_OBJECT = 'C'

# TODO: platform dependant script
RUN_KLEE = './run_klee.sh'
# Extension for klee test files generated by klee and read by ktest-tool
KLEE_TEST_EXT = 'ktest'
KLEE_LAST = './klee-last'

LLVM_COMPILE = 'llvm-gcc '
COMPILE_OPTIONS = '--emit-llvm -c -g {}.c'
LLVM_LINK = 'llvm-ld '
LINK_OPTIONS = '-r {0}.o {1}.o -o {2}.o'
KLEE_RUN = 'klee '
KLEE_OPTIONS = '-smtlib-human-readable --write-pcs --use-query-log=all:pc {}.o'

MAIN_FUNCTION_STRING =\
'''
#include "controller.h"
int main() {{
    INPUT_VAL iv;
    RETURN_VAL rv;

    int state_arr_[NUM_STATES];
    int output_arr[NUM_OUTPUTS];

    int state_arr[NUM_STATES] = {{ {0} }};
    int x_arr[NUM_X];

    klee_make_symbolic(state_arr, sizeof(state_arr), "state_arr");
    klee_make_symbolic(x_arr, sizeof(x_arr), "x_arr");

    /*
    klee_make_symbolic(&s[0], sizeof(int), "s0");
    klee_make_symbolic(&x[0], sizeof(int), "x0");
    klee_make_symbolic(&s[1], sizeof(int), "s1");
    klee_make_symbolic(&x[1], sizeof(int), "x1");
    */
    /*
    s[0] = klee_int("s0");
    s[1] = klee_int("s1");
    x[0] = klee_int("x0");
    x[1] = klee_int("x1");
    */

    // klee_assume((x[0] >= 0)&(s[0] >= 0)&(x[0] <= 10)&(s[0] <= 10));
    // klee_assume((x[1] >= 0)&(s[1] >= 0)&(x[1] <= 10)&(s[1] <= 10));
    {1}

    iv.state_arr = state_arr;
    iv.x_arr = x_arr;

    rv.state_arr = state_arr_;
    rv.output_arr = output_arr;

    // ignore return value.
    controller(&iv, &rv);

    return 0;
}}
'''

KLEE_ASSUME = 'klee_assume({});\n'


# Input: list
# Returns a string representation of the list without brackets
# e.g. l = [1, 2, 3]
# '1, 2, 3' = remove_brackets_from_list(l)
def remove_brackets_from_list(l):
    return ', '.join(str(i) for i in l)
    # lambda l: ', '.join(str(i) for i in str(self.state_array))

# TODO: Should not create more than one object per session!
class KleeWrap(object):
    var_type = None

    def __init__(self, var_type_dict):
        KleeWrap.var_type = var_type_dict

    # Writes the main file: FILE_UNDER_TEST
    # Usinf the string wrapper: MAIN_FUNCTION_STRING
    @staticmethod
    def write_file(c_state_array, constraints_on_x_str_list):
        # generate assumes
        assume_str = ''
        for cons_str in constraints_on_x_str_list:
            assume_str += KLEE_ASSUME.format(cons_str)
        logger.debug('klee constraints'.format(assume_str))
        data = MAIN_FUNCTION_STRING.format(
            remove_brackets_from_list(c_state_array),
            assume_str)
        fp.write_data(FILE_UNDER_TEST+'.c', data)

    # TODO: Remove compilation in the loop!!
    # Runs klee using the script RUN_KLEE
    @staticmethod
    def analyze(c_state_array, constraints_on_x_str_list):
        KleeWrap.write_file(c_state_array, constraints_on_x_str_list)
        # TODO: Is this platform dependant??
        # TODO: Does not work, why?
        # print call([LLVM_COMPILE, COMPILE_OPTIONS.format(FILE_UNDER_TEST)], shell=True)
        # TODO: Does not work if shell = False, why?

        cmd = [LLVM_COMPILE + COMPILE_OPTIONS.format(FILE_UNDER_TEST)]
        logger.debug('exec command: {}'.format(cmd))
        U.strict_call(cmd, shell=True)

        cmd = [LLVM_COMPILE + COMPILE_OPTIONS.format(CONTROLLER)]
        logger.debug('exec command: {}'.format(cmd))
        U.strict_call(cmd, shell=True)

        cmd = [LLVM_LINK + LINK_OPTIONS.format(CONTROLLER, FILE_UNDER_TEST, FINAL_OBJECT)]
        logger.debug('exec command: {}'.format(cmd))
        U.strict_call(cmd, shell=True)

        cmd = [KLEE_RUN + KLEE_OPTIONS.format(FINAL_OBJECT)]
        logger.debug('exec command: {}'.format(cmd))
        U.strict_call(cmd, shell=True)

        test_cases = KleeWrap.get_output()
        logger.debug('klee returned followinG test cases\n{}'.format(test_cases))
        return test_cases

    # Reads klee's output using a modified version of ktest-tool
    # Expects a var_type_dict: var_name -> type
    # Returns a var_val_dict: var_name -> value
    '''
    types:
        int
        int_arr
        str
    '''
    @staticmethod
    def get_output():
        test_case_list = []
        ktest_filenames = glob.glob('{}/*.{}'.format(KLEE_LAST, KLEE_TEST_EXT))
        for filename in ktest_filenames:
            b = KTest.fromfile(filename)
            logger.debug('ktest file : {}'.format(filename))
            logger.debug('args       : {}'.format(b.args))
            logger.debug('num objects: {}'.format(len(b.objects)))
            var_val = {}
            # Not clear what i stands for
            for i, (name, data) in enumerate(b.objects):
                # Always trim zeros
                STR = data
                Type = KleeWrap.var_type[name]
                if Type == 'int':
                    var_val[name] = struct.unpack('i', STR)[0]
                elif Type == 'int_arr':
                    n = c.sizeof_int()
                    var_val[name] = [struct.unpack('i', STR[j*n:(j+1)*n])[0]
                                     for j in range(len(STR)/n)]
                elif Type == 'str':
                    var_val[name] = '{:r}'.format(STR)
                # Unkown data type!
                else:
                    raise NotImplementedError
                    var_val[name] = STR
            test_case_list.append(var_val)
        return test_case_list


# lambda l: str(l).replace('[','{').replace(']','}')
# lambda l: ', '.join(str(i) for i in l)


class KTestError(Exception):
    pass


class KTest:
    @staticmethod
    def trimZeros(STR):
        for i in range(len(STR))[::-1]:
            if STR[i] != '\x00':
                return STR[:i+1]
        return ''
    @staticmethod
    def fromfile(path):
        if not os.path.exists(path):
            print("ERROR: file %s not found" % (path))
            sys.exit(1)

        f = open(path,'rb')
        hdr = f.read(5)
        if len(hdr)!=5 or (hdr!=b'KTEST' and hdr != b"BOUT\n"):
            raise KTestError('unrecognized file')
        version, = struct.unpack('>i', f.read(4))
        if version > version_no:
            raise KTestError('unrecognized version')
        numArgs, = struct.unpack('>i', f.read(4))
        args = []
        for i in range(numArgs):
            size, = struct.unpack('>i', f.read(4))
            args.append(str(f.read(size).decode(encoding='ascii')))

        if version >= 2:
            symArgvs, = struct.unpack('>i', f.read(4))
            symArgvLen, = struct.unpack('>i', f.read(4))
        else:
            symArgvs = 0
            symArgvLen = 0

        numObjects, = struct.unpack('>i', f.read(4))
        objects = []
        for i in range(numObjects):
            size, = struct.unpack('>i', f.read(4))
            name = f.read(size)
            size, = struct.unpack('>i', f.read(4))
            bytes = f.read(size)
            objects.append((name, bytes))

        # Create an instance
        b = KTest(version, args, symArgvs, symArgvLen, objects)
        # Augment with extra filename field
        b.filename = path
        return b

    def __init__(self, version, args, symArgvs, symArgvLen, objects):
        self.version = version
        self.symArgvs = symArgvs
        self.symArgvLen = symArgvLen
        self.args = args
        self.objects = objects

        # add a field that represents the name of the program used to
        # generate this .ktest file:
        program_full_path = self.args[0]
        program_name = os.path.basename(program_full_path)
        # sometimes program names end in .bc, so strip them
        if program_name.endswith('.bc'):
            program_name = program_name[:-3]
        self.programName = program_name


# Main from ktest-tool, can independatly read klee output
def main(args):
    from optparse import OptionParser
    op = OptionParser("usage: %prog [options] files")
    op.add_option('','--trim-zeros', dest='trimZeros', action='store_true', 
                  default=False,
                  help='trim trailing zeros')
    op.add_option('','--write-ints', dest='writeInts', action='store_true',
                  default=False,
                  help='convert 4-byte sequences to integers')
    op.add_option('','--int-arr', dest='intArr', action='store_true',
                  default=False,
                  help='display int arrays as arrays: assumes everything as int array!')
    
    opts,args = op.parse_args()
    if not args:
        op.error("incorrect number of arguments")

    for file in args:
        b = KTest.fromfile(file)
        pos = 0
        print('ktest file : %r' % file)
        print('args       : %r' % b.args)
        print('num objects: %r' % len(b.objects))
        for i,(name,data) in enumerate(b.objects):
            if opts.trimZeros:
                str = KTest.trimZeros(data)
            else:
                str = data

            print('object %4d: name: %r' % (i, name))
            print('object %4d: size: %r' % (i, len(data)))
            if opts.writeInts and len(data) == 4: 
                print('object %4d: data: %r' % (i, struct.unpack('i',str)[0]))
            elif opts.intArr:
                # n  = sizeof(int) = 4
                n = 4
                val = [struct.unpack('i', data[j*n:(j+1)*n])[0]
                                 for j in range(len(data)/n)]
                print('object {:4d} data: {}'.format(i, val))
            else:
                print('object %4d: data: %r' % (i, str))
        if file != args[-1]:
            print()

if __name__ == '__main__':
    main(sys.argv)