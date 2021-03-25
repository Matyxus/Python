buttons = {}

buttons["play"] = (False, 15)
print(buttons)
buttons.update({"play": (True, buttons["play"][1])})

for act, butt in buttons.values():
	print(act, butt)







