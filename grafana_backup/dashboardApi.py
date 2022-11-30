import re
import json
import requests
import sys
from grafana_backup.commons import log_response, to_python2_and_3_compatible_string


def health_check(grafana_url, http_get_headers, verify_ssl, client_cert, debug):
    url = '{0}/api/health'.format(grafana_url)
    print("\n[Pre-Check] grafana health check: {0}".format(url))
    return send_grafana_get(url, http_get_headers, verify_ssl, client_cert, debug)


def auth_check(grafana_url, http_get_headers, verify_ssl, client_cert, debug):
    url = '{0}/api/auth/keys'.format(grafana_url)
    print("\n[Pre-Check] grafana auth check: {0}".format(url))
    return send_grafana_get(url, http_get_headers, verify_ssl, client_cert, debug)



def search_dashboard(page, limit, grafana_url, http_get_headers, verify_ssl, client_cert, debug):
    url = '{0}/api/search/?type=dash-db&limit={1}&page={2}'.format(grafana_url, limit, page)
    print("search dashboard in grafana: {0}".format(url))
    return send_grafana_get(url, http_get_headers, verify_ssl, client_cert, debug)


def get_dashboard(board_uri, grafana_url, http_get_headers, verify_ssl, client_cert, debug):
    url = '{0}/api/dashboards/{1}'.format(grafana_url, board_uri)
    print("query dashboard uri: {0}".format(url))
    (status_code, content) = send_grafana_get(url, http_get_headers, verify_ssl, client_cert, debug)
    return (status_code, content)


def search_annotations(grafana_url, ts_from, ts_to, http_get_headers, verify_ssl, client_cert, debug):
    # there is two types of annotations
    # annotation: are user created, custom ones and can be managed via the api
    # alert: are created by Grafana itself, can NOT be managed by the api
    url = '{0}/api/annotations?type=annotation&limit=5000&from={1}&to={2}'.format(grafana_url, ts_from, ts_to)
    (status_code, content) = send_grafana_get(url, http_get_headers, verify_ssl, client_cert, debug)
    return (status_code, content)



def search_alert_channels(grafana_url, http_get_headers, verify_ssl, client_cert, debug):
    url = '{0}/api/alert-notifications'.format(grafana_url)
    print("search alert channels in grafana: {0}".format(url))
    return send_grafana_get(url, http_get_headers, verify_ssl, client_cert, debug)


def create_alert_channel(payload, grafana_url, http_post_headers, verify_ssl, client_cert, debug):
    return send_grafana_post('{0}/api/alert-notifications'.format(grafana_url), payload, http_post_headers, verify_ssl,
                             client_cert, debug)


def search_alerts(grafana_url, http_get_headers, verify_ssl, client_cert, debug):
    url = '{0}/api/alerts'.format(grafana_url)
    (status_code, content) = send_grafana_get(url, http_get_headers, verify_ssl, client_cert, debug)
    return (status_code, content)


def search_datasource(grafana_url, http_get_headers, verify_ssl, client_cert, debug):
    print("search datasources in grafana:")
    return send_grafana_get('{0}/api/datasources'.format(grafana_url), http_get_headers, verify_ssl, client_cert, debug)


def search_snapshot(grafana_url, http_get_headers, verify_ssl, client_cert, debug):
    print("search snapshots in grafana:")
    return send_grafana_get('{0}/api/dashboard/snapshots'.format(grafana_url), http_get_headers, verify_ssl, client_cert, debug)


def get_snapshot(key, grafana_url, http_get_headers, verify_ssl, client_cert, debug):
    url = '{0}/api/snapshots/{1}'.format(grafana_url, key)
    (status_code, content) = send_grafana_get(url, http_get_headers, verify_ssl, client_cert, debug)
    return (status_code, content)

def search_folders(grafana_url, http_get_headers, verify_ssl, client_cert, debug):
    print("search folder in grafana:")
    return send_grafana_get('{0}/api/search/?type=dash-folder'.format(grafana_url), http_get_headers, verify_ssl,
                            client_cert, debug)


def get_folder(uid, grafana_url, http_get_headers, verify_ssl, client_cert, debug):
    (status_code, content) = send_grafana_get('{0}/api/folders/{1}'.format(grafana_url, uid), http_get_headers,
                                              verify_ssl, client_cert, debug)
    print("query folder:{0}, status:{1}".format(uid, status_code))
    return (status_code, content)


def get_folder_permissions(uid, grafana_url, http_get_headers, verify_ssl, client_cert, debug):
    (status_code, content) = send_grafana_get('{0}/api/folders/{1}/permissions'.format(grafana_url, uid), http_get_headers,
                                              verify_ssl, client_cert, debug)
    print("query folder permissions:{0}, status:{1}".format(uid, status_code))
    return (status_code, content)


def get_dashboard_versions(dashboard_id, grafana_url, http_get_headers, verify_ssl, client_cert, debug):
    (status_code, content) = send_grafana_get('{0}/api/dashboards/id/{1}/versions'.format(grafana_url, dashboard_id), http_get_headers,
                                              verify_ssl, client_cert, debug)
    print("query dashboard versions: {0}, status: {1}".format(dashboard_id, status_code))
    return (status_code, content)


def get_version(dashboard_id, version_number, grafana_url, http_get_headers, verify_ssl, client_cert, debug):
    (status_code, content) = send_grafana_get('{0}/api/dashboards/id/{1}/versions/{2}'.format(grafana_url, dashboard_id, version_number), http_get_headers,
                                              verify_ssl, client_cert, debug)
    print("query dashboard {0} version {1}, status: {2}".format(dashboard_id, version_number, status_code))
    return (status_code, content)


def search_orgs(grafana_url, http_get_headers, verify_ssl, client_cert, debug):
    return send_grafana_get('{0}/api/orgs'.format(grafana_url), http_get_headers, verify_ssl,
                            client_cert, debug)


def get_org(id, grafana_url, http_get_headers, verify_ssl=False, client_cert=None, debug=True):
    return send_grafana_get('{0}/api/orgs/{1}'.format(grafana_url, id),
                            http_get_headers, verify_ssl, client_cert, debug)


def search_users(page, limit, grafana_url, http_get_headers, verify_ssl, client_cert, debug):
    return send_grafana_get('{0}/api/users?perpage={1}&page={2}'.format(grafana_url, limit, page),
                            http_get_headers, verify_ssl, client_cert, debug)


def get_users(grafana_url, http_get_headers, verify_ssl, client_cert, debug):
    return send_grafana_get('{0}/api/org/users'.format(grafana_url), http_get_headers, verify_ssl, client_cert, debug)



def get_user(id, grafana_url, http_get_headers, verify_ssl=False, client_cert=None, debug=True):
    return send_grafana_get('{0}/api/users/{1}'.format(grafana_url, id),
                            http_get_headers, verify_ssl, client_cert, debug)


def get_user_org(id, grafana_url, http_get_headers, verify_ssl=False, client_cert=None, debug=True):
    return send_grafana_get('{0}/api/users/{1}/orgs'.format(grafana_url, id),
                            http_get_headers, verify_ssl, client_cert, debug)



def send_grafana_get(url, http_get_headers, verify_ssl, client_cert, debug):
    r = requests.get(url, headers=http_get_headers, verify=verify_ssl, cert=client_cert)
    if debug:
        log_response(r)
    return (r.status_code, r.json())
