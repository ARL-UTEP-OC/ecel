import cmd
import sys
import os
import signal
import argparse
import ecel_service
from engine.engine import Engine
from logging.handlers import SysLogHandler

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Command line util for ECEL")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--start", action="store_true",
                        help= "Start a specific collector")
    group.add_argument("--stop", action="store_true",
                        help= "Stop a specific collector")
    group.add_argument("--status", action="store_true",
                        help= "View the status a specific collector")
    group.add_argument("--list", action="store_true",
                        help= "List all available Collectors")

    parser.add_argument("--collector","--c", type=str, help="ECEL collector")
    args = parser.parse_args()

    if args.list:
        engine = Engine()
        collectors = engine.get_all_collectors()
        print "[+] Available collectors are: "
        for i, collector in enumerate(collectors):
            print "%d) %s" % (i, collector.name)
    else:
        service_name = "ecel_service_"+args.collector
        service = ecel_service.ecel_Service(service_name, pid_dir='/tmp')
        if args.start:
                print "[+]Starting Collector"
                service.start()
        elif args.status:
            if service.is_running():
                print "[+] Service is running..."
            else:
                print "[-] Service is not running..."
        elif args.stop:
            print "[-] Stopping Service"
            service.stop()
    os._exit(0)
