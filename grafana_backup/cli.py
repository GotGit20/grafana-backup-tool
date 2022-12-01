from grafana_backup.constants import (PKG_NAME, PKG_VERSION, JSON_CONFIG_PATH)
from grafana_backup.save import main as save
from grafana_backup.grafanaSettings import main as conf
from docopt import docopt
import os
import sys
import time
import elasticapm


docstring = """
{0} {1}

Usage:
    grafana-backup save [--config=<filename>] [--components=<>] [--no-archive]
    grafana-backup restore [--config=<filename>] [--components=<>] <archive_file>
    grafana-backup delete [--config=<filename>] [--components=<>]
    grafana-backup tools [-h | --help] [--config=<filename>] [<optional-command>] [<optional-argument>]
    grafana-backup [--config=<filename>]
    grafana-backup [-h | --help]
    grafana-backup --version

Options:
    -h --help                               Show this help message and exit
    --version                               Get version information and exit
    --config=<filename>                     Override default configuration path
    --components=<>                         Comma separated list of individual components to backup (all by default); versions can only be saved not restored.
                                            <folders,folder_permissions,dashboards,datasources,alert-channels,organizations,users,snapshots,versions,annotations>

    --no-archive                            Skip archive creation and do not delete unarchived files
                                            (used for troubleshooting purposes)
""".format(PKG_NAME, PKG_VERSION)


args = docopt(docstring, help=False,
              version='{0} {1}'.format(PKG_NAME, PKG_VERSION))


def main():
    arg_config = args.get('--config', False)
    default_config = '{0}/conf/grafanaSettings.json'.format(
        os.path.dirname(__file__))

    if arg_config:
        settings = conf(arg_config)
    elif os.path.isfile(JSON_CONFIG_PATH):
        settings = conf(JSON_CONFIG_PATH)
    elif os.path.isfile(default_config):
        settings = conf(default_config)

    if args.get('save', None):
        client = elasticapm.Client(service_name="grafana-backup-tool", server_url="https://34.72.203.226:8200")
        elasticapm.instrument()
        time.sleep(60)
        client.begin_transaction(transaction_type="custom_script")
        save(args, settings)
        time.sleep(10)
        f = open("/opt/grafana-backup-tool/logs/done", "a")
        f.write("Cronjob done")
        f.close()
        client.end_transaction(name="backup", result="success")
        sys.exit()
    elif args.get('--help', None):
        print(docstring)
        sys.exit()
    else:
        print(docstring)
        sys.exit()


if __name__ == '__main__':
    main()
