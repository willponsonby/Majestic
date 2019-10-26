from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
import re
import csv

driver = webdriver.Chrome(r'C:\Users\wrapo\chromedriver.exe')

driver.get("https://www.majestic.co.uk/wine?pageNum=0&pageSize=6")
time.sleep(4)
index = 1

csv_file = open('majestic4.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)

while index <=2:
	try:
		print('\n')
		print("Scraping Page number " + str(index))
		print('\n')

		index = index + 1

		bottles = driver.find_elements_by_xpath('//div[@class="search-results__listing"]')

		for bottle in bottles:
			
			bottle_dict = {}		
			
			name = bottle.find_element_by_xpath('.//h3[@class="space-b--none"]/a').text
			print(name)
			bottle_dict['Name'] = name

			try:
				percentage = bottle.find_element_by_xpath('.//span[@class="splodge__ba-number"]').text
				print(percentage)
			except:
				print('NA')
			bottle_dict['Percentage'] = percentage	

			try:
			    n_reviewers = bottle.find_element_by_xpath('.//span[@class="splodge__ba-total t-fine"]').text
			    print(n_reviewers)
			except:
			    print('NA')
			bottle_dict['n_reviewers'] = n_reviewers[3:]
		
			################
			# open new tab #
			################

			tab = bottle.find_element_by_xpath('.//a[@alt="Product Image"]')
			main_window = driver.current_window_handle
			body = driver.find_element_by_tag_name('body')
			ActionChains(driver).key_down(Keys.CONTROL).key_down(Keys.SHIFT).click(tab).key_up(Keys.CONTROL).key_up(Keys.SHIFT).perform()
			driver.switch_to.window(driver.window_handles[1])
			time.sleep(1)


			awards = driver.find_elements_by_xpath('//div[@class="award-container__award"]/img')
			lis = []
			for i in range(len(awards)):
				lis.append(awards[i].get_attribute('alt'))
			print(lis[1:])
			bottle_dict['awards'] = lis[1:]

			ABV = driver.find_element_by_xpath('.//div[@class="product-info__symbol product-info__symbol--abv"]/div').text
			print(ABV[4:])
			bottle_dict['ABV'] = ABV[4:]		

			description = driver.find_element_by_xpath('.//div[@class="product-info__info product-info__info--pdp"]/div[3]/div[@class="product-info__symbol-label"]').text
			print(description)
			bottle_dict['Description'] = description

			full_description = driver.find_element_by_xpath('.//p[@class="product-content__description"]').text
			print(full_description)
			bottle_dict['Full Description'] = full_description

			price_per_bottle = driver.find_element_by_xpath('.//span[@class="product-action__price-info"]').text
			print(price_per_bottle)
			bottle_dict['Per Bottle Price'] = str((re.findall('\d+', price_per_bottle)[0])) + '.' + str(re.findall('\d+', price_per_bottle)[1])

			mix_six_price = driver.find_element_by_xpath('.//span[@class="product-action__price-text"]').text		
			print(mix_six_price)
			bottle_dict['Mix Six Price'] = str((re.findall('\d+', mix_six_price)[0])) + '.' + str(re.findall('\d+', mix_six_price)[1])	

			more_details = driver.find_element_by_xpath('.//p[@class="product-content__more t-link js-more-toggle"]')
			cookies = driver.find_element_by_xpath('.//span[@class="close js-close-cookie"]')
			
			try:
				cookies.click()
			except:
				pass
				
			more_details.click()

			content_table = driver.find_elements_by_xpath('.//table[@class="content-table"]//tr')
			for x in content_table:
				td_key_tags = driver.find_elements_by_xpath('.//td[1]')

			key_list = []
			for x_key in td_key_tags:
				key_list.append(x_key.text)

			for y in content_table:
				td_value_tags = driver.find_elements_by_xpath('.//td[2]')

			value_list = []
			for y_value in td_value_tags:
				value_list.append(y_value.text)

			if 'TYPE' in key_list:
				type = value_list[key_list.index('TYPE')]
				print(value_list[key_list.index('TYPE')])
			else:
				type = 'N/A'
				print('N/A')
			bottle_dict['Type'] = type

			if 'STYLE' in key_list:
				style = value_list[key_list.index('STYLE')]
				print(value_list[key_list.index('STYLE')])
			else:
				style = 'N/A'
				print('N/A')
			bottle_dict['Style'] = style

			if 'CLOSURE' in key_list:
				closure = value_list[key_list.index('CLOSURE')]
				print(value_list[key_list.index('CLOSURE')])
			else:
				closure = 'N/A'
				print('N/A')
			bottle_dict['Closure'] = closure

			if 'UNITS' in key_list:
				units = value_list[key_list.index('UNITS')]
				print(value_list[key_list.index('UNITS')])
			else:
				units = 'N/A'
				print('N/A')
			bottle_dict['Units'] = units

			if 'GRAPE' in key_list:
				grape = value_list[key_list.index('GRAPE')]
				print(value_list[key_list.index('GRAPE')])
			else:
				grape = 'N/A'
				print('N/A')
			bottle_dict['Grape'] = grape

			if 'COUNTRY' in key_list:
				country = value_list[key_list.index('COUNTRY')]
				print(value_list[key_list.index('COUNTRY')])
			else:
				country = 'N/A'
				print('N/A')
			bottle_dict['Country'] = country

			writer.writerow(bottle_dict.values())

			print('='*100)
			print('='*100)

			driver.close()
			driver.switch_to_window(main_window)

			#############
			# close tab #
			#############

		cookies = driver.find_element_by_xpath('.//span[@class="close js-close-cookie"]')					
		elementToClick = driver.find_element_by_xpath('//div[@class="search-results__pagination"]//a[@href="/wine?pageNum={}&pageSize=6"]'.format(index-1))

		try:
			cookies.click()
		except:
			pass
			
		elementToClick.click()

	except Exception as e:
		print(e)
		csv_file.close()
		driver.close()
		break


		# Iterate through the list and find the details of each review.
		#elementToClick = driver.find_element_by_xpath('//h3[@class="space-b--none"]/a')
		#time.sleep(3)





		#elementToClick.click()
		#for bottle in bottles:

			# Click review button to go to the review section
			#wine_button = driver.find_element_by_tag_name(bottle).send_keys(Keys.COMMAND + 't') 
			#wine_button.click()
		
			# Initialize an empty dictionary for each review
			#bottle_dict = {}
			# Use try and except to skip the review elements that are empty. 
			# Use relative xpath to locate the title.
			# Once you locate the element, you can use 'element.text' to return its string.
			# To get the attribute instead of the text of each element, use 'element.get_attribute()'
			#try:
			#	name = review.find_element_by_xpath('.//h1[@itemprop="name" class="product-info__name"]').text
			#except:
			#	continue

			#print('Name = {}'.format(name))

			#driver.find_element_by_tag_name('//img[@itemprop="image"]/@src').send_keys(Keys.COMMAND + 'w')
			#driver.close()

			#stars = review.find_element_by_xpath('.//span[@class="positionAbsolute top0 left0 overflowHidden color_000"]').get_attribute('style')
			#rating = int(re.findall('\d+', stars)[0])/20
			#print('Rating = {}'.format(rating))

			#username = review.find_element_by_xpath('.//span[@class="padLeft6 NHaasDS55Rg fontSize_12 pad3 noBottomPad padTop2"]').text
			#print('Username = {}'.format(username))

			#text = review.find_element_by_xpath('.//span[@class="pad6 onlyRightPad"]').text
			#print('Text = {}'.format(text))

			

			# OPTIONAL: How can we deal with the "read more" button?
			
			# Use relative xpath to locate text, username, date_published, rating.
			# Your code here

			# Uncomment the following lines once you verified the xpath of different fields
			

			#bottle_dict['text'] = text
			#bottle_dict['username'] = username
			# bottle_dict['date_published'] = date_published
			#bottle_dict['rating'] = rating

		# We need to scroll to the bottom of the page because the button is not in the current view yet.
		

		# Locate the next button element on the page and then call `button.click()` to click it.
		#button = driver.find_element_by_xpath('//li[@class="nextClick displayInlineBlock padLeft5 "]')
		#button.click()
		#time.sleep(2)

