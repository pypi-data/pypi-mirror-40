#author: Christoph Suerig
#date: 14.08.2018
#This is the main file of downward-dlr
#it is adding the argument "--build" to argv

import sys
import os


def already_contains_argument():
    return '--build=release64' in sys.argv or '--build=release32' in sys.argv


def release64_exists():
    cur_dir = os.path.dirname(__file__)
    build_dir = os.path.join(cur_dir,'builds','release64')
    return os.path.isdir(build_dir)


def dwdlr_main():
    from driver.main import main
    if (not already_contains_argument()) and release64_exists():
        sys.argv.insert(1,'--build=release64')
    main()


