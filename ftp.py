# -*- encoding: utf8 -*-
import os
import sys
import ftplib
import time

_XFER_FILE = 'FILE'
_XFER_DIR = 'DIR'

class Xfer(object):
    '''
    @note: upload local file or dirs recursively to ftp server
    '''    
    def __init__(self):    
        self.ftp = None    

    def __del__(self):    
        pass    

    def setFtpParams(self, ip, uname, pwd, port = 21, timeout = 60):            
        self.ip = ip    
        self.uname = uname    
        self.pwd = pwd    
        self.port = port    
        self.timeout = timeout    

    def initEnv(self):    
        if self.ftp is None:    
            self.ftp = ftplib.FTP()    
            print '### connect ftp server: %s ...'%self.ip    
            self.ftp.connect(self.ip, self.port, self.timeout)    
            self.ftp.login(self.uname, self.pwd)     
            print self.ftp.getwelcome()    

    def clearEnv(self):    
        if self.ftp:    
            self.ftp.close()    
            print '### disconnect ftp server: %s!'%self.ip     
            self.ftp = None    

    def uploadDir(self, localdir='./', remotedir='./'):    
        if not os.path.isdir(localdir):      
            return    
        self.ftp.cwd(remotedir)     
        for file in os.listdir(localdir):    
            src = os.path.join(localdir, file)    
            if os.path.isfile(src):    
                self.uploadFile(src, file)    
            elif os.path.isdir(src):    
                try:      
                    self.ftp.mkd(file)      
                except:      
                    sys.stderr.write('the dir is exists %s'%file)    
                self.uploadDir(src, file)    
        self.ftp.cwd('...')

    def uploadFile(self, localpath, remotepath='/'):
        self.ftp.storbinary('STOR '+'/image/python/' + remotepath, open(localpath, 'rb'))

    def __filetype(self, src):
        index = src.rfind('\\')
        if index == -1:
            index = src.rfind('/')
        return src[index+1:]

    def upload(self, src):
        filename = self.__filetype(src)
        self.uploadFile(src, filename)


if __name__ == '__main__':
    xfer = Xfer()    
    xfer.setFtpParams('127.0.0.1', 'slam', 'passwd')
    #xfer.upload(srcDir)
    xfer.initEnv()
    srcDir = r"/home/sxc/CODEAPP/mynteye/samples/bin/dataset/image_0/"
    m=1
    while(1):
        filename='%06d.png'%m
        srcFile=srcDir+filename
        if os.path.isfile(srcFile):
            time.sleep(0.02)
            xfer.upload(srcFile)
        else:
            continue
        m = m + 1
        print(u'正在传输第%06d图片' % m)
    xfer.clearEnv()
