import requests
import time
import csv
from bs4 import BeautifulSoup
import os
import pandas as pd
import glob

def parse_ad(soup):
    """
    Parses the information on the listing page using the given BeautifulSoup object.

    Price information is also retrieved with the "data-testid" attribute.

    Args:
    soup (BeautifulSoup): Parsed version of the listing page's HTML content.

    Returns:
    dict: Parsed listing data.
    """
    # Dictionary containing all fields, initially defaulting to None.
    data = {
        "adv_no": None,
        "price": None,
        "adv_date": None,
        "car_brand": None,
        "car_series": None,
        "car_model": None,
        "year": None,
        "km": None,
        "gear_type": None,
        "fuel_type": None,
        "carbody_type": None,
        "color": None,
        "engine_capacity": None,
        "engine_power": None,
        "engine_trac": None,
        "car_cond": None,
        "paint_change": None,
        "mean_fuel_cons": None,
        "fuel_storage": None,
        "trade_in": None,
        "seller": None,
        "warranty": None,
        # Overview section
        "car_class": None,
        # Engine and Performance section
        "max_speed": None,
        "acceleration": None,
        "max_power": None,
        "min_power": None,
        "engine_power": None,
        "engine_capacity": None,
        "torque": None,
        # Fuel Consumption section
        "city_fuel_consumption": None,
        "highway_fuel_consumption": None,
        "fuel_storage": None,
        # Size and Capacity section
        "seats": None,
        "trunk_capacity": None,
        "aks_range": None,
        # Extra: Area to include URL information (to be filled in later)
        "url": None
    }

    # ---------------------------------------------------------------------------
    # Part 1: We pull basic listing information from divs with "property-item" class.
    # ---------------------------------------------------------------------------
    for item in soup.find_all('div', class_='property-item'):
        key_elem = item.find('div', class_='property-key')
        value_elem = item.find('div', class_='property-value')
        if not (key_elem and value_elem):
            continue
        key_text = key_elem.get_text(strip=True)
        value_text = value_elem.get_text(strip=True)

        if key_text == "İlan No":
            data["adv_no"] = value_text.strip("Kopyalandı")
        elif key_text == "İlan Tarihi":
            data["adv_date"] = value_text
        elif key_text == "Marka":
            data["car_brand"] = value_text
        elif key_text == "Seri":
            data["car_series"] = value_text
        elif key_text == "Model":
            data["car_model"] = value_text
        elif key_text == "Yıl":
            data["year"] = value_text
        elif key_text == "Kilometre":
            data["km"] = value_text
        elif key_text == "Vites Tipi":
            data["gear_type"] = value_text
        elif key_text == "Yakıt Tipi":
            data["fuel_type"] = value_text
        elif key_text == "Kasa Tipi":
            data["carbody_type"] = value_text
        elif key_text == "Renk":
            data["color"] = value_text
        elif key_text == "Motor Hacmi":
            data["engine_capacity"] = value_text.strip(" cc")
        elif key_text == "Motor Gücü":
            data["engine_power"] = value_text.strip(" hp")
        elif key_text == "Çekiş":
            data["engine_trac"] = value_text
        elif key_text == "Araç Durumu":
            data["car_cond"] = value_text
        elif key_text == "Ort. Yakıt Tüketimi":
            data["mean_fuel_cons"] = value_text
        elif key_text == "Yakıt Deposu":
            data["fuel_storage"] = value_text.strip(" lt")
        elif key_text == "Boya-değişen":
            data["paint_change"] = value_text
        elif key_text == "Takasa Uygun":
            data["trade_in"] = value_text
        elif key_text == "Kimden":
            data["seller"] = value_text
        elif key_text == "Garanti Durumu":
            data["warranty"] = value_text

    # ---------------------------------------------------------------------------
    # Part 2: We pull the detailed information in the "tab-content-car-information-container".
    # ---------------------------------------------------------------------------
    containers = soup.find_all("div", class_="tab-content-car-information-container")
    for container in containers:
        header = container.find("h3")
        if not header:
            continue
        section_name = header.get_text(strip=True)

        #Overview: Vehicle Class information
        if section_name == "Genel Bakış":
            for li in container.find_all("li"):
                key_span = li.find("span", class_="property-key")
                value_span = li.find("span", class_="property-value")
                if key_span and value_span:
                    if key_span.get_text(strip=True) == "Sınıfı":
                        data["car_class"] = value_span.get_text(strip=True)
                        break

        # Engine and Performance information
        elif section_name == "Motor ve Performans":
            for li in container.find_all("li"):
                key_span = li.find("span", class_="property-key")
                value_span = li.find("span", class_="property-value")
                if not (key_span and value_span):
                    continue
                key = key_span.get_text(strip=True)
                val = value_span.get_text(strip=True)
                if key == "Maksimum Hız":
                    data["max_speed"] = val.strip(" km/s")
                elif key == "Hızlanma (0-100)":
                    data["acceleration"] = val.strip(" sn")
                elif key == "Maksimum Güç":
                    data["max_power"] = val.strip(" rpm")
                elif key == "Minimum Güç":
                    data["min_power"] = val.strip(" rpm")
                elif key == "Motor Gücü":
                    data["engine_power"] = val.strip(" hp")
                elif key == "Motor Hacmi":
                    data["engine_capacity"] = val.strip(" cc")
                elif key == "Tork":
                    data["torque"] = val.strip(" nm")

        # Fuel Consumption information
        elif section_name == "Yakıt Tüketimi":
            for li in container.find_all("li"):
                key_span = li.find("span", class_="property-key")
                value_span = li.find("span", class_="property-value")
                if not (key_span and value_span):
                    continue
                key = key_span.get_text(strip=True)
                val = value_span.get_text(strip=True)
                if key == "Şehir İçi Yakıt Tüketimi":
                    data["city_fuel_consumption"] = val.strip(" lt")
                elif key == "Şehir Dışı Yakıt Tüketimi":
                    data["highway_fuel_consumption"] = val.strip(" lt")
                elif key == "Yakıt Deposu":
                    data["fuel_storage"] = val.strip(" lt")

        # Dimensions and Capacity information
        elif section_name == "Boyut ve Kapasite":
            for li in container.find_all("li"):
                key_span = li.find("span", class_="property-key")
                value_span = li.find("span", class_="property-value")
                if not (key_span and value_span):
                    continue
                key = key_span.get_text(strip=True)
                val = value_span.get_text(strip=True)
                if key == "Koltuk Sayısı":
                    data["seats"] = val
                elif key == "Bagaj Hacmi":
                    data["trunk_capacity"] = val.strip(" lt")
                elif key == "Aks Aralığı":
                    data["aks_range"] = val.strip(" mm")
    
    # ---------------------------------------------------------------------------
    # Part 3: We pull the price information.
    # ---------------------------------------------------------------------------
    price_elem = soup.find("div", {"data-testid": "desktop-information-price"})
    if price_elem:
        price_text = price_elem.get_text(strip=True)
        # "TL", boşluk ve nokta karakterlerini kaldırıyoruz.
        price_text = price_text.replace("TL", "").replace(" ", "").replace(".", "")
        data["price"] = price_text

    return data

