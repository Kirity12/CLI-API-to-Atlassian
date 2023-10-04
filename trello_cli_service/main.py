"Main fuction of the CLI service"
import sys
import importlib.util
import typer
import os 

app = typer.Typer()

def welcome_message():
    "Simple welcome message and itro to The CLI sevice"

    intro = '''
            =============================================================================
                                    WELCOME TO TRELLO CLI API

            This CLI service does the following operations:

            1. Create a new card (with or without labels) for a given column in the board
            2. Create a new label separately (later can be added to a card)

            =============================================================================
            '''
    typer.echo(intro)


def import_trello_hard():
    "typer doesn't support import of external files and thus hard imports"

    module_path = str(os.path.join((os.path.dirname(os.path.realpath(__file__))), 'trello_api.py'))
    sys.path.append(str(os.path.dirname(os.path.realpath(__file__))))
    spec = importlib.util.spec_from_file_location(module_path, module_path)
    module = importlib.util.module_from_spec(spec)
    # HACK(dirty) : add local path to allow trello import
    spec.loader.exec_module(module)
    # Restore previous state
    sys.path.pop(-1)
    return module


def verify_user_credentials():
    "Take user authentication and verify to Trello connection"

    # Ask for the user's API key
    api_key = typer.prompt("Please enter your API key:")

    trello_module = import_trello_hard()

    trello = trello_module.TrelloApi(api_key)

    while True:
        # Check if the user has the required token
        has_token = typer.confirm("Do you have the required token for the read/write operation?")

        if not has_token:

            # Give options for actions: read or write
            action = get_read_write_action()

            # Provide the URL to create the token if not present
            typer.echo('Please create the token using the following link:\n')
            typer.echo(trello.get_token_url('temp',write_access=bool(action-1)))

        token: str = typer.prompt("\nPlease enter your token:")

        # Establish connection using the API key and token
        typer.echo(f"Verifying connection with API using API key: {api_key} and token: {token}")
        trello.set_token(token)

        status, _ = trello.get_boards()
        if status == 200:
            typer.echo("Connection verified. Status: 200")
            break
        else:
            typer.echo(f"Connection failed. Status: {status}")
            typer.echo(f"\nRe-enter the credentials")

    return trello

def get_read_write_action():
    "Action index if user wants to perform a read or write operation"

    while True:
        try:
            typer.echo("\nSelect an action for type of operation to be performed ([1-2]):")
            action: int = int(typer.prompt("1. Perform Read operation \n"
                                        "2. Perform Update/Add Operation\n\n"))
            if (1>action or action>=3):
                typer.echo('\nInvalid action')
            else:
                break
        except  ValueError or IndexError:
            typer.echo('\nInvalid action')
    return action


def get_boards(trello):
    "Display all boards as list accessible to user"

    status, response = trello.get_boards()

    if status == 200:
        typer.echo("\n\nBoards Available is/are::\n")
        boards_list = []

        for i, resp in enumerate(response):
            idx, name, bid = i+1, resp['name'], resp['id']
            typer.echo(f"{idx}. {name}")
            boards_list.append(bid)

    else:
        typer.echo(f"Connection failed. Status: {status}")
        sys.exit()

    return boards_list


def get_columns(trello, board):
    "Display all columns in the board"

    status, response = trello.get_columns(board)

    if status == 200:
        typer.echo("\nColumns available in this board is/are::\n")
        columns_list = []

        for i, resp in enumerate(response):
            idx, name, bid = i+1, resp['name'], resp['id']
            typer.echo(f"{idx}. {name}")
            columns_list.append(bid)

    else:
        typer.echo(f"Connection failed. Status: {status}")
        sys.exit()

    return columns_list


def get_cards(trello, board_id):
    "Display all cards in the board"

    status, response = trello.get_cards(board_id)
    #  Add columns name as well
    if status == 200:
        typer.echo("\nCards available in this board is/are::\n")
        cards_list = []

        for i, resp in enumerate(response):
            idx, name, bid = i+1, resp['name'], resp['id']
            typer.echo(f"{idx}. {name}")
            cards_list.append(bid)

    else:
        typer.echo(f"Connection failed. Status: {status}")
        sys.exit()

    return cards_list


