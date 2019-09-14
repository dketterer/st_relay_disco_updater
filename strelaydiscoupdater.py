import argparse
import json
import os
import tarfile
import traceback

from urllib.request import Request, urlopen, urlretrieve
from email.mime.text import MIMEText
from subprocess import Popen, PIPE

LOG_ERRORS_TO_MAIL = True
MAIL_TO = 'mail@example.org'
MAIL_FROM = 'mail@example.org'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('api_url', type=str)
    parser.add_argument('executable', type=str)
    parser.add_argument('--target_dir', type=str, default='/usr/local/bin')

    return parser.parse_args()


def log_error_and_exit(e: Exception, args):
    if LOG_ERRORS_TO_MAIL:
        error_string = traceback.format_exc()
        msg = MIMEText("While upgrading %s occurred an Error.\n\n"
                       "Calling arguments:\n"
                       "%s\n\n"
                       "%s" % (args.executable, str(args), error_string))
        msg["From"] = MAIL_FROM
        msg["To"] = MAIL_TO
        msg["Subject"] = "Error upgrading %s" % args.executable
        p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
        p.communicate(msg.as_bytes())
    exit(1)


if __name__ == '__main__':
    args = parse_args()
    tar_url = ''
    asset_url = ''
    name = ''
    try:
        base_req = Request(args.api_url, headers={
            'Accept': 'application/vnd.github.v3+json'})
        base_data = json.loads(urlopen(base_req).read().decode())
        assets_req = Request(base_data['assets_url'], headers={
            'Accept': 'application/vnd.github.v3+json'})
        assets_data = json.loads(urlopen(assets_req).read().decode())
        for dic in assets_data:
            if 'linux-amd64' in dic['name']:
                asset_url = dic['url']
                name = dic['name']
        linux_asset_req = Request(asset_url, headers={
            'Accept': 'application/vnd.github.v3+json'})
        linux_asset_data = json.loads(urlopen(linux_asset_req).read().decode())
        tar_url = linux_asset_data['browser_download_url']

        urlretrieve(tar_url, '/tmp/%s' % name)

        tarball = tarfile.open('/tmp/%s' % name, 'r:gz')
        path_in_tar = ''
        for entry in tarball.getnames():
            if entry.endswith(args.executable):
                path_in_tar = entry
        reader = tarball.extractfile(path_in_tar)
        bytes = reader.read()
        with open(os.path.join(args.target_dir, args.executable), 'wb+') as exe_file:
            exe_file.write(bytes)

        os.chmod(os.path.join(args.target_dir, args.executable), 0o755)
        os.remove('/tmp/%s' % name)

    except Exception as e:
        log_error_and_exit(e, args)
