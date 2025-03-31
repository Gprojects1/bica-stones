import aioconsole
from agent_service import agent

async def user_interface():
    agent_instance = None  # Инициализация переменной agent
    while True:
        print("\n1. Создать нового агента")
        print("2. Получить список лобби")
        print("3. Войти в лобби")
        print("4. Выйти")
        choice = await aioconsole.ainput("Выберите действие: ")

        if choice == "1":
            agent_id = int(await aioconsole.ainput("Введите ID агента: "))
            api_url = await aioconsole.ainput("Введите URL API: ")
            agent_instance = agent.Agent(agent_id, api_url)  # Теперь используем agent_instance
            if agent_instance: #проверяем что агент создался
                agent.agents[agent_id] = agent_instance
                print(f"Агент {agent_id} создан.")
            else:
                print(f"Не удалось создать агента {agent_id}.")

        elif choice == "2":
            if agent_instance is None or not agent.agents:  # Проверяем, был ли создан агент
                print("Нет созданных агентов.")
                continue
            agent_id = int(await aioconsole.ainput("Введите ID агента: "))
            if agent_id not in agent.agents:
                print("Агент не найден.")
                continue
            if agent.agents.get(agent_id):
                lobby_ids = await agent.agents[agent_id].get_lobby_ids()
                if lobby_ids:
                    print("Доступные лобби:", lobby_ids)
                else:
                    print("Не удалось получить список лобби.")
            else:
                print('Агент не найден')


        elif choice == "3":
            if agent_instance is None or not agent.agents:  # Проверяем, был ли создан агент
                print("Нет созданных агентов.")
                continue
            agent_id = int(await aioconsole.ainput("Введите ID агента: "))
            if agent_id not in agent.agents:
                print("Агент не найден.")
                continue
            if agent.agents.get(agent_id):
                lobby_id = int(await aioconsole.ainput("Введите ID лобби: "))
                result = await agent.agents[agent_id].enter_lobby(lobby_id)
                if result:
                    print(f"Агент {agent_id} вошел в лобби {lobby_id}.")
                else:
                    print("Не удалось войти в лобби.")
            else:
                print('Агент не найден')


        elif choice == "4":
            break

        else:
            print("Неверный выбор. Попробуйте снова.")