def get_labels(trello, board_id):
    "Display all labels in the board"

    status, response = trello.get_labels(board_id)
    #  Add labels name as well
    if status == 200:
        typer.echo("\nLabels available in this board is/are::\n")
        labels_list = []

        for i, resp in enumerate(response):
            idx, name, bid, col = i+1, resp['name'], resp['id'], resp['color']
            typer.echo(f"{idx}. Name: {name if name else 'None'} | Color: {col}")
            labels_list.append(bid)


    else:
        typer.echo(f"Connection failed. Status: {status}")
        sys.exit()

    return labels_list


def add_card(trello, columns_id, board_id):
    "Process to take information about card and add it to appropriate board"

    name: str = typer.prompt("\nName of the card:")
    description: str = typer.prompt("\nDescription of the card:")
    id_list = get_selected_labels_list(trello, board_id)

    status, response = trello.add_card(name, columns_id, description, id_list)
    if status == 200:
        typer.echo("Card added successfuly. Status: 200")
    else:
        typer.echo(f"Connection failed. Status: {status}")
        sys.exit()

    return response


def get_selected_labels_list(trello, board_id):
    flag= True
    while flag:
        try: 
            all_labels = get_labels(trello, board_id)
            selected_labels = typer.prompt("\nWrite the indexes of all the labels "
                                        f"(separated by ',')[0-{len(all_labels)}]::")
            selected_labels = selected_labels.split(',')
            selected_labels = [int(label)-1 for label in selected_labels]
            for i, label in enumerate(selected_labels):
                selected_labels[i] = int(label)
                flag = flag and (0<=int(label)<=len(all_labels))

            flag = not flag
            if flag:
                typer.echo("\nInvalid label indexes. Re-enter indexes to continue")
        except  ValueError or IndexError:
            typer.echo("\nInvalid label indexes. Re-enter indexes to continue")

    if -1 in selected_labels:
        id_list = []
    else:
        id_list = [all_labels[i] for i in selected_labels]
    return id_list


def add_labels(trello, card_id, board_id):
    "Process to take information about label and add it to appropriate card"

    id_list = get_selected_labels_list(trello, board_id)

    resp = []
    for i, id_ in id_list:
        status, response = trello.add_label_to_card(card_id, id_)
        resp.append((status, response))
        if status == 200:
            typer.echo(f"label with index {i+1} added successfuly. Status: 200")
        else:
            typer.echo("Label already presen or connection "
                       "failed for label {i+1}. Status: {status}")
    return resp


def create_label(trello, board_id):
    "Process to take information to create a new label"

    name: str = typer.prompt("\nName of the card:")
    color: str = typer.prompt("\nColor of the card:")
    status, response = trello.create_label(name, color, board_id)
    if status == 200:
        typer.echo("Label added successfuly. Status: 200")
    else:
        typer.echo(f"Connection failed. Status: {status}")
        sys.exit(0)

    return response


def perform_tasks(trello):
    "Perform tasks based on options given to user"
    
    has_token = True

    while has_token:

        # Give options for task to be performed
        while True:
            try:
                typer.echo("\nSelect an action for type of operation to be performed ([1-7]):")
                action: int = int(typer.prompt("1. Add Cards\n2. Add Existing Labels to a Card\n"
                                            "3. Create New Labels in Board\n\n4. Get Boards\n"
                                            "5. Get Columns\n6. Get Cards\n7. Get Labels\n\n0. Exit"))
                if 1>action or action>=8:
                    typer.echo('\nInvalid action')
                else:
                    break
            except  ValueError or IndexError:
                typer.echo('\nInvalid action')

        if action==1:
            add_card_to_board(trello)

        elif action==2:
            add_label_existing_card(trello)

        elif action==3:
            add_new_label_to_board(trello)

        elif action==4:
            _ = get_boards(trello)

        elif action==5:
            display_columns_list(trello)

        elif action==6:
            display_cards_list(trello)

        elif action==7:
            display_labels_list(trello)

        elif action==0:
            pass

        else:
            typer.echo('Incorrect action')

        has_token = typer.confirm("\nDo you want to continue doing operations?")

        if not has_token:
            break


