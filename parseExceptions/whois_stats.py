from datetime import datetime, timedelta
from urllib.parse import urlparse
import os
import pandas as pd

BASE_PATH = "/opt/tomcat/conf/dailybasecrawler/"

jobs_path = {
            "cctld": ["cctld/exception/", "cctld/dailybase/exception/"],
            "gtld": ["gtld/exception/"],
            "monitoring": ["monitoring/brand/exception/"],
            "bulk": ["bulk/exception/"]
        }

file_names = [("rdap_exception_", "rdap_exception"), ("invocation_exception.csv_", "invocation_exception"), ("io_exception.csv_", "io_exception"), ("io_exception.csv_secondregistrar", "io_exception_second_registrar"), ("no_such_method_exception.csv_", "no_such_method_exception"), ("parse_exception.csv_", "parse_exception"), ("scrapper_exception_", "scrapper_exception"), ("whois_client_CLUSTER_", "whois_client_cluster"), ("whois_client_PROXY_RACK_", "proxy_rack"), ("whois_client_SMART_PROXY_", "smart_proxy"),("tld_client_exception_", "tld_client_exception")]

def parseURL(x):
    try:
        hn = urlparse(x).hostname
        if hn:
            return hn
        return x
    except Exception as e:
        return None



class FormatResults:

    def __init__(self, job):
        self.content = "\n" + self.tocentered(job.upper(), 100, "-") +  "\n"

    def appendToContent(self, data):
        self.content += data + "\n"

    def tocentered(self, data, max_length, key = " "):
        data = str(data)
        spaces = max_length - len(data)
        space_per_side = spaces // 2
        return key*space_per_side + data + key*(spaces - space_per_side)

    def toright(self, data, max_length, key = " "):
        data = str(data)
        return key * (max_length - len(data)) + data

    def toleft(self, data, max_length, key = " "):
        data = str(data)
        return data + key * (max_length - len(data))

    def centeredToContent(self, data, max_length = 100, key="-"):
        data = self.tocentered(data, max_length, key)
        self.content += data + "\n\n"

    def appendListToContent(self, data, max_length):
        formatted_text = self.toleft(data[0], max_length)

        for x in data[1:]:
            formatted_text += self.toright(x, 30)

        formatted_text += "\n"
        self.content += formatted_text


    def writeContentToFile(self, filepath):
        with open(filepath, "a") as fi:
            fi.write(self.content)
    
    def prepareTable(self, data, isTlds=True):

        table_type = "TLDS" if isTlds else "WhoisServers"
        columns = list(data.keys())

        total_tlds_or_servers = dict()

        for x in columns:
            for key, value in data[x].items():
                if total_tlds_or_servers.get(key):
                    total_tlds_or_servers[key] += value
                else:
                    total_tlds_or_servers[key] = value


        columns.insert(0, table_type)

        headers_max_length = max(len(x) for x in columns)
        tlds_or_server_max_length = max(len(x) for x in total_tlds_or_servers.keys())

        max_spaces = max(headers_max_length, tlds_or_server_max_length) + 2  # maximum spaces

        # for headers
        self.appendListToContent(list(map(lambda x: x.upper(), columns)), max_spaces)

        for tlds_or_servers in total_tlds_or_servers.keys():
            exception_count_list = [tlds_or_servers]
            for exceptions in columns[1:]:
                if data[exceptions].get(tlds_or_servers):
                    exception_count_list.append(data[exceptions].get(tlds_or_servers))
                else:
                    exception_count_list.append("")

            self.appendListToContent(exception_count_list, max_spaces)

        total_exceptions_count = ["Total"]
        for exceptions in columns[1:]:
            total_exceptions_count.append(sum(data[exceptions].values()))

        self.content += "\n"
        self.appendListToContent(total_exceptions_count, max_spaces)
        self.content += "\n--------------------------------------------------------------------------\n"

    





