#!/usr/bin/python
import six
import time
import sys
import datetime
import os
import tarfile
import shutil
import urllib
match_str = ["out: Ran", "out: OK", "out: FAILED", "Start to", "Opening OVA source" ]
print_seq = ["nimbus_deploy", "vio_ovf_deploy", "vio_deploy", "keystone", "glance",
             "nova", "cinder", "neutron", "heat", "scenario", "vmware"]
exclude_print = ["nimbus_deploy", "vio_ovf_deploy", "vio_deploy"]
def formal_output (timestamp):
    print "{0: <15}{1: <15}{2: <15}{3: <15}{4: <15}".format("step_name", "execution_time","total_tests","failed","skipped")
#print "{0: <20, 1: <20, 2: <20,3:< 20,4: <20}".format("step_name", "execution_time","total_tests", "failed", "skipped")
    for k in print_seq:
        if k in timestamp:
            v = timestamp[k] 
            if k in exclude_print:
                print "{0: <15}{1: <15}".format(k, v[1])
            else:
                print "{0: <15}{1: <15}{2: <15}{3: <15}{4: <15}".format(k, v[1], v[2], v[3], v[4])
def formal_label ():
    print "{0: <30}{1: <10}{2: <10}{3: <10} {4: <5}{5: <5}{6: <5}{7: <5} {8: <5}{9: <5}{10: <5}{11: <5}" \
           "{12: <5}{13: <5}{14: <5}{15: <5}{16: <5}{17: <5}{18: <5}{19: <5}{20: <5}{21: <5}{22: <5}{23: <5}" \
           "{24: <5}{25: <5}{26: <5}{27: <5}{28: <5}{29: <5}{30: <5}{31: <5}{32: <5}{33: <5}{34: <5}{35: <5}".format(
           "build_number", "t_nimbus","t_vio_ovf","t_vio","t_ks","ks_T","ks_F", "ks_S","t_g","g_T","g_F", "g_S",
           "t_n","n_T","n_F", "n_S","t_c","c_T","c_F", "c_S","t_nt","nt_T","nt_F", "nt_S","t_h","h_T","h_F", "h_S",
           "t_sc","sc_T","sc_F", "sc_S","t_vm","vm_T","vm_F", "vm_S")
def formal_data (t):
    if len(t) == 0:
        return
    if "vmware" in t.keys(): 
        print "{0: <30}{1: <10}{2: <10}{3: <10} {4: <5}{5: <5}{6: <5}{7: <5} {8: <5}{9: <5}{10: <5}{11: <5}" \
           "{12: <5}{13: <5}{14: <5}{15: <5}{16: <5}{17: <5}{18: <5}{19: <5}{20: <5}{21: <5}{22: <5}{23: <5}" \
           "{24: <5}{25: <5}{26: <5}{27: <5}{28: <5}{29: <5}{30: <5}{31: <5}{32: <5}{33: <5}{34: <5}{35: <5}".format(
           t["build"], t["nimbus_deploy"][1],t["vio_ovf_deploy"][1],t["vio_deploy"][1], 
           t["keystone"][1].split('.')[0],t["keystone"][2],t["keystone"][3],t["keystone"][4],
           t["glance"][1].split('.')[0],t["glance"][2],t["glance"][3],t["glance"][4],
           t["nova"][1].split('.')[0],t["nova"][2],t["nova"][3],t["nova"][4],
           t["cinder"][1].split('.')[0],t["cinder"][2],t["cinder"][3],t["cinder"][4],
           t["neutron"][1].split('.')[0],t["neutron"][2],t["neutron"][3],t["neutron"][4],
           t["heat"][1].split('.')[0],t["heat"][2],t["heat"][3],t["heat"][4],
           t["scenario"][1].split('.')[0],t["scenario"][2],t["scenario"][3],t["scenario"][4],
           t["vmware"][1].split('.')[0], t["vmware"][2],t["vmware"][3],t["vmware"][4]
           )
    else:
         print "{0: <30}{1: <10}{2: <10}{3: <10} {4: <5}{5: <5}{6: <5}{7: <5} {8: <5}{9: <5}{10: <5}{11: <5}" \
           "{12: <5}{13: <5}{14: <5}{15: <5}{16: <5}{17: <5}{18: <5}{19: <5}{20: <5}{21: <5}{22: <5}{23: <5}" \
           "{24: <5}{25: <5}{26: <5}{27: <5}{28: <5}{29: <5}{30: <5}{31: <5}".format(
           t["build"], t["nimbus_deploy"][1],t["vio_ovf_deploy"][1],t["vio_deploy"][1], 
           t["keystone"][1].split('.')[0],t["keystone"][2],t["keystone"][3],t["keystone"][4],
           t["glance"][1].split('.')[0],t["glance"][2],t["glance"][3],t["glance"][4],
           t["nova"][1].split('.')[0],t["nova"][2],t["nova"][3],t["nova"][4],
           t["cinder"][1].split('.')[0],t["cinder"][2],t["cinder"][3],t["cinder"][4],
           t["neutron"][1].split('.')[0],t["neutron"][2],t["neutron"][3],t["neutron"][4],
           t["heat"][1].split('.')[0],t["heat"][2],t["heat"][3],t["heat"][4],
           t["scenario"][1].split('.')[0],t["scenario"][2],t["scenario"][3],t["scenario"][4]
           )

