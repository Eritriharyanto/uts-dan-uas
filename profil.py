def biodata(npm,nama,prodi):
	print("npm adalah :{}".format(npm))
	print("nama adalah :{}".format(nama))
	print("prodi adalah :{}".format(prodi))
profile = {"npm":"2200123","nama":"pipit toton","prodi":"informatika"}
biodata(**profile)