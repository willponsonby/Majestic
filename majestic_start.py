from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
import re
import csv

driver = webdriver.Chrome(r'C:\Users\wrapo\chromedriver.exe')

driver.get("https://www.majestic.co.uk/wine?pageNum=0&pageSize=40")
time.sleep(5)
index = 1

csv_file = open('majestic_df.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)

while index <=21:
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
				bottle_dict['Percentage'] = percentage
			except:
				print('NA')
				bottle_dict['Percentage'] = 'N/A'

			try:
				n_reviewers = bottle.find_element_by_xpath('.//span[@class="splodge__ba-total t-fine"]').text
				print(n_reviewers)
				bottle_dict['n_reviewers'] = n_reviewers[3:]
			except:
				print('NA')
				bottle_dict['n_reviewers'] = 'N/A'
			
		
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

			try:
				volume = driver.find_element_by_xpath('.//div[@class="product-info__symbol"]/div[@class="product-info__symbol-label"]').text
				print(volume[:-2])
				bottle_dict['Volume'] = volume[:-2]
			except:
				print('N/A')
				bottle_dict['Volume'] = 'N/A'

			try:
				ABV = driver.find_element_by_xpath('.//div[@class="product-info__symbol product-info__symbol--abv"]/div').text
				print(ABV[4:])
				bottle_dict['ABV'] = ABV[4:]
			except:
				print('N/A')
				bottle_dict['ABV'] = 'N/A'		

			try:
				description = driver.find_element_by_xpath('.//div[@class="product-info__info product-info__info--pdp"]/div[3]/div[@class="product-info__symbol-label"]').text
				print(description)
				bottle_dict['Description'] = description
			except:
				print('N/A')
				bottle_dict['Volume'] = 'N/A'

			try:
				full_description = driver.find_element_by_xpath('.//p[@class="product-content__description"]').text
				print(full_description)
				bottle_dict['Full Description'] = full_description
			except:
				print('N/A')
				bottle_dict['Full Description'] = 'N/A'

			try:
				price_per_bottle = driver.find_element_by_xpath('.//span[@class="product-action__price-info"]').text
				print(price_per_bottle)
				bottle_dict['Per Bottle Price'] = str((re.findall('\d+', price_per_bottle)[0])) + '.' + str(re.findall('\d+', price_per_bottle)[1])
			except:
				print('N/A')
				bottle_dict['Per Bottle Price'] = 'N/A'

			try:
				mix_six_price = driver.find_element_by_xpath('.//span[@class="product-action__price-text"]').text		
				print(mix_six_price)
				bottle_dict['Mix Six Price'] = str((re.findall('\d+', mix_six_price)[0])) + '.' + str(re.findall('\d+', mix_six_price)[1])	
			except:
				print('N/A')
				bottle_dict['Mix Six Price'] = 'N/A'
			
			
			try:
				cookies = driver.find_element_by_xpath('.//span[@class="close js-close-cookie"]')
				cookies.click()
			except:
				pass

			try:
				more_details = driver.find_element_by_xpath('.//p[@class="product-content__more t-link js-more-toggle"]')
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
			except:
				bottle_dict['Type'] = 'N/A'
				bottle_dict['Style'] = 'N/A'
				bottle_dict['Closure'] = 'N/A'
				bottle_dict['Units'] = 'N/A'
				bottle_dict['Grape'] = 'N/A'
				bottle_dict['Country'] = 'N/A'

			writer.writerow(bottle_dict.values())

			print('='*100)
			print('='*100)

			driver.close()
			driver.switch_to_window(main_window)

			#############
			# close tab #
			#############

		cookies = driver.find_element_by_xpath('.//span[@class="close js-close-cookie"]')					
		elementToClick = driver.find_element_by_xpath('//div[@class="search-results__pagination"]//a[@href="/wine?pageNum={}&pageSize=40"]'.format(index-1))

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


