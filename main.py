from bs4 import BeautifulSoup
import requests
import pandas as pd

url = requests.get('https://divar.ir/s/tehran/buy-apartment/navvab?districts=1006%2C197%2C275%2C284%2C94&price=1800000000-2500000000')

be = BeautifulSoup(url.text,'html.parser')

perlist = []
names = []

for item in be.find('div', attrs={'class': 'kt-post-card__body'}):
    for n in be.find_all('div', attrs={'class': 'kt-post-card__title'}):
        names.append(n.text)
    for pr in be.find_all('div', attrs={'class': 'kt-post-card__description'}):
        perlist.append(pr.text.replace('تومان','').replace(',',''))


max_length = max(len(names), len(perlist))

# Fill in missing values with None
names += [None] * (max_length - len(names))
perlist += [None] * (max_length - len(perlist))

# Convert the list to a DataFrame
df = pd.DataFrame({
'name':names,
'price':perlist
})
# Write the DataFrame to an Excel file
df.to_excel('output.xlsx', index=False)