import os
import ftplib

ftp = ftplib.FTP("ftp.ncbi.nlm.nih.gov")
ftp.login()
ftp.cwd("/pubmed/baseline/")

filenames = ftp.nlst()

local_dir = "C:/Users/imran/pubmed_data"

if not os.path.exists(local_dir):
    os.makedirs(local_dir)

os.chdir(local_dir)

for filename in filenames:
    with open(filename, "wb") as f:
        ftp.retrbinary("RETR " + filename, f.write)

ftp.quit() 