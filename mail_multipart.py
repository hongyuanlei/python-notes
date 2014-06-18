# -*- coding:utf-8 -*-

import base64
import quopri
import mimetypes,email.Generator,email.Message
import cStringIO,os

T_ADDR = "example@example.com"
F_ADDR = "example@example.com"

output_file = "dir_contents_mail"

def main():
    main_msg = email.Message.Message()
    main_msg["To"] = T_ADDR
    main_msg["From"] = F_ADDR
    main_msg["Subject"] = "Directory contents"
    main_msg["Mime-version"] = "1.0"
    main_msg["Content-type"] = "Multipart/mixed"
    main_msg.preamble = "Mime message\n"
    main_msg.epilogue = ""

    file_names = [f for f in os.listdir(os.curdir) if os.path.isfile(f)]
    for file_name in file_names:
        content_type,ignored = mimetypes.guess_type(file_name)
        if content_type is None:
            content_type = "application/octet-stream"
        contents_encoded = cStringIO.StringIO()
        with open(file_name,"rb") as f:
            main_type = content_type[:content_type.find("/")]
            if main_type == "text":
                cte = "quoted-printable"
                quopri.encode(f,contents_encoded,True)
            else:
                cte = "base64"
                base64.encode(f,contents_encoded)
        sub_msg = email.Message.Message()
        sub_msg.add_header("Content-type",content_type,name=file_name)
        sub_msg.add_header("Content-transfer-encoding",cte)
        sub_msg.set_payload(contents_encoded.getvalue())
        contents_encoded.close()
        main_msg.attach(sub_msg)
    body_content = email.Message.Message()
    body_content.set_type("text/plain")
    body_content.set_payload("hello word")
    main_msg.attach(body_content)
    
    f = open(output_file,"wb")
    g = email.Generator.Generator(f)
    g.flatten(main_msg)
    f.close()
    return None

if __name__ == '__main__':
    main()
    
    import smtplib
    f = open(output_file,"r")
    html = f.read()
    f.close()
    

    EMAIL_HOST = ""
    EMAIL_PORT = 25
    server = smtplib.SMTP(EMAIL_HOST,EMAIL_PORT)
    server.sendmail(F_ADDR,T_ADDR,html)
    server.quit()
           
