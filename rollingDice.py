# import random
#
#
# print("Rolling ur Dice")
# for i in range(1,11):
#     user = input("Press enter")
#     if i<10 or n==6:
#         n = random.randint(1, 6)
#         if n<6:
#             print(n)
#             print(f"No. of times u roll: {i},Try again")
#         else:
#             print(n)
#             print(f"U took {i} times to get six")
#             print("Yeah! U got 6...")
#             break
#     else:
#         print(n)
#         print(f"U took {i} times to roll but not getting 6")
#         print("Game over!!")


# import random
# min = 1
# max = 6
#
# roll_again = "yes"
#
# while roll_again == "yes" or roll_again == "y":
#     print("Rolling the dices...")
#     print("The values are....")
#     print(random.randint(min, max))
#     print(random.randint(min, max))
#
#     roll_again = input("Roll the dices again?")

# import random
# from collections import Counter
# s = """
# happy sad mango cherry bba jimmy harmony kind nope
# """
# s = s.split()
# word = random.choice(s)
# print(word)