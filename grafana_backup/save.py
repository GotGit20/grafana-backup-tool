from grafana_backup.api_checks import main as api_checks
from grafana_backup.save_dashboards import main as save_dashboards
from grafana_backup.save_datasources import main as save_datasources
from grafana_backup.save_folders import main as save_folders
from grafana_backup.save_alert_channels import main as save_alert_channels
from grafana_backup.save_snapshots import main as save_snapshots
from grafana_backup.save_versions import main as save_versions
from grafana_backup.save_annotations import main as save_annotations
from grafana_backup.archive import main as archive
from grafana_backup.save_orgs import main as save_orgs
from grafana_backup.save_users import main as save_users
from grafana_backup.gcs_upload import main as gcs_upload
from grafana_backup.loggingmod import logger
import sys


def main(args, settings):
    arg_components = args.get('--components', False)
    arg_no_archive = args.get('--no-archive', False)

    backup_functions = {'dashboards': save_dashboards,
                        'datasources': save_datasources,
                        'folders': save_folders,
                        'alert-channels': save_alert_channels,
                        'organizations': save_orgs,
                        'users': save_users,
                        'snapshots': save_snapshots,
                        'versions': save_versions,
                        'annotations': save_annotations}

    (status, json_resp) = api_checks(settings)

    # Do not continue if API is unavailable or token is not valid
    if not status == 200:
        logger.error("server status is not ok: {0}".format(json_resp))
        sys.exit(1)


    if arg_components:
        arg_components_list = arg_components.replace("_", "-").split(',')

        # Backup only the components that provided via an argument
        for backup_function in arg_components_list:
            backup_functions[backup_function](args, settings)
    else:
        # Backup every component
        for backup_function in backup_functions.keys():
            backup_functions[backup_function](args, settings)

    gcs_bucket_name = settings.get('GCS_BUCKET_NAME')

    if not arg_no_archive:
        archive(args, settings)

    if gcs_bucket_name:
        logger.info('Upload archives to GCS:')
        gcs_upload(args, settings)
