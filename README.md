### google-leak

`google-leak` lets you easily track sensitive data upon using Google Dorks from common resources where collaborators might share unintentionally. This Python script allows you to send such information to your SIEM solution based on a given schedule, so that you can have visibility of shadow IT projects that your employees might be using, ~~restricted~~ information, secrets within repositories and more options as soon as Google indexes new resources.

### Why?
It's quite common to obtain sensitive information with the usage of google dorks as we can see through [exploit-db - google hacking database](https://www.exploit-db.com/google-hacking-database) that is updated every day.  Additionally, some resources are becoming a traditional source of data leak where employees might be using over the years without knowing that their data is shared publicly as we can see with [Trelo on this blog post](https://www.kaspersky.com/blog/trello-data-leaks/39497/). 

Different scenarios on Cloud environments are also a major source for data leak due to the misinterpretation of the shared responsibility model and misconfigured services. We can also rely on different tools over GitHub and also other ones such as different search engines like [https://buckets.grayhatwarfare.com/](https://buckets.grayhatwarfare.com/). And as you may suspect, for every item indexed by a search engine such as Google whereas the resource should not be public, more problems might arise

### Building image with Dockerfile
1. `git clone https://github.com/pahennig/google-leak`
2. Build the image:
	*  `docker build -t prh/google-leak .`
3. Run the container, and ensure to specify the following arguments:
	* `$COMPANY`
	* `$SIEM_IP`
	* `$SIEM_SYSLOG_PORT` 
4. If your SIEM is already fed by different log sources that use rsyslog protocol on the same server you're using to run the script, you can run the container with a specified hostname (`-h or --hostname`) in order to avoid mixed events in the same log source identifier as per the following example:
	* `docker run -h google-leak -v $(pwd):/usr/app prh/google-leak unicorns 192.168.100.30 514`

### Schedule
Since the script will use a base file to interpret new findings, you can use it based on a given schedule in order to provide awareness to your Blue or SOC team. For instance, the example below is running the container once a day between Monday and Friday:
* `0 8 * * 1-5 /bin/bash /home/ec2-user/blue-team/google-leak/cronfile.sh`

As an example of the mentioned shell file within our cron, refer to this example:
* [cronfile.sh](https://github.com/pahennig/google-leak/blob/main/cronfile.sh)
