__author__ = 'Student'
import djclick as click
import requests
from requests.auth import HTTPBasicAuth
@click.command()
def login():
    click.echo('oh god please work')
    user = ''
    password = ''
    #requests.get('https://whatever', auth=HTTPBasicAuth(user, password))


login()
