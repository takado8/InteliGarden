using System;
using System.IO;
using System.Net;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace userApp
{
    class ftp
    {
        private string _hostname;
        private string _user;
        private string _pass;

        public ftp(string hostname, string user, string pass)
        {
            _hostname = hostname;
            _user = user;
            _pass = pass;
        }

        public List<string> DirectoryListing(string dirfilename)
        {
            string fullpath = _hostname + dirfilename;
            FtpWebRequest request = (FtpWebRequest)WebRequest.Create(fullpath);

            request.Method = WebRequestMethods.Ftp.ListDirectory;
            request.Credentials = new NetworkCredential(_user, _pass);
            FtpWebResponse response = (FtpWebResponse)request.GetResponse();
            Stream responseStream = response.GetResponseStream();
            StreamReader reader = new StreamReader(responseStream, System.Text.Encoding.Default);
            List<string> result = new List<string>();

            while (!reader.EndOfStream)
            {
                result.Add(reader.ReadLine());
            }
            reader.Close();
            response.Close();
            return result;
        }

        public void Upload(string localpath, string dirfilename)
        {

            WebClient client = new WebClient();
            client.Credentials = new NetworkCredential(_user, _pass);
            string fullpath = _hostname + dirfilename;
            client.UploadFile(fullpath, localpath);

        }

        public void Download(string dirfilename, string localpath)
        {
            WebClient client = new WebClient();
            client.Credentials = new NetworkCredential(_user, _pass);
            string fullpath = _hostname + dirfilename;
            client.DownloadFile(fullpath, localpath);
        }

        public void Delete(string dirfilename)
        {
            string fullpath = _hostname + dirfilename;
            FtpWebRequest request = (FtpWebRequest)WebRequest.Create(fullpath);
            request.Credentials = new NetworkCredential(_user, _pass);
            request.Method = WebRequestMethods.Ftp.DeleteFile;
            FtpWebResponse response = (FtpWebResponse)request.GetResponse();
            Console.WriteLine("Delete status: {0}", response.StatusDescription);
            response.Close();
        }

        public void CreateDir(string dirpath)
        {
            string fullpath = _hostname + dirpath;
            WebRequest request = WebRequest.Create(fullpath);
            request.Method = WebRequestMethods.Ftp.MakeDirectory;
            request.Credentials = new NetworkCredential(_user, _pass);
            using (var resp = (FtpWebResponse)request.GetResponse())
            {
                Console.WriteLine(resp.StatusCode);
            }
        }

        public void DeleteDir(string dirpath)
        {
            string fullpath = _hostname + dirpath;
            WebRequest request = WebRequest.Create(fullpath);
            request.Method = WebRequestMethods.Ftp.RemoveDirectory;
            request.Credentials = new NetworkCredential(_user, _pass);
            using (var resp = (FtpWebResponse)request.GetResponse())
            {
                Console.WriteLine(resp.StatusCode);
            }
        }
    }
}
