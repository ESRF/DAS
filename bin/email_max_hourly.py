#!/usr/bin/env python
#   
import os, sys, getopt, re
import time
from datetime import date, datetime, timedelta

def help():
    print "\nUsage:"
    print "email_max_hourly.py -p project -e emails_separated_by_,"
    print "\nReads message on stdin\n"
    print "Only one e-mail per hour and per project and per machine goes out"
    print "A specific e-mail goes out when too many e-mails would have been sent\n"

def createTimeStamp(stampFile):
    if os.path.exists(stampFile):
        try:
            os.remove(stampFile)
        except Exception, e:
            raise e
        # create a file with one line
        try:
            fd = os.open(stampFile, os.O_RDWR | os.O_CREAT)
            # Write one string
            os.write(fd, "Timestamp for program email_max_hourly.py")
            # Close opened file
            os.close(fd)
        except Exception, e:
            raise e
    else:
        # create it
        try:
            fd = os.open(stampFile, os.O_RDWR | os.O_CREAT)
            # Write one string
            os.write(fd, "Timestamp for program email_max_hourly.py")
            # Close opened file
            os.close(fd)
        except Exception, e:
            raise e

def removeTimeStamp(stampFile):
    if os.path.exists(stampFile):
        try:
            os.remove(stampFile)
        except Exception, e:
            raise e

# assemble arguments
try:
    opts, args = getopt.getopt(sys.argv[1:], "p:e:")
    for opt, val in opts:
        if opt == '-p':
            project = val
        if opt == '-e':
            email = val
except getopt.GetoptError:
    print >> sys.stderr, "\nSyntax error"
    help()
    sys.exit()

# check some syntax
if email == re.sub('@', '', email):
    print >> sys.stderr, "\ne-mail without @"
    help()
    sys.exit(-1)
if project != re.sub(r'\s', '', project):
    print >> sys.stderr, "project can not have spaces in it"
    help()
    sys.exit(-1)
if len(args) != 0:
    print >> sys.stderr, "\nsome extra entries without -p or -e"
    help()
    sys.exit(-1)

# time stamp for last sent e-mail
timeStampFile = "/tmp/." + project + "_email_time_stamp"
# panic stamp - sent one extra e-mail within one hour and then stop
panicStamp = "/tmp/." + project + "_email_panic_time_stamp"
# Now decide if we send project mail
if os.path.exists(timeStampFile):
    # already a time stamp.. Check if we should ignore it
    createTime = os.path.getctime(timeStampFile)
    # if more than one hour (36000s) just remove and ignore
    if (createTime > (time.time() - 3600)):
        # too soon, let us send e-mail number two if no panic stamp
        if not os.path.exists(panicStamp):
            # make a timestamp before sending panic mail
            createTimeStamp(panicStamp)
            try:
                os.execv('/bin/mailx', ['mailx', '-s', 'Last Error sent from project ' + project + ' for one hour : congestion ', email])
            except Exception, e:
                print "Exception in python" + str(e)
                sys.exit(-1)
        else:
            # quietly exit - Panic is declared - No more e-mails
            sys.exit(0)
    else:
        # all OK - Just remove all stamps
        removeTimeStamp(panicStamp)
        removeTimeStamp(timeStampFile)

# make a timestamp before sending
createTimeStamp(timeStampFile)
try:
    os.execv('/bin/mailx', ['mailx', '-s', 'Error sent from project ' + project, email])
except Exception, e:
    print "Exception in python" + str(e)
    sys.exit(-1)
