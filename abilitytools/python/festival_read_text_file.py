﻿#!/usr/bin/env python
# -*- coding: UTF-8-*-
'''
    Reads a text file using festival and a media player.
    
    The festival engine is a software speech synthesizer.
    
    Install festival using a package manager to install a festivox or festival voice.
    The package manager should automatically select the festival package and the
    required support files.
    
    If you are using this extension to create still frame videos you need ffmpeg. Webm is the  
    recommended video format. If you are creating a long video, be patient. It can take a long
    time for the external program to render the video.
    
    Read Text Extension 0.7.18 or newer dialog:
    Read with an external program: 
    /usr/bin/python
    Normal Command line options: 
    "(FESTIVAL_READ_TEXT_PY)" "(TMP)"
    Command line option to save as a .wav file: 
    "(FESTIVAL_READ_TEXT_PY)"  --output "(HOME)(NOW).wav" "(TMP)"
    
    Copyright (c) 2011 James Holgate
    '''
import getopt,sys,codecs,os,platform,readtexttools

def usage():
    sA = ' ' + os.path.split(sys.argv[0])[1]
    print ("")
    print ("Reads a text file using festival and a media player.")
    print ("")
    print ("Usage")
    print (sA+' "input.txt"')
    print (sA+' --visible "false" "input.txt"')
    print (sA+' --output "output.wav" "input.txt"')
    print (sA+' --output "output.[m4a|mp2|mp3|ogg]" "input.txt"')
    print (sA+' --output "output.[avi|webm]" --image "input.[png|jpg]" "input.txt"')
    print (sA+' --audible "false" --output "output.wav" "input.txt"')
    print ("")

def festivalread(sFILEPATH,sVISIBLE,sAUDIBLE,sTMP0,sIMG1,sC):
    '''
        sTXTFILE - Text File to speak
        sVISIBLE- Use a graphical media player,or False for a command line media player
        sTMP0 - Name of desired output file
        sAUDIBLE - If false, then don't play the sound file
        sIMG1 - a .png or .jpg file is required if we are making a movie, otherwise it is ignored.
        '''
    # Determine the output file name
    sOUT1=readtexttools.fsGetSoundFileName(sTMP0,sIMG1,"OUT")
    # Determine the temporary file name
    sTMP1=readtexttools.fsGetSoundFileName(sTMP0,sIMG1,"TEMP")
    
    # Some apps throw an error if we try to overwrite a file, so delete old versions
    if os.path.isfile(sTMP1):
        os.remove(sTMP1)
    if os.path.isfile(sOUT1):
        os.remove(sOUT1)
    try:
        if "windows" in platform.system().lower():
            if readtexttools.getWinFullPath("festival/text2wave"):
                sCommand=readtexttools.getWinFullPath("festival/festival.exe")+' --script "'+readtexttools.getWinFullPath("festival/text2wave")+'"'
                s1=sCommand+' "'+sFILEPATH+'" -o "'+sTMP1+'"' 
                readtexttools.myossystem(s1)
                readtexttools.ProcessWaveMedia(sC,sTMP1,sIMG1,sOUT1,sAUDIBLE,sVISIBLE)
            else:
                # With Windows, this script only supports reading text aloud.
                sCommand=readtexttools.getWinFullPath("festival/festival.exe")
                s1=sCommand+ '--tts  "' + sFILEPATH+'"'
            readtexttools.myossystem(s1)
        else:
            sCommand='text2wave'
            # text2wave is an executable festival script
            s1=sCommand+' "'+sFILEPATH+'" -o "'+sTMP1+'"' 
            readtexttools.myossystem(s1)
            readtexttools.ProcessWaveMedia(sC,sTMP1,sIMG1,sOUT1,sAUDIBLE,sVISIBLE)
    except IOError,err:
        print ('I was unable to read!')
        print (str(err))
        usage()
        sys.exit(2)

def main():
    sWAVE=""
    sVISIBLE=""
    sAUDIBLE=""
    sTXTFILE=""
    sRATE="100%"
    sPITCH="100%"
    sIMG1=""
    try:
        opts,args=getopt.getopt(sys.argv[1:],"hovarpi",["help","output=","visible=","audible=","rate=","pitch=","image="])
    except getopt.GetoptError,err:
        # print help information and exit
        print (str(err)) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    for o,a in opts:
        if o in ("-h","--help"):
            usage()
            sys.exit(0)
        elif o in ("-o","--output"):
            sWAVE=a
        elif o in ("-v","--visible"):
            sVISIBLE=a
        elif o in ("-a","--audible"):
            sAUDIBLE=a
        elif o in ("-r","--rate"):
            sRATE=a
        elif o in ("-p","--pitch"):
            sPITCH=a
        elif o in ("-i","--image"):
            sIMG1=a
        else:
            assert False,"unhandled option"
    try:
        sFILEPATH=sys.argv[-1]
        oFILE=codecs.open(sFILEPATH,mode='r',encoding=sys.getfilesystemencoding())
    
    except IOError:
        print ('I was unable to open the file you specified!')
        usage()
    else:
        sTXT=oFILE.read().replace(u" '",u" ‘").replace(u"'",u"’").replace(u' "',u" “").replace(u'"',u'”')
        oFILE.close()
        sB=sTXT.encode('ascii','replace')
        if len(sB) > 29: # limit of title length.
            sC=sTXT[:26].encode( "utf-8" )+'...'
        else:
            sC=sTXT.encode( "utf-8" )
        festivalread(sFILEPATH,sVISIBLE,sAUDIBLE,sWAVE,sIMG1,sC)
        sys.exit(0)

if __name__=="__main__":
    main()


