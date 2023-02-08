import ftplib

ftp = ftplib.FTP("ftp.ncbi.nlm.nih.gov")
ftp.login()
ftp.cwd("/pubmed/baseline/")

filenames = ftp.nlst()

for filename in filenames:
    with open(filename, "wb") as f:
        ftp.retrbinary("RETR " + filename, f.write)

ftp.quit()