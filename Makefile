# Makefile for source rpm: anthy
# $Id$
NAME := anthy
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
