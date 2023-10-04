from typer.testing import CliRunner
import sys
import os
import pytest
import typer
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import trello_cli_service.main as main
from trello_cli_service.trello_api import TrelloApi


runner = CliRunner()

API_KEY = "26dea0c6d8f4574827f3e06654ab5102"
TOKEN_KEY = "ATTA0c9670fe99c679e661aeef28cd9275b160270a70dff5e00fc4cd516fe1f321ef059D598F"


def mock_perform_tasks():
    main.perform_tasks(TrelloApi(API_KEY, TOKEN_KEY))


def test_welcome_message():

    app = typer.Typer()
    app.command()(main.welcome_message) 

    result = runner.invoke(app)

    assert result.exit_code == 0
    assert "WELCOME TO TRELLO CLI API" in result.stdout


def test_varify_credentials_known():

    app = typer.Typer()
    app.command()(main.verify_user_credentials)

    result = runner.invoke(app, input='\n'.join([API_KEY, 'y', TOKEN_KEY]))

    assert result.exit_code == 0
    assert "Status: 200" in result.stdout


def test_varify_credentials_unkown_read():

    app = typer.Typer()
    app.command()(main.verify_user_credentials)

    result = runner.invoke(app, input='\n'.join([API_KEY, 'n', '1', TOKEN_KEY]))

    assert result.exit_code == 0
    assert ("Please create the token" in result.stdout) 
    assert ("scope=read" in result.stdout) 
    assert ("Status: 200" in result.stdout)


def test_varify_credentials_unkown_write():

    app = typer.Typer()
    app.command()(main.verify_user_credentials)

    result = runner.invoke(app, input='\n'.join([API_KEY, 'n', '2', TOKEN_KEY]))

    assert result.exit_code == 0
    assert ("Please create the token" in result.stdout) 
    assert ("scope=read,write" in result.stdout) 
    assert ("Status: 200" in result.stdout)


def test_display_tasks():

    app = typer.Typer()
    app.command()(mock_perform_tasks)

    result = runner.invoke(app, input='\n'.join(['4', 'n']))
    print(result.stdout)
    assert 1==2
    assert ("action for type of operation to be performed ([1-7])" in result.stdout) 

def test_task_display_columns():

    app = typer.Typer()
    app.command()(mock_perform_tasks)

    result = runner.invoke(app, input='\n'.join(['5', '1', 'n']))
    print(result.stdout)

    assert ("action for type of operation to be performed ([1-7])" in result.stdout) 
    assert ("Boards Available is/are:" in result.stdout)
    assert ("Columns available in this board" in result.stdout)
