import googlemaps
import cloudscraper
from bs4 import BeautifulSoup
scraper = cloudscraper.create_scraper()
gmaps = googlemaps.Client(key = "")
class Worth:
	def __init__(self, city_mpg, tank_size):
		self.tank_size = tank_size
		self.city_mpg = city_mpg
	def generate_local_gas(self, zip_code = ""): #Generates a dictionary with the addresses and prices of the gas station
		url = "https://www.gasbuddy.com/home?search="
		url += zip_code
		page = scraper.get(url)
		soup = BeautifulSoup(page.content, 'html.parser')
		prices = soup.findAll("span", attrs={
			"class": "text__xl___2MXGo text__left___1iOw3 StationDisplayPrice-module__price___3rARL"})
		addresses = soup.findAll("div", attrs={"class": "StationDisplay-module__address___2_c7v"})
		local_gas = {}
		price_lst = []
		for price in prices: #Generates a list of prices
			price_lst.append(price.text.replace("$", ""))
		for address in addresses: #Iterates through addresses and matches the addresses to the prices
			count = 0
			local_gas[address.text] = price_lst[count]
			count += 1
		return local_gas
	def get_price(self, start, destination, price, tank_percent): #
		my_dist = gmaps.distance_matrix(start, destination)['rows'][0]['elements'][0] #Calculates the distance between start and the gas station
		fuel_used = (int(my_dist["distance"]["value"]) * 0.000621371)/float(self.city_mpg) #Calculates the fuel used when driving from state to gas station based on mpg
		percent_needed = 1.0 - float(int(tank_percent)/100) #Calculates the percent of tank that needs to be filled up
		return (2*(float(fuel_used)*float(price)) + float(self.tank_size)*float(price)*float(percent_needed))*1.1 #calculates the total cost of gas, which includes a 10% tax and a trip to the gas station and back

city_mpg = input("What is your car's city mpg?")
tank_size = input("What is your car's tank size?")
tank_percent = input("What percent of your car's tank is full? (EX: '20' or '90')")
start = input("What address are you starting your drive?")
zip_code = input("What is your zip code?")
best_option = {"total" : 0.00, #Dictionary that holds the best option for gas station given the zip code that one begins in
			   "price" : 0.00,
			   "address" : ""}
current = Worth(city_mpg, tank_size)
x = current.generate_local_gas(zip_code)
for address, price in x.items(): #Generates the best option dictionary by iterating through each gas station and calculating the total cost of gas and the trip
	total = current.get_price(start, address, price, tank_percent)
	if best_option["address"] == "":
		best_option["total"] = total
		best_option["price"] = price
		best_option["address"] = address
	else:
		if best_option["total"] > total:
			best_option["total"] = total
			best_option["price"] = price
			best_option["address"] = address
		else:
			continue
y = best_option["address"]
z = best_option["price"]
j = best_option["total"]
print(f"The best option in your area is currently at {y} with a price of ${z} per gallon")
prompt1 = input("Would you like to check a specific gas station? (Y/N)")
if prompt1.lower() == "y":
	prompt1_a = input("What is the address of the gas station?")
	prompt1_b = input("What is the price of gas there in $/gallon?")
	specific = Worth(city_mpg, tank_size) #Instantiates a class for a specific gas station
	specific_total = specific.get_price(start, prompt1_a, prompt1_b, tank_percent) #Calculates the price of trip to a specific gas station and fill up
	if specific_total > best_option["total"]:
		print("This is not worth it")
		print(f"Going to {prompt1_a} will cost you ${specific_total} while going to {y} will cost you ${j}")
	else:
		print("This is worth it!")
		print(f"Going to {prompt1_a} will cost you ${specific_total} while going to {y} will cost you ${j}")
if prompt1.lower() == "n":
	print("Thank you")
