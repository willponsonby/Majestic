from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
import re

# Windows users need to specify the path to chrome driver you just downloaded.
# You need to unzip the zipfile first and move the .exe file to any folder you want.
# driver = webdriver.Chrome(r'path\to\the\chromedriver.exe')
driver = webdriver.Chrome(r'C:\Users\wrapo\chromedriver.exe')
# Go to the page that we want to scrape
driver.get("https://www.majestic.co.uk/wine?pageNum=0&pageSize=40")


# Page index used to keep track of where we are.
index = 1
# We want to start the first two pages.
# If everything works, we will change it to while True
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
			bottle_dict['name'] = name

			percentage = driver.find_element_by_xpath('.//span[@class="splodge__ba-number"]').text
			print(percentage)
			bottle_dict['Percentage'] = percentage	

			n_reviewers = driver.find_element_by_xpath('.//span[@class="splodge__ba-total t-fine"]').text
			print(n_reviewers)
			bottle_dict['n_reviewers'] = n_reviewers

			awards = driver.find_element_by_xpath('.//div[@class="award-container"]')
			try:
				award = driver.find_element_by_xpath('.//div[@class="award-container"]//img[2]').get_attribute('alt')
				print(award)
			except:
				print('NA')





			#if awards.text == "":
			#	print('NA')
			#else:
			#	awards2 = driver.find_element_by_xpath('.//div[@class="award-container"]//img[2]').get_attribute('alt')
			#	print(awards2)
			bottle_dict['awards'] = awards

			tab = bottle.find_element_by_xpath('.//a[@alt="Product Image"]')
			main_window = driver.current_window_handle
			body = driver.find_element_by_tag_name('body')
			ActionChains(driver).key_down(Keys.CONTROL).key_down(Keys.SHIFT).click(tab).key_up(Keys.CONTROL).key_up(Keys.SHIFT).perform()
			driver.switch_to.window(driver.window_handles[1])
			time.sleep(2)

			ABV = driver.find_element_by_xpath('.//div[@class="product-info__symbol product-info__symbol--abv"]/div').text
			print(ABV)
			bottle_dict['ABV'] = ABV

			country = driver.find_element_by_xpath('.//div[@class="product-info__symbol product-info__symbol--country"]/div[@class="product-info__symbol-label"]').text
			print(country)
			bottle_dict['Country'] = country			

			description = driver.find_element_by_xpath('.//div[@class="product-info__info product-info__info--pdp"]/div[3]/div[2]').text
			print(description)
			bottle_dict['ABV'] = description

			full_description = driver.find_element_by_xpath('.//p[@class="product-content__description"]').text
			print(full_description)
			bottle_dict['Full Description'] = full_description

			price_per_bottle = driver.find_element_by_xpath('.//span[@class="product-action__price-info"]').text
			print(price_per_bottle)
			bottle_dict['Per Bottle Price'] = price_per_bottle

			mix_six_price = driver.find_element_by_xpath('.//span[@class="product-action__price-text"]').text		
			print(mix_six_price)
			bottle_dict['Mix Six Price'] = mix_six_price		

			more_details = driver.find_element_by_xpath('.//p[@class="product-content__more t-link js-more-toggle"]')
			cookies = driver.find_element_by_xpath('.//span[@class="close js-close-cookie"]')

			

			
			try:
				cookies.click()
			except:
				time.sleep(1)
			finally:	
				more_details.click()

			#type = driver.find_element_by_xpath('.//table[@class="content-table"]/tbody/tr[3]').text
			#print('Wine type = {}'.format(type))
			#bottle_dict['Wine type'] = type

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
				print(value_list[key_list.index('TYPE')])
			else:
				print('N/A')

			if 'STYLE' in key_list:
				print(value_list[key_list.index('STYLE')])
			else:
				print('N/A')

			if 'CLOSURE' in key_list:
				print(value_list[key_list.index('CLOSURE')])
			else:
				print('N/A')

			if 'UNITS' in key_list:
				print(value_list[key_list.index('UNITS')])
			else:
				print('N/A')

			if 'GRAPE' in key_list:
				print(value_list[key_list.index('GRAPE')])
			else:
				print('N/A')


				#if z.text == 'TYPE':
				#	print('Type = {}').format(next(z.text))
				#else:
				#	print('NA')
				#print('Contents = {}'.format(y))
				#bottle_dict['y'] = y

			print('='*100)
			print('='*100)

			time.sleep(1)
			driver.close()
			driver.switch_to_window(main_window)

		cookies = driver.find_element_by_xpath('.//span[@class="close js-close-cookie"]')					
		elementToClick = driver.find_element_by_xpath('//div[@class="search-results__pagination"]//a[@href="/wine?pageNum={}&pageSize=40"]'.format(index-1))
		#driver.executeScript("window.scrollTo(0,"+elementToClick.getLocation().y+")")
		try:
			cookies.click()
		except:
			time.sleep(1)
		finally:	
			elementToClick.click()

	except Exception as e:
		print(e)
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

