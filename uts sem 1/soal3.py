jenis = input("masukan jenis kendaraan : ")

a ="mobil"
b = "motor"
c = "sepeda"

if jenis == a:
	harga = 5000

elif jenis == b:
	harga = 2000

elif jenis == c:
	harga = 500

harga_format = ("{:,.0f}".format(harga).replace(",","."))

if harga > 0:
	print(f"biaya parkir anda adalah rp {harga_format},00")

else:
	print("tidak di kenakan parkir")