# Trello CLI API

This Command Line Interface (CLI) tool allows you to interact with Trello boards, cards, labels, and columns. You can create new cards, add labels to cards, create new labels, and perform various other operations on your Trello boards, all from the command line.

## Features

- Create new cards on Trello boards.
- Add labels to cards.
- Create new labels in a Trello board.
- Retrieve information about boards, columns, cards, and labels.
- Perform read and write operations on Trello boards.

## Getting Started

To get started with the Trello CLI, follow these steps:

1. Navigate to the project directory

### Installation

2. I've created a Python CLI project using the Poetry dependency management tool and the Typer library for building the CLI interface. Open the terminal in the current directory and command:

        ~ pip install dist\trello_cli_service-0.1.0-py3-none-any.whl

    Also install requirements.txt (for backup):

        ~ pip install requirements.txt

### Execution

3. Execute the command

        ~ trello_cli_service

    Follow the on-screen prompts to select actions and perform operations on your Trello boards.

## Backup Option to run the service

Just incase the wheel is not istalled properly or the service is not working, we can still use the service
just by running the python command on terminal. 

    ~ python trello_cli_service\main.py

## Configuration

Obtain your Trello API key by visiting Trello Developer API Keys and following the instructions.
TO create a new API key, first create an account at Trello and the create a new API key at: https://trello.com/power-ups/admin

You'll also need a token for read and write access to your Trello account. The CLI tool will guide you on how to generate this token.

## Example Usage

Once the user is verifed, the following operations can be performed:

### To add a new card to a Trello board, follow these steps:
To add a new card to a Trello board, follow these steps:

1. Select the index for "Add Cards" i.e 1 (is int type).
2. Choose the index of board where you want to add the card. Example: 1 or 2... (is int type).
3. Select the column where you want to add the card. Example: 1 or 2... (is int type).
4. Provide a name and description for the card.
5. Choose labels (if any) to add to the card.

### Adding a Label to a Card
To add an existing label to a card, follow these steps:

1. Select the index for "Add Existing Labels to a Card" i.e 2 (is int type).
2. Choose the index of board where you want to add the label. Example: 1 or 2... (is int type).
3. Choose the index of card where you want to add the label. Example: 1 or 2... (is int type).
4. Similarly choose the labels to add to the card.

### Add Existing Labels to a Card
To add an existing label to a card, follow these steps:

1. Select the index for "Add Existing Labels to a Card" i.e 2 (is int type).
2. Choose the index of board where you want to add the label. Example: 1 or 2... (is int type).
3. Choose the index of card where you want to add the label. Example: 1 or 2... (is int type).
4. Similarly choose the labels to add to the card.

### Create New Labels in Board
To add an existing label to a card, follow these steps:

1. Select the index for "Create New Labels in Board" i.e 3 (is int type).
2. Choose the index of board where you want to add the label. Example: 1 or 2... (is int type).
3. Provide a name and color for the label.

### Get the list of Boards, Columns, Cards and Labels
To display the contents of the board, follow these steps:

1. Select the index for "Get Boards" i.e 4 (is int type).
2. Select the index for "Get Columns", "Get Cards" and "Get Labels" for a given board, i.e 5, 6, 7 respectively.