import typer
from trello_api import TrelloApi

app = typer.Typer()

def welcome_message():
    intro = '''
            =============================================================================
                                    WELCOME TO TRELLO CLI API

            This CLI service does the following operations:

            1. Create a new card (with or without labels) for a given column in the board
            2. Create a new label separately (later can be added to a card)

            =============================================================================
            '''
    typer.echo(intro)


def establish_connection():
    # Step 2: Ask for the user's API key
    api_key: str = typer.prompt("Please enter your API key:")

    trello = TrelloApi(api_key)

    # Step 3: Check if the user has the required token
    has_token = typer.confirm("Do you have the required token for the read/write operation?")
    
    if not has_token:

        # Step 4: Give options for actions
        while True:
            typer.echo("\nSelect an action for type of operation to be performed ([1-2]):")
            action: int = int(typer.prompt("1. Perform Read operation \n2. Perform Update/Add Operation\n\n"))
            if 1<=action<3:
                break
            else:
                typer.echo('Invalid action')

        # Step 5: Provide the URL to create the token if not present
        typer.echo('Please create the token using the following link:\n')
        typer.echo(trello.get_token_url('temp',write_access=(True if action-1 else False)))

    token: str = typer.prompt("\nPlease enter your token:")
        
    # Step 6 : Establish connection using the API key and token
    typer.echo(f"Verifying connection with API using API key: {api_key} and token: {token}")
    trello.set_token(token)

    status, _ = trello.get_boards()
    if status == 200:
        typer.echo(f"Connection verified. Status: 200")
        return trello
    
    else:
        typer.echo(f"Connection failed. Status: {status}")
        quit()


def get_boards(trello: TrelloApi):
    status, response = trello.get_boards()

    if status == 200:
        typer.echo(f"\n\nBoards Available is/are::\n")
        boards_list = []

        for i, resp in enumerate(response):
            idx, name, bid = i+1, resp['name'], resp['id']
            typer.echo(f"{idx}. {name}")
            boards_list.append(bid)

        return boards_list

    else:
        typer.echo(f"Connection failed. Status: {status}")
        quit()


def get_columns(trello, board):
    status, response = trello.get_columns(board)

    if status == 200:
        typer.echo(f"\nColumns available in this board is/are::\n")
        columns_list = []

        for i, resp in enumerate(response):
            idx, name, bid = i+1, resp['name'], resp['id']
            typer.echo(f"{idx}. {name}")
            columns_list.append(bid)

        return columns_list

    else:
        typer.echo(f"Connection failed. Status: {status}")
        quit()


def get_cards(trello, board_id):
    status, response = trello.get_cards(board_id)
    #  Add columns name as well
    if status == 200:
        typer.echo(f"\nCards available in this board is/are::\n")
        cards_list = []

        for i, resp in enumerate(response):
            idx, name, bid = i+1, resp['name'], resp['id']
            typer.echo(f"{idx}. {name}")
            cards_list.append(bid)

        return cards_list

    else:
        typer.echo(f"Connection failed. Status: {status}")
        quit()


def get_labels(trello, board_id):
    status, response = trello.get_labels(board_id)
    #  Add labels name as well
    if status == 200:
        typer.echo(f"\nLabels available in this board is/are::\n")
        labels_list = []

        for i, resp in enumerate(response):
            idx, name, bid, col = i+1, resp['name'], resp['id'], resp['color']
            typer.echo(f"{idx}. Name: {name if name else 'None'} | Color: {col}")
            labels_list.append(bid)

        return labels_list

    else:
        typer.echo(f"Connection failed. Status: {status}")
        quit()


def add_card(trello, columns_id, board_id):

    name: str = typer.prompt(f"\nName of the card:")
    description: str = typer.prompt(f"\nDescription of the card:")
    flag= True
    while flag:
        all_labels = get_labels(trello, board_id)
        selected_labels = typer.prompt(f"\nWrite the indexes of all the labels (separated by ',')[0-{len(all_labels)}], 0 being None::")
        selected_labels = selected_labels.split(',')
        selected_labels = [int(label)-1 for label in selected_labels]
        for i, label in enumerate(selected_labels):
            selected_labels[i] = int(label)
            flag = flag and (0<=int(label)<=len(all_labels))

        flag = not flag
        if flag:
            typer.echo("Invalid label indexes. Re-enter indexes to continue")
    
    if -1 in selected_labels:
        id_list = []
    else:
        id_list = [all_labels[i] for i in selected_labels]

    status, response = trello.add_card(name, columns_id, description, id_list)
    if status == 200:
        typer.echo(f"Card added successfuly. Status: 200")
        return response
    else:
        typer.echo(f"Connection failed. Status: {status}")
        quit()


