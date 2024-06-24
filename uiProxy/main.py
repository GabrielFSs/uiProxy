import asyncio
import websockets

async def proxy_handler(client_ws, path):
    # Conecta-se ao servidor WebSocket real
    async with websockets.connect('ws://localhost:1880/ui1') as server_ws:
        # Função para encaminhar mensagens do cliente para o servidor
        async def forward_client_to_server():
            async for message in client_ws:
                print(f"Cliente para servidor: {message}")
                await server_ws.send(message)

        # Função para encaminhar mensagens do servidor para o cliente
        async def forward_server_to_client():
            async for message in server_ws:
                print(f"Servidor para cliente: {message}")
                await client_ws.send(message)

        # Executa ambas as funções simultaneamente
        await asyncio.gather(forward_client_to_server(), forward_server_to_client())

async def start_proxy():
    print("Iniciando proxy em ws://localhost:9090/ui1")
    async with websockets.serve(proxy_handler, 'localhost', 9090):
        await asyncio.Future()  # Mantém o servidor rodando

asyncio.run(start_proxy())