def cal_exe_time(end, start):
    t1 = time.mktime(time.strptime(start,"%Y-%m-%d %H:%M:%S"))
    t2 = time.mktime(time.strptime(end,"%Y-%m-%d %H:%M:%S"))
    return datetime.timedelta(seconds=t2-t1)
def gen_data_from_url(url,compact = False):
#grep -E "out: Ran|out: OK|out: FAILED|Start to|Downloaded support" ../testbed\ 10/os-test.log
#    url = "http://p3-ci-int.eng.vmware.com/view/End%20to%20End/job/master-tempest-nsxv/lastSuccessfulBuild/artifact/testbed.tar.gz"
    tempestlog = urllib.URLopener()
    try: 
        tempestlog.retrieve(url,"/tmp/testbed.tar.gz")
    except IOError: 
#        print "Job result is lost, can not download ", url
        return []
    os.chdir("/tmp")
    filtered = []
    tar = tarfile.open("testbed.tar.gz")
    if compact:
        try: 
            f = tar.extractfile('testbed/os-test.log.1')
            content1 = f.read().split('\n')
            for line in content1:
                for k in match_str:
                    if k in line:
                        filtered.append(line)
                        break
        except KeyError:
            filtered = []
    f = tar.extractfile('testbed/os-test.log')
    content = f.read().split('\n')
    for line in content:
        for k in match_str:
           if k in line:
              filtered.append(line)
              break;
#print filtered
    tar.close()
    return filtered
def gen_timestamp(content):
    d = {
         'nimbus_deploy':  'Start to provision infrastructure',
         'vio_ovf_deploy': 'Start to deploy management server',
         'vio_deploy':     'Start to create OpenStack Cluster',
         'keystone': 'Start to run keystone',
         'glance':   'Start to run glance',
         'nova':     'Start to run nova',
         'cinder':   'Start to run cinder',
         'neutron':  'Start to run neutron',
         'heat':     'Start to run heat',
         'scenario': 'Start to run scenario',
         'vmware':   'Start to run VMware tempest',
#       'nsxv':     'Start to run nsxv tests',
#         'build':'Opening OVA source:' 
    }

    timestamp = {}
    if len(content) < 5:
#        print "wrong build"
        return {}
    for line in content:
        if "Opening OVA source:" in line:
            build_num = line.split("Opening OVA source:")[-1].split("/")[-1]
            date = line.split("Opening OVA source:")[0].split(" ")[0]
            timestamp["build"] = build_num.split('_')[0].split('-')[2:]
            timestamp["date"] = date
