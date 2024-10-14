def get_input(prompt, default=None):
    """Helper function to get user input with optional default."""
    if default:
        return input(f"{prompt} [{default}]: ") or default
    else:
        return input(f"{prompt}: ")


def generate_env():
    # Collect inputs from the user
    key_name = get_input("Enter key_name", "redhat_key")
    root_password = get_input("Enter root_password", "secret")
    flavor_name = get_input("Enter flavor_name", "vepc-ow-fe85")
    image_name = get_input("Enter image_name", "integra-vnf-8.5_GA")

    # Dynamic user input for any number of FEs
    num_fes = int(get_input("Enter the number of FEs", "2"))
    vm_name = get_input(f"Enter vm_name for {num_fes} FEs (comma separated)",
                        "f1252cnbvowfebq85-01,f1252cnbvowfebq85-02").split(",")
    vm_name_str = f"[{','.join(vm_name)}]"  # Joining without spaces around commas

    ovs_management = get_input("Enter ovs_management", "vEPC_BackChannel_MGMT3_Tagged")
    sriov_0_1 = get_input("Enter sriov_0_1", "sriov-0-1-flat")
    sriov_0_2 = get_input("Enter sriov_0_2", "sriov-0-2-flat")
    sriov_1_1 = get_input("Enter sriov_1_1", "sriov-1-1-flat")
    sriov_1_2 = get_input("Enter sriov_1_2", "sriov-1-2-flat")
    aaa_net = get_input("Enter aaa_net", "vEPC_CnBvOWFE_BM1R")
    ldap_net = get_input("Enter ldap_net", "vEPC_CnBvOWFE_BMAPP")

    oam_ip = get_input(f"Enter OAM IPs for {num_fes} FEs (comma separated)", "10.7.14.103,10.7.14.104").split(",")
    oam_ip_str = f"[{','.join(oam_ip)}]"  # Joining without spaces around commas

    oamnetmask = get_input("Enter OAM netmask", "255.255.255.0")
    oamgw = get_input("Enter OAM gateway", "10.7.14.1")
    ntp_servers = get_input("Enter NTP servers (comma separated)", "172.25.153.53,172.25.153.13,172.25.164.163")

    # Dynamic generation of port names based on number of FEs
    port_names = {}
    for i in range(1, num_fes + 1):
        ports = get_input(f"Enter port names for FE{i} (comma separated)",
                          f"f1252cnbvowfebq85-0{i}-MGMT,f1252cnbvowfebq85-0{i}-SIDE-A,f1252cnbvowfebq85-0{i}-SIDE-B,f1252cnbvowfebq85-0{i}-BM1R,f1252cnbvowfebq85-0{i}-BMAPP").split(",")
        port_names[f"port{i}_name"] = ports

    subvlan = get_input("Enter subvlan", "244")
    subnetmask4 = get_input("Enter subnetmask4", "255.255.255.192")
    subipv4 = get_input(f"Enter subipv4 for {num_fes} FEs (comma separated)", "10.5.50.56,10.5.50.57").split(",")
    subipv4_str = f"[{','.join(subipv4)}]"

    subipv6 = get_input(f"Enter subipv6 for {num_fes} FEs (comma separated)", "2605:b100:fff4::2b9/122,2605:b100:fff4::2ba/122").split(",")
    subipv6_str = f"[{','.join(subipv6)}]"

    intvlan = get_input("Enter intvlan", "245")
    intnetmask4 = get_input("Enter intnetmask4", "255.255.255.192")
    intipv4 = get_input(f"Enter intipv4 for {num_fes} FEs (comma separated)", "10.5.50.120,10.5.50.121").split(",")
    intipv4_str = f"[{','.join(intipv4)}]"

    intipv6 = get_input(f"Enter intipv6 for {num_fes} FEs (comma separated)", "2605:b100:fff4::2f9/126,2605:b100:fff4::2fa/126").split(",")
    intipv6_str = f"[{','.join(intipv6)}]"

    ipv6dfgw = get_input("Enter ipv6 default gateway", "2605:b100:fff4::2c1")
    defgw = get_input("Enter default gateway", "10.5.50.65")
    sub4gw = get_input("Enter subnet IPv4 gateway", "10.5.50.1")
    sub6gw = get_input("Enter subnet IPv6 gateway", "2605:b100:fff4::281")

    aaa_ip = get_input(f"Enter AAA IPs for {num_fes} FEs (comma separated)", "10.7.39.103,10.7.39.104").split(",")
    aaa_ip_str = f"[{','.join(aaa_ip)}]"

    aaa_mask = get_input("Enter AAA mask", "255.255.255.0")
    aaa_gw = get_input("Enter AAA gateway", "10.7.39.1")

    ldap_ip = get_input(f"Enter LDAP IPs for {num_fes} FEs (comma separated)", "10.7.43.103,10.7.43.104").split(",")
    ldap_ip_str = f"[{','.join(ldap_ip)}]"

    ldap_mask = get_input("Enter LDAP mask", "255.255.255.0")
    ldap_gw = get_input("Enter LDAP gateway", "10.7.43.1")

    wait_for = get_input("Enter wait_for", "oam01:8080")
    fe_region = get_input("Enter FE region", "87Ontario")
    sys_component = get_input("Enter system components (comma separated)", "Core,STM,WebFiltering,IPTM,TCPAcc,RBM")
    cc_ramdisk_size = get_input("Enter cc_ramdisk_size", "20%")
    oam_registration_timeout = get_input("Enter OAM registration timeout", "3600")

    service_ifc = get_input("Enter service interface", "eth0")
    dataplane_vnic_type = get_input("Enter dataplane vNIC type", "direct")

    oam01_svc_ip = get_input("Enter OAM01 service IP", "10.7.12.100")
    oam02_svc_ip = get_input("Enter OAM02 service IP", "10.7.13.100")

    stack_name = get_input("Enter stack name", "87ontario")
    resource_index = get_input(f"Enter resource index for {num_fes} FEs (comma separated)", "03,04").split(",")
    resource_index_str = f"[{','.join(resource_index)}]"

    # Generate the ENV template based on user inputs
    env_content = f"""
parameters:
  key_name: {key_name}
  root_password: {root_password}
  flavor_name: {flavor_name}
  image_name: {image_name}
  vm_name: {vm_name_str}

  ovs_management: {ovs_management}
  sriov_0_1: {sriov_0_1}
  sriov_0_2: {sriov_0_2}
  sriov_1_1: {sriov_1_1}
  sriov_1_2: {sriov_1_2}
  aaa_net: {aaa_net}
  ldap_net: {ldap_net}

  oam_ip: {oam_ip_str}
  oamnetmask: {oamnetmask}
  oamgw: {oamgw}
  ntp_servers: {ntp_servers}
"""

    for port_name, ports in port_names.items():
        env_content += f"  {port_name}: [{','.join(ports)}]\n"

    env_content += f"""
  subvlan: {subvlan}
  subnetmask4: {subnetmask4}
  subipv4: {subipv4_str}
  subipv6: {subipv6_str}

  intvlan: {intvlan}
  intnetmask4: {intnetmask4}
  intipv4: {intipv4_str}
  intipv6: {intipv6_str}

  ipv6dfgw: {ipv6dfgw}
  defgw: {defgw}
  sub4gw: {sub4gw}
  sub6gw: {sub6gw}

  aaa_ip: {aaa_ip_str}
  aaa_mask: {aaa_mask}
  aaa_gw: {aaa_gw}

  ldap_ip: {ldap_ip_str}
  ldap_mask: {ldap_mask}
  ldap_gw: {ldap_gw}

# Integra system settings
  wait_for: {wait_for}
  fe_region: {fe_region}
  sys_component: {sys_component}
  cc_ramdisk_size: {cc_ramdisk_size}
  oam_registration_timeout: {oam_registration_timeout}

# Network settings
  service_ifc: {service_ifc}

# vnic type for internet and subscriber ports. specify "direct" for SR-IOV passthrough. maps to OS::Neutron::Port#binding:vnic_type. default is "normal"
  dataplane_vnic_type: {dataplane_vnic_type}

# System settings
  ntp_servers: {ntp_servers}

# OAM IPs
  oam01_svc_ip: {oam01_svc_ip}
  oam02_svc_ip: {oam02_svc_ip}

# Stackname and index
  stack_name: {stack_name}
  resource_index: {resource_index_str}
"""

    # Generate the file name using the first and last resource indices
    fe_base_name = vm_name[0].split('-')[0]  # Get the base name from the first FE name
    fe_index_range = f"{resource_index[0]}_{resource_index[-1]}"  # Create the range string (e.g., "03_04")
    file_name = f'{fe_base_name}-{fe_index_range}.env'  # Create the full file name

    # Write the ENV content to the file
    with open(file_name, 'w') as file:
        file.write(env_content)

    print(f"ENV configuration file '{file_name}' has been created.")

# Run the function to generate the ENV
generate_env()
