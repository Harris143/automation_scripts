import re

# Function to generate the file content based on user input
def generate_script(hostname_pattern, fe_name, subscriber_ipv4, subscriber_ipv6, internet_ipv4, internet_ipv6, subvlan,
                    internetvlan, aaa, ldap):
    # Extract base hostname and FE numbers
    match = re.match(r"([a-zA-Z0-9\-]+)\{(\d+)\.\.(\d+)\}", hostname_pattern)
    if match:
        base_hostname = match.group(1)
        fe_start_str = match.group(2)
        fe_end_str = match.group(3)
        fe_start = int(fe_start_str)
        fe_end = int(fe_end_str)
        width = len(fe_start_str)  # To preserve leading zeros
    else:
        print("Invalid hostname pattern.")
        return

    # Initialize the script content
    script_content = "#Change hostname to Bell standard name\n\n"

    # First command applies to all hosts
    script_content += f"for host in {hostname_pattern}; do echo $host; ssh -q $host \"grep -i hostname /etc/sysconfig/network\"; done\n"

    # Loop over each FE number for individual commands
    for i in range(fe_start, fe_end + 1):
        fe_number_str = f"{i:0{width}}"
        host_with_number = f"{base_hostname}{{{fe_number_str}..{fe_number_str}}}"
        fe_name_with_number = f"{fe_name}-{fe_number_str}"

        # Command to change hostname in /etc/sysconfig/network
        script_content += f"for h in {host_with_number}; do echo $h; ssh -q $h \"perl -pi -e's#localhost.localdomain#{fe_name_with_number}#g' /etc/sysconfig/network\"; done\n"

    # Commands that apply to all hosts
    script_content += f"for host in {hostname_pattern}; do echo $host; ssh -q $host \"grep -i hostname /etc/sysconfig/network\"; done\n"
    script_content += f"for host in {hostname_pattern}; do echo $host; ssh -q $host \"hostnamectl set-hostname {fe_name}-\\`hostname|tail -c 3\\`\"; done\n"
    script_content += f"for host in {hostname_pattern}; do echo $host; ssh -q $host \"hostname\"; done\n"
    script_content += f"for host in {hostname_pattern}; do echo $host; ssh -q $host \"hostnamectl\"; done\n\n"

    # Updates ssh file to allow Bell tools access
    script_content += "#Updates ssh file to allow Bell tools access\n\n"
    script_content += f"for host in {hostname_pattern}; do echo $host; ssh -q $host \"cp /etc/ssh/sshd_config /etc/ssh/sshd_config_backup\"; done\n"
    script_content += f"for host in {hostname_pattern}; do echo $host; ssh -q $host \"perl -pi -e 's#AllowUsers root opwv cloud-user#AllowUsers root opwv cloud-user pdsnroutine1 hpna psacdsrw#g' /etc/ssh/sshd_config\"; done\n"
    script_content += f"for host in {hostname_pattern}; do echo $host; ssh -q $host \"grep -i AllowUsers /etc/ssh/sshd_config\"; done\n\n"

    # Perform a reboot before Validating all configuration
    script_content += "#Perform a reboot before Validating all configuration\n"
    script_content += f"for h in {hostname_pattern}; do echo $h; ssh -q $h \"reboot\"; done\n\n"

    # Verify the SNMP configuration file on each new FE node is properly configured
    script_content += "#Verify the SNMP configuration file on each new FE node is properly configured\n"
    script_content += f"for h in {hostname_pattern}; do echo $h; ssh -q $h \"grep -i snmpTargetAddrEntry /opt/opwv/oam/8.5/snmpcfg/snmpd.cnf -A 1; sleep 1; echo; echo\"; done\n\n"

    # Check for owm aliases setting on the new node
    script_content += "#Check for owm aliases setting on the new node\n"
    script_content += f"for h in {hostname_pattern}; do echo $h; ssh -q $h \"ls -lrth /root/owm.aliases\"; done\n\n"

    # Check for all the software rpm packages
    script_content += "#Check for all the software rpm packages\n"
    script_content += f"for h in {hostname_pattern}; do echo $h; ssh -q $h \"rpm -qa |grep -i opwv |wc -l\"; done\n\n"

    # Check all the new FE have the correct ConfigServer for the Region
    script_content += "#Check all the new FE have the correct ConfigServer for the Region\n"
    script_content += f"for h in {hostname_pattern}; do echo $h; ssh -q $h \"grep ConfigServer /etc/opwv/oam-v8.5/oam_bootstrap.xml\"; done\n\n"

    # Check for hostname
    script_content += "#Check for hostname\n"
    script_content += f"for h in {hostname_pattern}; do echo $h; ssh -q $h \"echo 'Verify------>'; hostname; echo '--------'; echo\"; done\n"
    script_content += f"for h in {hostname_pattern}; do echo $h; ssh -q $h \"cat /opt/opwv/ost/etc/vars\"; done\n"
    script_content += f"for h in {hostname_pattern}; do echo $h; ssh -q $h \"cksum /opt/opwv/oam/8.5/tools/reporting/scripts/conf/thresholds.conf\"; done\n"
    script_content += f"for h in {hostname_pattern}; do echo $h; ssh -q $h \"rpm -qa |grep -i opwv |grep ost\"; done\n\n"

    # Check the filesystem layout the same as the other existing FE.
    script_content += "#Check the filesystem layout the same as the other existing FE.\n"
    script_content += f"for h in {hostname_pattern}; do echo $h; ssh -q $h \"df -kh\"; done\n\n"

    # Check the SCA status
    script_content += "#Check the SCA status\n"
    script_content += f"for h in {hostname_pattern}; do echo $h; ssh -q $h \"/etc/init.d/oamsca-v8.5 status\"; done\n\n"

    # Check for iptables configuration
    script_content += "#Check for iptables configuration\n"
    script_content += f"for h in {hostname_pattern}; do echo $h; ssh -q $h \"iptables -t mangle -L -n |wc -l\"; done\n\n"

    # Check for the TCP Acceleration profiles
    script_content += "#Check for the TCP Acceleration profiles:\n"
    script_content += f"for h in {hostname_pattern}; do echo $h; ssh -q $h \"echo 'Verify------->'; hostname; /opt/opwv/integra/8.5/tools/vpp/bin/vppctl tp_show_tcp_profile port 443; sleep 2; echo; echo; echo\"; done\n"
    script_content += f"for h in {hostname_pattern}; do echo $h; ssh -q $h \"echo 'Verify------->'; hostname; /opt/opwv/integra/8.5/tools/vpp/bin/vppctl tp_show_tcp_profile port 8080; sleep 2\"; done\n\n"

    # Check for MTU/MSS settings
    script_content += "#Check for MTU/MSS settings:\n"
    script_content += f"for h in {hostname_pattern}; do echo $h; ssh -q $h \"echo 'Verify------->'; hostname; uptime; echo; ifconfig |grep -i mtu; sleep 2; echo '-----------'; echo\"; done\n"
    script_content += f"for h in {hostname_pattern}; do echo $h; ssh -q $h \"echo 'Verify------->'; hostname; iptables -t mangle -L -n |grep TCPMSS; echo '-----------'; echo\"; done\n"
    script_content += f"for h in {hostname_pattern}; do echo $h; ssh -q $h \"echo 'Verify------->'; hostname; ip6tables -t mangle -L -n |grep TCPMSS; echo '-----------'; echo\"; done\n\n"

    # Check for NTP - Chrony is now used for NTP time
    script_content += "#Check for NTP - Chrony is now used for NTP time:\n"
    script_content += f"for h in {hostname_pattern}; do echo $h; ssh -q $h \"chronyc sources\"; done\n"
    script_content += f"for h in {hostname_pattern}; do echo $h; ssh -q $h \"timedatectl\"; done\n"
    script_content += f"for h in {hostname_pattern}; do echo $h; ssh -q $h \"clock\"; done\n\n"

    # Check for Static routes
    script_content += "#Check for Static routes - Static routes should be similar to 8.2 FE\n"
    script_content += f"for h in {hostname_pattern}; do echo $h; ssh -q $h \"netstat -rn\"; done\n"
    script_content += f"for h in {hostname_pattern}; do echo $h; ssh -q $h \"netstat -6 -rn\"; done\n\n"

    # Check network reachability
    script_content += "# Check network reachability (To F5 and the next hop routers)\n"
    script_content += f"for h in {hostname_pattern}; do echo $h; ssh -q $h \"ping -c 2 {subscriber_ipv4} -I vbond0.{subvlan} | grep loss\"; done\n"
    script_content += f"for h in {hostname_pattern}; do echo $h; ssh -q $h \"ping -c 2 {internet_ipv4} -I vbond0.{internetvlan} | grep loss\"; done\n"
    script_content += f"for h in {hostname_pattern}; do echo $h; ssh -q $h \"ping6 -c 2 {subscriber_ipv6} -I vbond0.{subvlan} | grep loss\"; done\n"
    script_content += f"for h in {hostname_pattern}; do echo $h; ssh -q $h \"ping6 -c 2 {internet_ipv6} -I vbond0.{internetvlan} | grep loss\"; done\n"
    script_content += f"for h in {hostname_pattern}; do echo $h; ssh -q $h \"ping -c 2 {aaa} -I eth3 | grep loss\"; done\n"
    script_content += f"for h in {hostname_pattern}; do echo $h; ssh -q $h \"ping -c 2 {ldap} -I eth4 | grep loss\"; done\n\n"

    # Check for open ports
    script_content += "# Check for open ports\n"
    script_content += f"for h in {hostname_pattern}; do echo $h; ssh -q $h \"netstat -peanut|grep 80|grep LISTEN\"; done\n"

    return script_content