#print timestamp['build']
            continue
        for k, v in six.iteritems(d):
            if v in line:
                key = k
                value = []
                value.append(line.split(",")[0])
                break
        if 'out: Ran' in line:
            value.append(line.split("out: Ran")[-1].split(" ")[-1])
            value.append(line.split("out: Ran")[-1].split(" ")[-4])
        if 'out: OK' in line:
            value.append("0")
            states = line.split("out: OK")[-1].split(",")
            for state in states:
                if "skipped" in state:
                    value.append(state.split('=')[1].strip(')'))
                else:
                    value.append("0")
        elif 'out: FAILED' in line:
            states = line.split("out: FAILED")[-1].split(",")
            for state in states:
                if "failures" in state:
                    value.append(state.split('=')[1].strip(')'))
                elif "skipped" in state:
                    value.append(state.split('=')[1].strip(')'))
                else:
                    value.append("0")
            if len(states) == 1:
                    value.append("0")
        timestamp[key] =  value
    timestamp['nimbus_deploy'].append(cal_exe_time(timestamp['vio_ovf_deploy'][0],timestamp['nimbus_deploy'][0]))
    timestamp['vio_ovf_deploy'].append(cal_exe_time(timestamp['vio_deploy'][0],timestamp['vio_ovf_deploy'][0]))
    timestamp['vio_deploy'].append(cal_exe_time(timestamp['keystone'][0],timestamp['vio_deploy'][0]))
    if 'neutron' not in timestamp.keys():
        timestamp['neutron']=["0","0","0","0","0"]
    return timestamp
def example():
    url_range = range(177,178)
    formal_label()
    for i in url_range:
        url = "http://p3-ci-int.eng.vmware.com/view/End%20to%20End/job/master-tempest-nsxv/{0}/artifact/testbed.tar.gz".format(i)
        content = gen_data_from_url(url)
        print content
        timestamp = gen_timestamp(content)
        print timestamp
        formal_data(timestamp)

def nsxv_ha():
    url_range = range(177,289)
    formal_label()
    for i in url_range:
        url = "http://p3-ci-int.eng.vmware.com/view/End%20to%20End/job/master-tempest-nsxv/{0}/artifact/testbed.tar.gz".format(i)
        content = gen_data_from_url(url)
        timestamp = gen_timestamp(content)
        formal_data(timestamp)
def dvs_ha():
    url_range = range(165,233)
    formal_label()
    for i in url_range:
        url = "http://p3-ci-int.eng.vmware.com/view/End%20to%20End/job/master-tempest-dvs/{0}/artifact/testbed.tar.gz".format(i)
        content = gen_data_from_url(url)
        timestamp = gen_timestamp(content)
        formal_data(timestamp)
def nsxv_compact():
    url_range = range(60,99)
    formal_label()
    for i in url_range:
        url = "http://p3-ci-int.eng.vmware.com/view/End%20to%20End/job/master-tempest-nsxv-singlevm/{0}/artifact/testbed.tar.gz".format(i)
        content = gen_data_from_url(url, True)
        timestamp = gen_timestamp(content)
        formal_data(timestamp)
def dvs_compact():
    url_range = range(1,37)
    formal_label()
    for i in url_range:
        url = "http://p3-ci-int.eng.vmware.com/view/End%20to%20End/job/master-tempest-dvs-singlevm/{0}/artifact/testbed.tar.gz".format(i)
        content = gen_data_from_url(url, True)
        timestamp = gen_timestamp(content)
        formal_data(timestamp)

def collect_all():
    print "Collecting trend for HA mode of nsxv tempest:\n"
    nsxv_ha()
    print "Collecting trend for compact mode of nsxv tempest:\n"
    nsxv_compact()
    print "Collecting trend for HA mode of dvs tempest:\n"
    dvs_ha()
    print "Collecting trend for compact mode of dvs tempest:\n"
    dvs_compact()
   
    
def main(argv):
# filename = argv[1]
    execution_time = {}
    example()
    collect_all()
    return
 
if __name__ == "__main__":
    main(sys.argv)