def display_labels_list(trello):
    "Display all labels in the current board"

    boards = get_boards(trello)
    while True:
        try:
            idx: int = int(typer.prompt(f"\nSelect the board ([1-{len(boards)}]):"))
            if 1>idx or idx>len(boards):
                typer.echo('Invalid input')
            else:
                break
        except  ValueError or IndexError:
            typer.echo('\nInvalid action')

    get_labels(trello, boards[idx-1])


def display_cards_list(trello):
    "Display all cards in the current board"

    boards = get_boards(trello)
    while True:
        try:
            idx: int = int(typer.prompt(f"\nSelect the board ([1-{len(boards)}]):"))
            if 1>idx or idx>len(boards):
                typer.echo('Invalid input')
            else:
                break
        except  ValueError or IndexError:
            typer.echo('\nInvalid action')

    get_cards(trello, boards[idx-1])


def display_columns_list(trello):
    "Display all columns in the current board"

    boards = get_boards(trello)
    while True:
        try:
            idx: int = int(typer.prompt(f"\nSelect the board ([1-{len(boards)}]):"))
            if 1>idx or idx>len(boards):
                typer.echo('Invalid input')
            else:
                break
        except  ValueError or IndexError:
            typer.echo('\nInvalid action')

    get_columns(trello, boards[idx-1])


def add_new_label_to_board(trello):
    "Adds new label to the board selected by the user"

    boards = get_boards(trello)
    while True:
        try:
            idx: int = int(typer.prompt(f"\nSelect the board ([1-{len(boards)}]):"))
            if 1>idx or idx>len(boards):
                typer.echo('Invalid input')
            else:
                break
        except  ValueError or IndexError:
            typer.echo('\nInvalid action')
    board_id = boards[idx-1]

    create_label(trello, board_id)


def add_label_existing_card(trello):
    "Adds existing label to the card selected by the user"

    boards = get_boards(trello)
    while True:
        try:
            idx: int = int(typer.prompt(f"\nSelect the board ([1-{len(boards)}]):"))
            if 1>idx or idx>len(boards):
                typer.echo('Invalid input')
            else:
                break
        except  ValueError or IndexError:
            typer.echo('\nInvalid action')
    board_id = boards[idx-1]

    cards = get_cards(trello, boards[idx-1])
    while True:
        try:
            idx: int = int(typer.prompt(f"\nSelect the Card ([1-{len(cards)}]):"))
            if 1>idx or idx>len(cards):
                typer.echo('Invalid input')
            else:
                break
        except  ValueError or IndexError:
            typer.echo('\nInvalid action')

    add_labels(trello, cards[idx-1], board_id)


def add_card_to_board(trello):
    "Adds new card to the board selected by the user"

    boards = get_boards(trello)
    while True:
        try:
            idx: int = int(typer.prompt(f"\nSelect the board ([1-{len(boards)}]):"))
            if 1>idx or idx>len(boards):
                typer.echo('Invalid input')
            else:
                break
        except  ValueError or IndexError:
            typer.echo('\nInvalid action')

    board_id = boards[idx-1]

    columns = get_columns(trello, board_id)
    while True:
        try:
            idx: int = int(typer.prompt(f"\nSelect the column ([1-{len(columns)}]):"))
            if 1>idx or idx>len(columns):
                typer.echo('Invalid input')
            else:
                break
        except  ValueError or IndexError:
            typer.echo('\nInvalid action')

    add_card(trello, columns[idx-1], board_id)


def goodbye_message():
    'API Exit function, prints out the  exit message Ctrl+c'
    typer.echo('Aborting...')


@app.command()
def main():
    '''
    This is CLI service does the following operations:

            1. Create a new card (with or without labels) for a given column in the board\n
            2. Create a new label separately (later can be added to a card)
    '''

    welcome_message()

    trello = verify_user_credentials()

    perform_tasks(trello)

    goodbye_message()


if __name__ == "__main__":

    app()
