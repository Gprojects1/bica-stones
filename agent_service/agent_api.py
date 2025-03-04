from fastapi import FastAPI, HTTPException
import logging
import asyncio
from agent_service import agent
from agent_service import start_loop
app = FastAPI()

@app.post("/agent/move_info/")
async def get_game_info(agent_id: int, move_data: dict[int, tuple[bool, list[int]]]):
    if agent_id not in agent.agents:
        raise HTTPException(status_code=404, detail="Agent not found")

    agent = agent.agents[agent_id]
    logging.info(f"Received move data for agent {agent_id}: {move_data}")

    stone_to_pick = agent.neural_network.choose_stone(move_data)
    await agent.pick_stone(stone_to_pick)

    return {"status": "success", "data": move_data}

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_loop.user_interface())

@app.on_event("shutdown")
async def shutdown_event():
    for agent in agent.agents.values():
        await agent.close()