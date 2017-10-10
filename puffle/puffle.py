__all__ = ['run_tests']

import subprocess
import os
import time
import json


def run_tests(truffle_dir, test_dir, testrpc_command, test_marker, *,
         clear_builds=False, build_dir=None, tests_to_run=None, truffle_network=None):
    os.chdir(truffle_dir)

    if clear_builds:
        clear_artifacts(build_dir)
        compilation_task = subprocess.Popen(['truffle', 'compile', 'all'])
        compilation_task.wait()

    tests_to_run = gather_tests(test_dir, tests_to_run)

    for test in tests_to_run:
        subps = []
        if not truffle_network:
            truffle_network = "development"

        try:
            testrpc_task = subprocess.Popen(testrpc_command, stdout=subprocess.PIPE)
            subps.append(testrpc_task)
            time.sleep(0.5)

            tests_task = subprocess.Popen(['truffle',
                                      'test',
                                      '--network',
                                      truffle_network,
                                      test],
                                     stdout=subprocess.PIPE)
            subps.append(tests_task)
            tests_task.wait()

            try:
                print(tests_task.communicate()[0].decode('utf-8').split(test_marker)[1].strip())
            except IndexError:
                for yoke in tests_task.communicate():
                    print(yoke.decode('utf-8'))
            for subp in subps:
                subp.terminate()
        except Exception as e:
            for subp in subps:
                subp.terminate()
            raise e   


def clear_artifacts(build_dir):
    for artifact in os.listdir(build_dir):
        os.remove(os.path.join(build_dir, artifact))


def gather_tests(test_dir, tests_to_run):
    run_me = []
    for dir_path, _, file_list in os.walk(test_dir):
        for test_file in file_list:
            if tests_to_run is not None:
                if test_file in tests_to_run:
                    run_me.append([dir_path, test_file])
            else:
                run_me.append([dir_path, test_file])
    run_me = [os.path.join(*test_loc) for test_loc in run_me]
    return run_me

