import click
import os
import zipfile
from pipz.pipzlib import install_private_package, download_private_package, install_powershell_module, isAdmin, install_data
import subprocess
import sys
import getpass


def common_libs():
    os.system('pip install ipywidgets')
    os.system('pip install cufflinks')
    os.system('pip install git+https://github.com/altair-viz/jupyter_vega')
    os.system('conda install -y bokeh')


@click.group(invoke_without_command=True)
@click.option('--admin/--no-admin', default=False)
@click.option('--upgrade', default=False, is_flag=True)
@click.pass_context
def cli(ctx, admin, upgrade):
    if ctx.obj is None:
        ctx.obj = {}
    ctx.obj['admin'] = admin
    ctx.obj['upgrade'] = upgrade
    if admin and not isAdmin():
        raise Exception('Run the command with elevated priviledges.')

    nothing = True

    if upgrade:
        nothing = False
        subprocess.Popen('pip install --upgrade --no-cache --no-cache-dir pipz'.split())
        sys.exit(0)


@cli.command(name='install')
@click.argument('package')
@click.option('--secret', default=None)
@click.pass_context
def install(ctx, package, secret):
    if secret is None:
        secret = getpass.getpass()
    install_private_package(ctx, package, secret)


@cli.command(name='install-module')
@click.argument('package')
@click.option('--secret', default=None)
@click.pass_context
def install_module(ctx, package, secret):
    if secret is None:
        secret = getpass.getpass()
    install_powershell_module(ctx, package, secret)

@cli.command(name='install-data')
@click.option('--package', default=None)
@click.option('--location', default='localdata')
@click.pass_context
def install_module(ctx, package, location):
    install_data(ctx, package, location)

@cli.command(name='install-requirements')
@click.argument('package')
@click.pass_context
def install_requirements(ctx, package):
    pipz_path = os.path.dirname(os.path.dirname(__import__('pipz').__file__))
    file = os.path.join(pipz_path, package, 'z-requirements.py')
    if not os.path.exists(file):
        return
    if os.path.exists(file):
        with open(file) as fp:
            for cnt, line in enumerate(fp):
                line = line[1:].strip()
                if line.startswith('run '):
                    ll = line[len('run '):]
                    os.system(ll)
                    continue

                if line.startswith('winrun ') and (sys.platform == "win32"):
                    ll = line[len('winrun '):]
                    os.system(ll)
                    continue

                if line.startswith('linrun ') and (sys.platform != "win32"):
                    ll = line[len('linrun '):]
                    os.system(ll)
                    continue


                if len(line) == 0 or line.startswith('#') or line.startswith(';'):
                    continue
                try:
                    package, secret = [x.strip() for x in line.split('--secret')]

                    if package.startswith('module:'):
                        module = package[len('module:'):].strip()
                        install_powershell_module(ctx, module, secret)
                    else:
                        install_private_package(ctx, package, secret)
                except Exception as e:
                    print("Error installing: {}".format(line))
                    print(e)
        return

    print('{} does not exist.'.format(file))


@cli.command(name='uninstall')
@click.argument('package')
@click.pass_context
def uninstall(ctx, package):
    os.system('pip uninstall {}'.format(package))


@cli.command(name='download')
@click.argument('package')
@click.option('--secret', default=None)
@click.option('--unzip', default=False)
@click.pass_context
def download(ctx, package, secret, unzip):
    if secret is None:
        secret = getpass.getpass()
    download_private_package(ctx, package, secret)
    if unzip:
        print('Unzip is not supported your. Please unzip the file manually')

@cli.command(name='ps')
@click.option('--str', default='')
@click.option('--process', default='')
@click.option('--down', default=False, is_flag=True)
@click.pass_context
def ps(ctx, str, process, down):
    cmd = 'powershell "Get-WmiObject -Class Win32_process'
    if process:
        cmd += '| ? {$_.Name -eq \'' + process + '\'}  '

    if str:
        cmd += '| ?{$_.CommandLine -like \'*' + str + '*\'} '

    cmd += '| ?{-not ($_.CommandLine  -like \'*get-wimobject*\')}| ?{-not ($_.CommandLine  -like \'*pipz  ps*\')}| ?{-not ($_.CommandLine  -like \'*pipz.exe*\')}|select processid, commandline'

    os.system(cmd)

    if down:
        os.system(cmd + '|foreach {stop-Process  -ID $_.ProcessId}')


if __name__ == '__main__':
    cli(obj={'ok':1})