class ParsedFiles:
    
    def __init__(self):
        self.tlds = dict()
        self.servers = dict()


    def smart_proxy(self, path, previous_date):
        file_path = path + previous_date + ".csv"
        if not os.path.exists(file_path):
            return;
        df = pd.read_csv(file_path, usecols=[0,1,2], header=None, names=["dat", "domain", "server"])
        df["server"] = df["server"].apply(parseURL)
        df = df[df["server"].notna()]
        self.servers["smart_proxy"] = self.getDict(df, "server", False)
        del df


    def proxy_rack(self, path, previous_date):
        file_path = path + previous_date + ".csv"
        if not os.path.exists(file_path):
            return;
        df = pd.read_csv(file_path, usecols=[0,1,2], header=None, names=["dat", "domain", "server"])
        df["server"] = df["server"].apply(parseURL)
        df = df[df["server"].notna()]
        self.servers["proxy_rack"] = self.getDict(df, "server", False)
        del df
    
    def whois_client_cluster(self, path, previous_date):
        file_path = path + previous_date + ".csv"
        if not os.path.exists(file_path):
            return;
        df = pd.read_csv(file_path, usecols=[0,1,2], header=None, names=["dat", "domain", "server"])
        self.servers["cluster"] = self.getDict(df, "server", False)
        del df

    def scrapper_exception(self, path, previous_date):
        file_path = path + previous_date + ".csv"
        if not os.path.exists(file_path):
            return;
        df = pd.read_csv(file_path, usecols=[0,1], header=None, names=["dat", "server"])
        pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$'
        df = df[df["dat"].str.match(pattern)]
        df["server"] = df["server"].apply(parseURL)
        df = df[df["server"].notna()]
        self.servers["scrapper"] = self.getDict(df, "server", False)
        del df

    def parse_exception(self, path, previous_date):
        file_path = path + previous_date
        if not os.path.exists(file_path):
            return;
        df = pd.read_csv(file_path, usecols=[0], header=None, names=["domain"])
        self.tlds["parse"] = self.getDict(df, "domain", True)
        del df


    def no_such_method_exception(self, path, previous_date):
        file_path = path + previous_date
        if not os.path.exists(file_path):
            return;
        df = pd.read_csv(file_path, usecols=[0], header=None, names=["domain"])
        self.tlds["no_such_method"] = self.getDict(df, "domain", True)
        del df

    def invocation_exception(self, path, previous_date):
        file_path = path + previous_date
        if not os.path.exists(file_path):
            return
        df = pd.read_csv(file_path, usecols=[0], header=None, names=["domain"])
        self.tlds["invocation"] = self.getDict(df, "domain", True)
        del df

    def io_exception(self, path, previous_date):
        file_path = path + previous_date
        if not os.path.exists(file_path):
            return
        df = pd.read_csv(file_path, usecols=[0], header=None, names=["domain"])
        self.tlds["io_exception"] = self.getDict(df, "domain", True)
        del df

    def io_exception_second_registrar(self, path, previous_date):
        file_path = path + previous_date
        if not os.path.exists(file_path):
            return
        df = pd.read_csv(file_path, usecols=[0,1], header=None, names=["domain", "error"])
        df["server"] = df["error"].apply(lambda x : x.split(":")[-1].strip())
        self.tlds["io_exception_registrar"] = self.getDict(df, "server", True)
        del df
        
    def rdap_exception(self, path, previous_date):
        file_path = path + previous_date + ".csv"
        if not os.path.exists(file_path):
            return
        df = pd.read_csv(file_path, usecols=[0, 1], header=None, names=["dat", "server"])
        df["server"] = df["server"].apply(parseURL)
        df = df[df["server"].notna()]
        self.servers["rdap"] = self.getDict(df, "server", False)
        del df

    def tld_client_exception(self, path, previous_date):
        file_path = path + previous_date + ".csv"
        if not os.path.exists(file_path):
            return
        df = pd.read_csv(file_path, usecols=[0, 1], header=None, names=["dat", "server"])
        df["server"] = df["server"].apply(parseURL)
        df = df[df["server"].notna()]
        self.servers["tld_client"] = self.getDict(df, "server", False)
        del df

    def getDict(self, df, column, istld):
        if istld:
            df["tld"] = df[column].apply(lambda x: x.split(".")[-1].split("/")[0].split(" ")[0])
            column = "tld"
        else:
            df[column] = df[column].apply(lambda x: x.split("/")[0])

        df[column] = df[column].str.strip()
        server_tld_count = df[column].value_counts()
        server_tld_count_dict = server_tld_count.to_dict()
        return server_tld_count_dict
        
        



if __name__  == "__main__":

    current_date = datetime.now()
    previous_date = current_date - timedelta(days=1)
    formatted_date = previous_date.strftime("%Y-%m-%d")

    for crawlers, crawlersPath in jobs_path.items():
        for path in crawlersPath:

            formatResults = FormatResults(crawlers)
            print(formatted_date)
            print(path)
            parsedFiles = ParsedFiles()
            
            for files in file_names:
                try:
                    func = getattr(parsedFiles, files[1])
                    file_path = BASE_PATH + path + files[0]
                    func(file_path, formatted_date)
                except Exception as e:
                    print(e)

            formatResults.centeredToContent(path)

            if bool(parsedFiles.servers):
                formatResults.prepareTable(parsedFiles.servers, False)

            if bool(parsedFiles.tlds):
                formatResults.prepareTable(parsedFiles.tlds)

            

            formatResults.writeContentToFile("/home/whois-1/cronjob/analysis/whois/" + formatted_date + ".txt")
