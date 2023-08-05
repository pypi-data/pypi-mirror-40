import os
import sys
sys.tracebacklimit=0
import platform
import subprocess

def install():
    #name=raw_input('Enter your name : ')
    #print ("Hi %s, Welcome to Canvas Technology!" % name);
    jpath = 'notSet'
    while (jpath == 'notSet'):
        jpath=javapath()
    print jpath
    server_type = ''
    while (server_type != 'tomcat' and server_type != 'jboss'):
        server_type=server()
    print 'END'
    return ('You have successfully Install Canvas!!! Ready to Rock and Roll')

def remove():
     print "Remove is yet to Implement"
     return ('Thanks for Choosing Canvas')

def server():
    server_value=raw_input('Enter Server Preference 1.Tomcat 2.Jboss (input 1 or 2): ')
    val = 0
    try:
        val = int(server_value)
    except ValueError:
        print("input is not valid, Try again!!!")
        return ''
    if(val ==1 or val==2):
        if(val ==1):
            print 'You have choose Tomcat as your Application Server'
            return 'tomcat'
        if(val ==2):
            print 'You have choose JBOSS as your Application Server'
            return 'jboss'
    else:
        print 'Choose between 1 and 2'
        print 'Please try again!!!'
        return ''
def javapath():
    platform_check = platform.system()
    print platform_check
    if(platform_check == "Linux"):
        javapath=raw_input('Enter Java path(Supports java 1.8+ ) : ')
        #java_string = javapath + " -version 2>&1 | awk -F[\\\"_] 'NR==1{print $2}'"
        java_string = javapath + " -version 2>&1 | awk -F[\\\"\.] -v OFS=. \'NR==1{print $2,$3}\'"
        #print java_string
        java_version = subprocess.check_output(java_string, shell=True)
        print java_version.strip()
        if(java_version.strip() == '.'):
            print "Please Enter the valid Java Path"
            return 'notSet'
        if (float(java_version) >= 1.8):
            print 'Java Version Compertable with the bench mark. Lets Proceed Further!!!'
        else:
            print 'Java version not supported!!!'
            exit()
        #print java_version
        return javapath


#install()
