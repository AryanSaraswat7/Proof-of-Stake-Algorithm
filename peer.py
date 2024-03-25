import asyncio
import argparse
import json

peers_list = [];



# Step 1: Parse Command Line Arguments
parser = argparse.ArgumentParser(description="Simple Asyncio P2P Peer")
parser.add_argument('--port', type=int, help="Port number to listen on")
parser.add_argument('--node', type=int, help="Node to send data to")
args = parser.parse_args()

# Step 2: Server Handler - Handles incoming data from peers
async def handle_peer(reader, writer):
    data = await reader.read(100)  # Read up to 100 bytes
    try:
        message = json.loads(data.decode())
        addr = writer.get_extra_info('peername')
        print(f"Received {message} from {addr}")

        # Debug prints to help verify the structure and types of the received message
        print(message)
        print(message.get('type'))
        print(message.get('code'))
        print(type(message.get('code')))

        # Handle different types of request from peers
        if message.get('type') == "request":
          
            
            if message.get('code') == "get_peers_list":
                await send_data('127.0.0.1','response','set_peers_list',peers_list,peers_list[0],message.get('from'))
            else:
                print("Unknown Request.")

        # handle different kind of response from peers
        if message.get("type") == "response":
            if message.get('code') == 'set_peers_list':
                print("Got peers list")
                peers_list.extend(message.get('data'))
                print("updating own peers list : " )
                print(peers_list)
                await notify_peers_on_list(message.get('data'))

        if message.get('type') == "notification":
            if message.get('code') == 'new_peer_addition':
                peers_list.append(message.get('data'))
                print("Updated Peers List " + json.dumps({"peers_list":peers_list}))

    except Exception as e:
        print("Unexpected error:", e)

    writer.close()

# Step 3: Sending Data to Peers
async def send_data(host, type, code ,data, from_port,to_port):
    message = {
        "type":type,
        "code":code,
        "data":data,
        "from":from_port,
        "to":to_port
    }
    print("[issue 4] : here inside send data")
    print(message);
    reader, writer = await asyncio.open_connection('127.0.0.1', to_port)
    print(f"Sending: {message}")
    writer.write(json.dumps(message).encode())

    writer.close()
    await writer.wait_closed()

# Function to get user input and send data asynchronously
async def send_data_to(address,node):
    while True:
        await asyncio.sleep(2)
        await send_data('127.0.0.1', node, json.dumps({"address":address}))

# Ask for peer list 
async def ask_peers_list(address,node):
    await send_data('127.0.0.1','request','get_peers_list','',address,node);
    # await send_data('127.0.0.1',node,json.dumps({"type":"request","code":"get_peers_list","address":address}));

# Notify all the peers about new peer node
async def notify_peers_on_list(list):
    for peer in list:
        print("Sending notification to : " + str(peer))
        await send_data(peer,'notification','new_peer_addition',peers_list[0],peers_list[0],peer)


async def consensus_algo():
    while True:
        await asyncio.sleep(2)
        print(str(peers_list[0]) + " : mining..." )


# Updated Step 4: Run both server and input/sending concurrently
async def main():
    # Update peer list with own port
    peers_list.append(args.port)

    # Start the server
    server = await asyncio.start_server(handle_peer, '127.0.0.1', args.port)
    addr = server.sockets[0].getsockname()
    print(f"Serving on {addr}")

    # Create a task for the server
    server_task = asyncio.create_task(server.serve_forever())

    # Create a task for mining and creating blocks 
    consensus_task  =asyncio.create_task(consensus_algo())
    
    # Create a task for sending data based on user input
    if(args.node):
        # input_task = asyncio.create_task(send_data_to(args.port,args.node))
        # await input_task
        discovery_task = asyncio.create_task(ask_peers_list(args.port,args.node))
        await discovery_task
    
    # Wait for both tasks to complete
    await consensus_task
    await server_task

# Run the asyncio event loop
asyncio.run(main())