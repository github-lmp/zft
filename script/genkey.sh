#!/usr/bin/expect -f

########################################
# Usage: ./genkey.sh host_IP password
########################################

set HOST [lindex $argv 0]
set PSWD [lindex $argv 1]
spawn -noecho ssh-copy-id -i /root/.ssh/id_rsa.pub $HOST  
#spawn -noecho scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no stop.sh $HOST:/tmp/  
expect {
	"*yes/no" { 
		send "yes\r"; exp_continue 
	}
	"password:" {
		send "$PSWD\r"; 
		expect {
			"denied" {exit 1} 
			eof
		}
	}
	"*No route to host" {exit 2}
	"*Connection refused" {exit 3}
}


