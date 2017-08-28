import csv, json, requests
import urllib

testfile = urllib.URLopener()
testfile.retrieve("https://docs.google.com/spreadsheets/d/15-rp4oC3QCBs3SvyLM5PNemSMHVdRGNY-kjHEyK_PGg/export?format=csv&id=15-rp4oC3QCBs3SvyLM5PNemSMHVdRGNY-kjHEyK_PGg&gid=0", "sublet.csv")

with open('sublet.csv', 'rb') as csvfile:
	f = csv.writer(open("populate.csv", "wb+"))
	reader = csv.reader(csvfile)

	f.writerow(["address","rent","comments"])

	for data in reader:
                # print(data[3])
                extracted_number = ""
                found_number = False
                for i in data[3]:
                        if i.isdigit() == True:
                                found_number = True
                                extracted_number = extracted_number + i
                        else:
                                if found_number == True:
                                        break

                if extracted_number != "":
        		f.writerow([data[1] + " Medford MA",
        					int(extracted_number),
			             		data[6]])

                        print(".")

                        r = requests.post("http://glasshouse120.herokuapp.com/house",
                                params = {"address" : (data[1] + " Medford MA"), "rent" : int(extracted_number)})