def add_labels(trello, card_id, board_id):
    flag= True
    while flag:
        all_labels = get_labels(trello, board_id)
        selected_labels = typer.prompt(f"Write the idx of all the labels (separated by ',')[0-{len(all_labels)}], 0 being None::")
        selected_labels = selected_labels.split(',')
        selected_labels = [int(label)-1 for label in selected_labels]
        for i, label in enumerate(selected_labels):
            selected_labels[i] = int(label)
            flag &= (0<=int(label)<=len(all_labels))

        flag = not flag
        if flag:
            typer.echo("Invalid label indexes. Re-enter indexes to continue")
    
    if -1 in selected_labels:
        id_list = []
    else:
        id_list = [(i, all_labels[i]) for i in selected_labels]
    
    resp = []
    for i, id_ in id_list:
        status, response = trello.add_label_to_card(card_id, id_)
        resp.append((status, response))
        if status == 200:
            typer.echo(f"label with {i+1} added successfuly. Status: 200")
            return response
        else:
            typer.echo(f"Label already presen or connection failed for label {i+1}. Status: {status}")
    return resp

def create_label(trello, board_id):
    name: str = typer.prompt(f"\nName of the card:")
    color: str = typer.prompt(f"\Color of the card:")
    status, response = trello.create_label(name, color, board_id)
    if status == 200:
        typer.echo(f"Label added successfuly. Status: 200")
        return response
    else:
        typer.echo(f"Connection failed. Status: {status}")
        quit()

def perform_tasks(trello: TrelloApi):

    # Step 7 : Give options for task to be performed
    while True:
        typer.echo("\nSelect an action for type of operation to be performed ([1-7]):")
        action: int = int(typer.prompt("1. Add Cards\n2. Add Existing Labels to a Card\n3. Create New Labels in Board\n"
                                       "4. Get Boards\n5. Get Columns\n6. Get Cards\n7. Get Labels\n\n"))
        if 1<=action<8:
            break
        else:
            typer.echo('Invalid action')
    
    if action==1:

        boards = get_boards(trello)
        while True:
            idx: int = int(typer.prompt(f"\nSelect the board ([1-{len(boards)}]):"))
            if 1<=idx<=len(boards):
                break
            else:
                typer.echo('Invalid input')
        board_id = boards[idx-1]
        
        columns = get_columns(trello, board_id)
        while True:
            idx: int = int(typer.prompt(f"\nSelect the column ([1-{len(columns)}]):"))
            if 1<=idx<=len(columns):
                break
            else:
                typer.echo('Invalid input')

        card_id = add_card(trello, columns[idx-1], board_id)
    
    elif action==2:
        boards = get_boards(trello)
        while True:
            idx: int = int(typer.prompt(f"\nSelect the board ([1-{len(boards)}]):"))
            if 1<=idx<=len(boards):
                break
            else:
                typer.echo('Invalid input')
        board_id = boards[idx-1]
        
        cards = get_cards(trello, boards[idx-1])
        while True:
            idx: int = int(typer.prompt(f"\nSelect the Card ([1-{len(cards)}]):"))
            if 1<=idx<=len(cards):
                break
            else:
                typer.echo('Invalid input')

        add_labels(trello, cards[idx-1], board_id)
    
    elif action==3:
        boards = get_boards(trello)
        while True:
            idx: int = int(typer.prompt(f"\nSelect the board ([1-{len(boards)}]):"))
            if 1<=idx<=len(boards):
                break
            else:
                typer.echo('Invalid input')
        board_id = boards[idx-1]
        
        label = create_label(trello, boards[idx-1])
    
    elif action==4:
        _ = get_boards(trello)
    
    elif action==5:
        boards = get_boards(trello)
        while True:
            idx: int = int(typer.prompt(f"\nSelect the board ([1-{len(boards)}]):"))
            if 1<=idx<=len(boards):
                break
            else:
                typer.echo('Invalid input')
        
        columns = get_columns(trello, boards[idx-1])

    elif action==6:
        boards = get_boards(trello)
        while True:
            idx: int = int(typer.prompt(f"\nSelect the board ([1-{len(boards)}]):"))
            if 1<=idx<=len(boards):
                break
            else:
                typer.echo('Invalid input')
        
        columns = get_cards(trello, boards[idx-1])

    else:
        boards = get_boards(trello)
        while True:
            idx: int = int(typer.prompt(f"\nSelect the board ([1-{len(boards)}]):"))
            if 1<=idx<=len(boards):
                break
            else:
                typer.echo('Invalid input')
        
        columns = get_labels(trello, boards[idx-1])

    has_token = typer.confirm("\nDo you to continue doing operations?")

    if has_token:
        perform_tasks(trello)


def goodbye_message():
    typer.echo('Aborting...')
      

@app.command()
def main():
        
    welcome_message()

    trello = establish_connection()

    perform_tasks(trello)

    goodbye_message()
    


if __name__ == "__main__":
    app()