
		];
	};
	
	//Generate a random index for the proxy list
	try
	{
		var index=-1;
		while(index<0&&proxylist[index].toString()=="")
			index=Math.ceil(proxylist.length*Math.random())-1;

		if(proxylist.length)
		{
			if(ENABLE_LOGGING)
				alert("Rule not triggered!\n" + dnsResolve(host) + "\n" + host.toLowerCase() + "\n" + url.toLowerCase() + "\nUsing Proxy: " + proxylist[index]);
			return "PROXY "+proxylist[index];
		}
		else
			return "DIRECT";
	}
	catch(e)
	{
		if(ENABLE_LOGGING)
			alert("An exception has been encountered!\n" + proxylist);
		return "DIRECT";
	};
}