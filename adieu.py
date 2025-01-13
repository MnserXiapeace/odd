import inflect

p = inflect.engine()


mon_list = []
a = 1
while True:
    try:
        user_input = input("Name: ").strip()

        mon_list.append(user_input)
        if user_input == "":
            mon_list = mon_list[:-1]
            mon_list = p.join(mon_list)
            print(f"Adieu, adieu, to {mon_list}")
            break

    except EOFError:
        mon_list = p.join(mon_list)
        print(f"Adieu, adieu, to {mon_list}")
        break