def create_default_data(link):
    """
    In case of error, it creates a default dictionary with all fields set to None and includes link information.
    """
    return {
        "adv_no": None,
        "price": None,
        "adv_date": None,
        "car_brand": None,
        "car_series": None,
        "car_model": None,
        "year": None,
        "km": None,
        "gear_type": None,
        "fuel_type": None,
        "carbody_type": None,
        "color": None,
        "engine_capacity": None,
        "engine_power": None,
        "engine_trac": None,
        "car_cond": None,
        "paint_change": None,
        "mean_fuel_cons": None,
        "fuel_storage": None,
        "trade_in": None,
        "seller": None,
        "warranty": None,
        "car_class": None,
        "max_speed": None,
        "acceleration": None,
        "max_power": None,
        "min_power": None,
        "engine_capacity": None,
        "torque": None,
        "city_fuel_consumption": None,
        "highway_fuel_consumption": None,
        "fuel_storage":None,
        "seats": None,
        "trunk_capacity": None,
        "aks_range": None,
        "url": link
    }

def save_dataset(dataset, filename):
    """
    Saves the dataset to a CSV file.
    """
    if dataset:
        # We take the keys in the first row to ensure that the same fields are found in all rows.
        fieldnames = dataset[0].keys()
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(dataset)
        print(f"Your dataset has been saved to file '{filename}'.")
    else:
        print("No ad data could be retrieved.")

