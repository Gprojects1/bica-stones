from fastapi import FastAPI, HTTPException
import logging
import httpx
from typing import Optional, Dict, List
from agent_service import neural_network as n

agents: Dict[int, "Agent"] = {}
count: int = 0
class Agent:
    def __init__(self, agent_id: int, api_url: str):
        global count
        self.agent_id = agent_id
        self.api_url = api_url
        self.client = httpx.AsyncClient()
        self.neural_network = n.AgentTG(count, 'agent_service/10_stone.pth')
        count += 1

    async def get_lobby_ids(self) -> Optional[List[int]]:
        try:
            response = await self.client.get(f"{self.api_url}/get_lobby_ids/")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logging.error(f"Error getting lobby IDs: {e.response.text}")
            return None

    async def enter_lobby(self, lobby_id: int):
        try:
            response = await self.client.post(
                f"{self.api_url}/enter_lobby/?lobby_id={lobby_id}&agent_id={self.agent_id}"  # Параметры в query string
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logging.error(f"Error entering lobby: {e.response.text}")
            return None

    async def leave_lobby(self) -> Optional[dict]:
        try:
            response = await self.client.post(
                f"{self.api_url}/game/leave_lobby/",
                json={"agent_id": self.agent_id}
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logging.error(f"Error leaving lobby: {e.response.text}")
            return None

    async def get_game_info(self) -> Optional[dict]:
        try:
            response = await self.client.get(
                f"{self.api_url}/game/get_game_info/",
                params={"agent_id": self.agent_id}
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logging.error(f"Error getting game info: {e.response.text}")
            return None

    async def pick_stone(self, stone: int) -> Optional[dict]:
        try:
            response = await self.client.post(
                f"{self.api_url}/game/pick_stone/",
                params={"agent_id": self.agent_id, "stone": stone},
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logging.error(f"Error picking stone: {e.response.text}")
            return None

    async def wait_round_start(self, timeout: int = 600) -> Optional[dict]:
        try:
            response = await self.client.get(
                f"{self.api_url}/game/wait_round_start/",
                params={"agent_id": self.agent_id, "timeout": timeout}
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logging.error(f"Error waiting for round start: {e.response.text}")
            return None

    async def close(self):
        await self.client.aclose()
