def merek(*args):
	print("masukan merek sepeda")
	jumlah_sepeda = int(input("masukan banyaknya sepeda : "))

	for i in range(jumlah_sepeda):
		sepeda = input(f"sepeda {i+1} : ")
		args += (sepeda,)

		for i, sepeda in enumerate (args):
			print(f"{i+1}. {sepeda}")
	print("Terimakasih")
merek()