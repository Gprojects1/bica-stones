from agent_service import agent

async def user_interface():
    while True:
        print("\n1. Создать нового агента")
        print("2. Получить список лобби")
        print("3. Войти в лобби")
        print("4. Выйти")
        choice = input("Выберите действие: ")

        if choice == "1":
            agent_id = int(input("Введите ID агента: "))
            api_url = input("Введите URL API: ")
            agent = agent.Agent(agent_id, api_url)
            agent.agents[agent_id] = agent
            print(f"Агент {agent_id} создан.")

        elif choice == "2":
            if not agent.agents:
                print("Нет созданных агентов.")
                continue
            agent_id = int(input("Введите ID агента: "))
            if agent_id not in agent.agents:
                print("Агент не найден.")
                continue
            lobby_ids = await agent.agents[agent_id].get_lobby_ids()
            if lobby_ids:
                print("Доступные лобби:", lobby_ids)
            else:
                print("Не удалось получить список лобби.")

        elif choice == "3":
            if not agent.agents:
                print("Нет созданных агентов.")
                continue
            agent_id = int(input("Введите ID агента: "))
            if agent_id not in agent.agents:
                print("Агент не найден.")
                continue
            lobby_id = int(input("Введите ID лобби: "))
            result = await agent.agents[agent_id].enter_lobby(lobby_id)
            if result:
                print(f"Агент {agent_id} вошел в лобби {lobby_id}.")
            else:
                print("Не удалось войти в лобби.")

        elif choice == "4":
            break

        else:
            print("Неверный выбор. Попробуйте снова.")