# ---------------------------------------------------------------------------
# Create page URLs
# ---------------------------------------------------------------------------
pages = ["https://www.arabam.com/ikinci-el/otomobil-istanbul?take=50"]
for page in range(2, 51):
    pages.append("https://www.arabam.com/ikinci-el/otomobil-istanbul?take=50&page=" + str(page))

print("Total number of pages:", len(pages))
for url in pages:
    print(url)

# ---------------------------------------------------------------------------
# Pull ad links from page URLs
# ---------------------------------------------------------------------------
all_links = []
total_pages = len(pages)

for idx, url in enumerate(pages, start=1):
    print(f"\n[{(idx/total_pages)*100:.2f}%] Visited page: {url}")
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    except Exception as e:
        print(f"{url} Error occurred while pulling {e}")
        continue

    time.sleep(5)
    
    if response.status_code != 200:
        print(f"{url} page could not be retrieved. Status Code: {response.status_code}")
        continue

    soup = BeautifulSoup(response.content, "html.parser")
    ad_elements = soup.find_all("tr", class_="listing-list-item")

    if not ad_elements:
        print(f"{url} no ads found on the page.")

    for ad in ad_elements:
        a_tag = ad.find("a", href=True)
        if a_tag:
            link = a_tag["href"]
            if link.startswith("/"):
                link = "https://www.arabam.com" + link
            all_links.append(link)
    
    time.sleep(1)

print("\nTotal number of ads:", len(all_links))
for link in all_links:
    print(link)

# ---------------------------------------------------------------------------
# Get the details from each ad link and create a dataset
# ---------------------------------------------------------------------------
dataset = []
batch_size = 100  # Save a break after every 100 ads are processed.
batch_counter = 0
total_links = len(all_links)

for idx, link in enumerate(all_links, start=1):
    progress = (idx / total_links) * 100
    print(f"\n[{progress:.2f}%] The ad is being withdrawn ({idx}/{total_links}): {link}")
    try:
        response = requests.get(link, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        time.sleep(5)
        if response.status_code == 200:
            ad_soup = BeautifulSoup(response.content, "html.parser")
            ad_data = parse_ad(ad_soup)
            # Let's add the URL information to each ad data:
            ad_data["url"] = link
        else:
            print(f"Error: {link} - HTTP {response.status_code}")
            ad_data = create_default_data(link)
    except Exception as e:
        print(f"{link} An error occurred while capturing: {e}")
        ad_data = create_default_data(link)
    
    dataset.append(ad_data)
    batch_counter += 1

    # Save after reaching a certain batch size
    if batch_counter >= batch_size:
        filename = f"adv_dataset_part_{idx // batch_size}.csv"
        save_dataset(dataset, filename)
        # Reset the dataset and reset the batch counter
        dataset = []
        batch_counter = 0

#If there is any remaining data, let's save it.
if dataset:
    filename = "adv_dataset_part_final.csv"
    save_dataset(dataset, filename)

# Combine all csv files
all_files = glob.glob("*.csv")

dfs = [pd.read_csv(file) for file in all_files]

merged_df = pd.concat(dfs, ignore_index=True)

merged_df.to_csv("arabamDataset.csv", index=False)

print("File saved as 'arabamDataset.csv'.")

