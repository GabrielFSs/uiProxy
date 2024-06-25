import asyncio
import websockets

async def proxy_handler(client_ws, path):
    # Determina a URI do servidor com base no caminho
    if path == "/ui/1":
        server_uri = 'ws://localhost:1880/ui/1'
    elif path == "/ui/2":
        server_uri = 'ws://localhost:1880/ui/2'
    else:
        print(f"Caminho não suportado: {path}")
        await client_ws.close()
        return

    # Conecta-se ao servidor WebSocket real
    async with websockets.connect(server_uri) as server_ws:
        # Função para encaminhar mensagens do cliente para o servidor
        async def forward_client_to_server():
            async for message in client_ws:
                print(f"Cliente para servidor ({path}): {message}")
                await server_ws.send(message)

        # Função para encaminhar mensagens do servidor para o cliente
        async def forward_server_to_client():
            async for message in server_ws:
                print(f"Servidor para cliente ({path}): {message}")
                await client_ws.send(message)

        # Executa ambas as funções simultaneamente
        await asyncio.gather(forward_client_to_server(), forward_server_to_client())

async def start_proxy():
    print("Iniciando proxy em ws://localhost:9090")
    async with websockets.serve(proxy_handler, 'localhost', 9090):
        await asyncio.Future()  # Mantém o servidor rodando

asyncio.r