# Function to get user inputs and generate the script
def get_user_input_and_generate_script():
    # Get user inputs
    hostname_pattern = input("Enter the hostname(s) (e.g., winnipeg-fe{03..04}): ")
    fe_name = input("Enter the FE name (e.g., m1271cnbvowfewq85): ")
    subscriber_ipv4 = input("Enter the Subscriber IPv4: ")
    subscriber_ipv6 = input("Enter the Subscriber IPv6: ")
    internet_ipv4 = input("Enter the Internet IPv4: ")
    internet_ipv6 = input("Enter the Internet IPv6: ")
    subvlan = input("Enter the Subscriber VLAN: ")
    internetvlan = input("Enter the Internet VLAN: ")
    aaa = input("Enter the AAA server IPv4: ")
    ldap = input("Enter the LDAP server IPv4: ")

    # Generate the script content
    script = generate_script(hostname_pattern, fe_name, subscriber_ipv4, subscriber_ipv6, internet_ipv4, internet_ipv6,
                             subvlan, internetvlan, aaa, ldap)

    # Extract the first FE number from the hostname pattern for the file name
    match = re.match(r"([a-zA-Z0-9\-]+)\{(\d+)\.\.(\d+)\}", hostname_pattern)
    if match:
        base_hostname = match.group(1)
        fe_start_str = match.group(2)
        fe_end_str = match.group(3)
        # Use the first FE number in the file name
        file_name = f"validation_script-{base_hostname}{fe_start_str}-{fe_end_str}.sh"
    else:
        file_name = "validation_script.sh"  # Default name if pattern doesn't match

    # Save the script to the file
    with open(file_name, "w") as file:
        file.write(script)

    print(f"Script generated and saved as '{file_name}'.")

# Run the function
get_user_input_and_generate_script()
