import sys;

hosts = {"host":{"all":[], "one":""}, "alias":{"all":[], "one":""}};

def main():
	global hosts;
	print("Le Shell de VHost");
	print(sys.argv);
	
	# step 1
	localhost = input("saisir l\'adresse de localhost?\n");
	if not len(localhost):
		localhost = "127.0.0.1";
	host = input("saisir le nom de virtualhost?\n");
	if not len(host):
		host = "duo";
	address = input("saisir le nom des adresses ip?\n");
	if not len(address):
		address = "127.0.0.10";
	
	port = input("saisir le port utiliser?\n");
	if not len(port):
		port = "80";
	prefixs = input("saisir les prefixes?\n");
	if not len(prefixs):
		prefixs = "hr";
	domains = input("saisir les domaines?\n");
	if not len(domains):
		domains = "tn";
	dr = input("saisir le document root?\n");
	if not len(dr):
		dr = host;
	dr = "c:/wamp/www/" + dr;
	
	# step 2
	prefixs = prefixs.split(",");
	prefixs = list(filter((lambda x: len(x)), prefixs));
	prefixs = list(set(prefixs + ["ar", "en", "fr"]));
	print(prefixs);
	domains = domains.split(",");
	domains = list(filter((lambda x: len(x)), domains));
	domains = list(set(domains + ["io", "com", "gov", "net", "org"]));
	print(domains);
	
	# step 3
	for v in domains:
		#print("for domain", v);
		hosts["alias"]["all"].append("%s.%s" % (host, v));
		hosts["alias"]["all"].append("*.%s.%s" % (host, v));
		
		hosts["host"][v] = {};
		hosts["host"][v]["all"] = [];
		for val in prefixs:
			#print("for prefix", val);
			hosts["host"][v]["all"].append("%s.%s.%s" % (val, host, v));
			hosts["host"][v]["all"].append("www.%s.%s.%s" % (val, host, v));
		
		hosts["host"][v]["all"] = list(set(hosts['host'][v]["all"]));
		hosts["host"][v]["one"] = " ".join(hosts["host"][v]["all"]);
		hosts["host"]["all"] += hosts["host"][v]["all"];
		hosts["host"]["one"] += "%s %s\n" % (localhost, hosts["host"][v]["one"]);
	
	hosts['alias']["all"] = list(set(hosts['alias']["all"]));
	hosts["alias"]["one"] = " ".join(hosts["alias"]["all"]);
	hosts["host"]["one"] = hosts["host"]["one"][0:-1];
	
	# step 4
	ligne1 = """
# {host} {address}:{port}
<IfDefine !APACHE24>
	NameVirtualHost {address}:{port}
</IfDefine>
<VirtualHost {sn}:{port} {address}:{port}>
	DocumentRoot \"{dr}\"
	ServerAdmin webmaster@{sn}
	ServerName {sn}
	ServerAlias {sa}

	<Directory \"{dr}\">
		DirectoryIndex index.php
		Options Indexes FollowSymLinks MultiViews
		AllowOverride All
	    
	    <IfDefine APACHE24>
            Require local
			Require all granted
        </IfDefine>
		
		<IfDefine !APACHE24>
			Order Deny, Allow
			Deny from all
			Allow from all
		</IfDefine>
	</Directory>

	ErrorLog \"c:/wamp/logs/{host}-apache_error.log\"
	LogLevel warn
	CustomLog \"c:/wamp/logs/{host}-access.log\" combined
	#RewriteLog \"c:/wamp/logs/{host}-rewrite.log\"
	#RewriteLogLevel 3
</VirtualHost>
""".format(host=host, address=address, port=port, sn=hosts["alias"]["all"][0], sa=hosts["alias"]["one"], dr=dr);
	
	ligne2 = """
{0}
""".format(hosts["host"]["one"]);
	
	print('Generation de vhost');
	print('Code generated for Apache 2.2.x and Apache 2.4.x');
	print("-" * 60);
	print(ligne1);
	print("-" * 60);
	print(ligne2);
	print("-" * 60);
	
	import json;
	print(json.dumps(hosts, sort_keys=True, indent=4));
	print("-" * 60);

if __name__ == "__main__":
	main();
