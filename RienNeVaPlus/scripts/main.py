import game_functions as gf


def run():
    # Runs the program
    budget = gf.ask_budget()
    spin = False
    bet_list = []
    while not spin:
        bet = gf.ask_bet()
        bet_list.append((bet))
        bet_value = int(input("Enter how much you would like to bet: "))
        budget -= bet_value
        if input("Bet some more? y/n: ") == "n":
            spin = True

    spinned_number = gf.spin_wheel()
    bet_multiplier_list = gf.wheel_math(spinned_number, bet_list)
    if bet_multiplier_list:
        for bet_multiplier in bet_multiplier_list:
            budget += bet_value * bet_multiplier
    print(budget)
    spin = False


run()
