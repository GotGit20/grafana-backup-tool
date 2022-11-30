from grafana_backup.commons import print_horizontal_line
from grafana_backup.dashboardApi import health_check, auth_check


def main(settings):
    grafana_url = settings.get('GRAFANA_URL')
    http_get_headers = settings.get('HTTP_GET_HEADERS')
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    debug = settings.get('DEBUG')
    api_health_check = settings.get('API_HEALTH_CHECK')

    if api_health_check:
        (status, json_resp) = health_check(grafana_url, http_get_headers, verify_ssl, client_cert, debug)
        if not status == 200:
            return (status, json_resp, None, None, None)

    (status, json_resp) = auth_check(grafana_url, http_get_headers, verify_ssl, client_cert, debug)
    if not status == 200:
        return (status, json_resp, None, None, None)


    print_horizontal_line()
    if status == 200:
        print("[Pre-Check] Server status is 'OK' !!")
    else:
        print("[Pre-Check] Server status is NOT OK !!: {0}".format(json_resp))
    print_horizontal_line()

    return (status, json_resp)
