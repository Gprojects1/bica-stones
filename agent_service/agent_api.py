from fastapi import FastAPI, HTTPException, Query, Body
import logging
import asyncio
import agent_service.agent 
from agent_service import start_loop
from typing import Dict, Tuple, List
app = FastAPI()

def transform_move_data(move_dict: Dict[str, Tuple[bool, List[str]]]) -> Dict[int, Tuple[bool, List[int]]]:

    """
    Преобразует move_data из Dict[str, Tuple[bool, List[str]]] в Dict[int, Tuple[bool, List[int]]].

    Ключи (строки, представляющие числа) преобразуются в int.
    Строки в списках (A, B, C, ...) преобразуются в int (A -> 0, B -> 1, ...).
    """

    transformed_data: Dict[int, Tuple[bool, List[int]]] = {}
    for key, value in move_dict.items():
        try:
            int_key = int(key)  # Преобразуем ключ в int
        except ValueError:
            print(f"Skipping invalid key: {key}")  # Обработка некорректного ключа
            continue  # Пропускаем этот элемент

        bool_value, str_list = value  # Разделяем tuple
        int_list: List[int] = []
        for s in str_list:
            try:
                int_val = ord(s.upper()) - ord('A')  # Преобразуем строку в int (A=0, B=1, ...)
                if 0 <= int_val < 26: # check if the letter is valid
                    int_list.append(int_val)
                else:
                    print(f"Skipping invalid list value: {s}")
                    continue
            except Exception as e: #handles all other exceptions
                print(f"Skipping invalid list value: {s}")
                continue
        transformed_data[int_key] = (bool_value, int_list)

    return transformed_data

@app.post("/agent/move_info/{agent_id}")
async def get_game_info(
    agent_id: int ,
    move_data: Dict[str, Tuple[bool, List[str]]],
):
    if agent_id not in agent_service.agent.agents:
        raise HTTPException(status_code=404, detail="Agent not found")

    agent = agent_service.agent.agents[agent_id]
    logging.info(f"Received move data for agent {agent_id}: {move_data}")
    data_to_n = transform_move_data(move_data)
    agent.neural_network.update(data_to_n)
    stone_to_pick = agent.neural_network.choose_stone()
    asyncio.create_task(agent.pick_stone(stone_to_pick))
    return {"status": "success", "data": move_data}

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_loop.user_interface())

@app.on_event("shutdown")
async def shutdown_event():
    for agent in agent_service.agent.agents.values():
        await agent.close()