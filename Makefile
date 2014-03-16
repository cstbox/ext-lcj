# CSTBox framework
#
# Makefile for building the Debian distribution package containing the
# LCJ products support extension.
#
# author = Eric PASCUAL - CSTB (eric.pascual@cstb.fr)

# name of the CSTBox module
MODULE_NAME=ext-lcj

include $(CSTBOX_DEVEL_HOME)/lib/makefile-dist.mk

copy_files: \
    check_metadata_files \
    copy_python_files 
