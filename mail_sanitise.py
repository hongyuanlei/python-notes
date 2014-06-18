# -*- coding:utf-8 -*-

reply_message = """
This message contained an attachment that was stripped out.
The filename was: %(filename)s,
The original type was: %(content_type)s
(and it had additional parameters of:%(params)s)
"""

import re
bad_content_re = re.compile('application/(msword|msexcel)',re.I)
bad_fileext_re = re.compile(r'(\.exe|\.py|\.pyc|\.zip|\.pif|\.scr|\.ps)$')

def sanitise(msg):
    '''剥去消息中所有可能的危险载荷'''
    ct = msg.get_content_type()
    fn = msg.get_filename()
    if bad_content_re.search(ct) or (fn and  bad_fileext_re.search(fn)):
        #有威胁的消息部分，先获取用于报告的信息，然后销毁
        #将content-type、键列表、值对的参数表示成key=value
        #的形式，并以逗号隔开
        print msg.get_params()
        params = msg.get_params()[1:]
        params = ','.join(['='.join(p) for p in params])
        #将通知消息作为新载荷
        replace = reply_message % dict(content_type=ct,filename=fn,params=params)
        msg.set_payload(replace)
        #移除参数并在content-type头部设置内容
        for k,v in msg.get_params()[1:]:
            msg.del_param(k)
        msg.set_type("text/plain")
        #删除没有content-type的头部
        del msg['Content-Transfer-Encoding']
        del msg['Content-Disposition']
    else:
        #现在检查消息的所有子部分
        if msg.is_multipart():
            #对各子部分递归调用sanitise
            payload = [sanitise(x) for x in msg.get_payload()]
            #用清理过的载荷列表替换
            msg.set_payload(payload)
    #返回清理过的消息
    return msg


if __name__ == '__main__':
    import email,smtplib,sys,cStringIO
    FILE_NAME = "dir_contents_mail"
    message = email.message_from_file(open(FILE_NAME))
    message = sanitise(message)
    fp = cStringIO.StringIO()
    g = email.Generator.Generator(fp)
    g.flatten(message)

#    MAIL_HOST = ""
#    MAIL_PORT = 25
#    MAIL_USER = ""
#    MAIL_PASSWD = ""
#    FROM_ADDR = "example@example.com"
#    TO_ADDR = "example@example.com";

#    server = smtplib.SMTP(MAIL_HOST,25)
#    server.login(MAIL_USER,MAIL_PASSWD)
#    server.sendmail(FROM_ADDR,TO_ADDR,fp.getvalue())

        
    
