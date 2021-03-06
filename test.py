# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool
from urllib.request import urlopen
from proxies_scraper import get_proxies
from random import choice, uniform
from time import sleep
titles = ['seller',
            'feed_product_type',
            'item_sku',
            'external_product_id',
            'external_product_id_type',
            'part_number',
            'model',
            'item_name',
            'brand_name',
            'manufacturer',
            'product_description',
            'update_delete',
            'condition_type',
            'standard_price',
            'quantity',
            'product_tax_code',
            'product_site_launch_date',
            'restock_date',
            'sale_price',
            'sale_from_date',
            'sale_end_date',
            'item_package_quantity',
            'offering_can_be_gift_messaged',
            'offering_can_be_giftwrapped',
            'fulfillment_latency',
            'number_of_items',
            'merchant_shipping_group_name',
            'list_price_with_tax',
            'website_shipping_weight',
            'website_shipping_weight_unit_of_measure',
            'item_length',
            'item_heigth',
            'item_width',
            'item_dimensions_unit_of_measure',
            'item_weight',
            'item_weight_unit_of_measure',
            'bullet_point1',
            'bullet_point2',
            'bullet_point3',
            'bullet_point4',
            'bullet_point5',
            'recommended_browse_nodes',
            'generic_keywords',
            'style_keywords1',
            'style_keywords2',
            'style_keywords3',
            'main_image_url',
            'other_image_url1',
            'other_image_url2',
            'other_image_url3',
            'swatch_image_url',
            'parent_child',
            'parent_sku',
            'relationship_type',
            'variation_theme',
            'safety_warning',
            'legal_disclaimer_description',
            'strap_type',
            'style_name',
            'department_name',
            'outer_material_type1',
            'outer_material_type2',
            'inner_material_type1',
            'inner_material_type2',
            'material_composition',
            'closure_type',
            'lifestyle1',
            'lifestyle2',
            'lifestyle3',
            'seasons',
            'material_type1',
            'material_type2',
            'are_batteries_included',
            'battery_cell_composition',
            'lithium_battery_weight',
            'warranty_type',
            'warranty_description',
            'occasion_type1',
            'occasion_type2',
            'care_instructions',
            'sole_material',
            'heel_type',
            'toe_style',
            'arch_type',
            'color_name',
            'size_name',
            'collection_name',
            'sport_type']


useragents = open('useragents.txt').read().split('\n')
proxies = get_proxies()
for i in range(10):
    proxys = {'http':'http://' + choice(proxies)}
    useragentr = {'User-Agent': choice(useragents[:20])}

def get_html(start_url, useragent=useragentr, proxy=proxys):
    sleep(uniform(0, 1))
    try:
        r = requests.get(start_url, headers=useragentr, proxies=proxys, timeout=10)
    except (requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
        return None
    return r.text
    
def get_ip(url):
    print('proxy and ua')
    soup = BeautifulSoup(get_html(url), 'lxml')
    ip = soup.find('span', class_='ip')
    ua = soup.find('span', class_='ip').find_next_sibling('span').text.strip()
    print(ip.text)
    print(ua)

def get_number_of_pages(start_url):
    soup = BeautifulSoup(get_html(start_url), 'html5lib')
    for i in soup.findAll('span', class_='pagnDisabled'):
        pages = i.text.strip()
    return int(pages)
#
def get_start_urls():
    with open('Start_Urls.csv') as infile:
        reader = csv.DictReader(infile)
        script_cat = {row['URL']:row['Script Category'] for row in reader}     
def write_titles():
    with open('amazon_test.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(titles)
def generate_all_pages(url):
    all_pages = []
    num = get_number_of_pages(url)
    for i in range(1, num + 1):
        base_url = 'https://www.amazon.com/s/ref=sr_pg_' + str(i)
        query_part1 = '?' + url.split('?')[1].split('bbn=')[0] + 'page=' + str(i) + '&bbn='
        query_part2 = '&ie=' + url.split('&ie=')[1]
        new_url = base_url + query_part1 + query_part2
        all_pages.append(new_url)
    return all_pages

def get_product_links_multi(start_url):
    
    page_links = generate_all_pages(start_url)
    with Pool(4) as p:
        p.map(get_product_links_single, page_links)
def get_product_links_single(page_url):
    links = []
    with open('1.csv', 'a') as f:
        writer = csv.writer(f)
        html = get_html(page_url)
        if  html != None:
            soup = BeautifulSoup(html, 'html5lib')
            for k in soup.findAll('div', class_='a-row a-gesture a-gesture-horizontal'):
                item = k.find('a', class_='a-link-normal a-text-normal').get('href')
                links.append(item)
                writer.writerow([item])
        else:
            pass
    return links

def get_product_info(url, product_link):
    data = {'seller': '',
            'feed_product_type':'SHOES',
            'item_sku':'',
            'external_product_id': '',
            'external_product_id_type': 'ASIN',
            'part_number': '',
            'model': '',
            'item_name': '',
            'brand_name': '',
            'manufacturer':'',
            'product_description':'',
            'update_delete': 'update',
            'condition_type':'new',
            'standard_price':'',
            'quantity':'10',
            'product_tax_code':'',
            'product_site_launch_date':'',
            'restock_date':'',
            'sale_price':'',
            'sale_from_date':'',
            'sale_end_date':'',
            'item_package_quantity':'1',
            'offering_can_be_gift_messaged':'',
            'offering_can_be_giftwrapped':'',
            'fulfillment_latency':'20',
            'number_of_items':'',
            'merchant_shipping_group_name':'',
            'list_price_with_tax':'',
            'website_shipping_weight':'',
            'website_shipping_weight_unit_of_measure':'',
            'item_length':'',
            'item_heigth':'',
            'item_width':'',
            'item_dimensions_unit_of_measure':'IN',
            'item_weight':'',
            'item_weight_unit_of_measure':'LB',
            'bullet_point1':'',
            'bullet_point2':'',
            'bullet_point3':'',
            'bullet_point4':'',
            'bullet_point5':'',
            'recommended_browse_nodes':'',
            'generic_keywords':'',
            'style_keywords1':'',
            'style_keywords2':'',
            'style_keywords3':'',
            'main_image_url':'',
            'other_image_url1':'',
            'other_image_url2':'',
            'other_image_url3':'',
            'swatch_image_url':'',
            'parent_child':'parent',
            'parent_sku':'',
            'relationship_type':'',
            'variation_theme':'',
            'safety_warning':'',
            'legal_disclaimer_description':'',
            'strap_type':'',
            'style_name':'',
            'department_name': '',
            'outer_material_type1':'',
            'outer_material_type2':'',
            'inner_material_type1':'',
            'inner_material_type2':'',
            'material_composition':'',
            'closure_type':'',
            'lifestyle1':'',
            'lifestyle2':'',
            'lifestyle3':'',
            'seasons':'',
            'material_type1':'',
            'material_type2':'',
            'are_batteries_included':'',
            'battery_cell_composition':'',
            'lithium_battery_weight':'',
            'warranty_type':'',
            'warranty_description':'',
            'occasion_type1':'',
            'occasion_type2':'',
            'care_instructions':'',
            'sole_material':'',
            'heel_type':'',
            'toe_style':'',
            'arch_type':'',
            'color_name':'',
            'size_name':'',
            'collection_name':'',
            'sport_type':''}
    soup = BeautifulSoup(get_html(product_link), 'html5lib')
    
    try:
        brand = soup.find('a', id='brand').get('href').split('/')[1]
    except:
        brand = ' '
    with open('accepted_brand.csv', 'r') as f:
        list_ab = []
        reader = csv.reader(f)
        accepted_brands = list(reader)
        for row in accepted_brands:
            list_ab.append(row[0])
    with open('Restricted-Brands.csv', 'r') as f:
        list_rb = []
        reader = csv.reader(f)
        restricted_brands = list(reader)
        for row in restricted_brands:
            list_rb.append(row[0])
    if brand in list_ab and brand not in list_rb:
        data['brand_name'] = brand
    else: 
        return
    
    try:
        name = soup.find('span', id='productTitle').text.strip()
    except: 
        name = ''
    
    try:
        for i in soup.findAll('span', class_='a-text-bold'):
            if 'ASIN' in i.text.strip():
                ASIN = i.find_next_sibling('span').text
    except:
        ASIN = 'cant get'
    with open('Restricted-Asins.csv', 'r') as f:
        reader = csv.reader(f)
        restricted_asins = list(reader)
        list_ra = ''.join(str(x) for x in restricted_asins)
    if ASIN not in list_ra:
        data['external_product_id'] = ASIN
    else:
        return
    bullets = []
    try:
        for i in soup.find('ul', class_='a-unordered-list a-vertical a-spacing-none').findAll('li'):
            bullets.append(i.text.strip())
    except: bullets = []
    try:desc = soup.find('p').text.strip()
    except: desc = ' '  
    
    imgs = []
    for i in soup.findAll('span', class_='a-button-text'):
        a = i.find('img')
        if a != None:
            imgs.append(a['src'])
    if 'Men' or 'Boy' in name:
        department_name = 'Men'
    else:
        department_name = 'Women'
    
    data['item_name'] = name
    data['part_number'] = 'LYS' + ASIN + '-' + get_code(url)
    data['item_sku'] = 'LYS' + ASIN + '-' + get_code(url)
    data['external_product_id'] = ASIN
    data['department_name'] = department_name
    data['lifestyle1'] = 'Casual'
    data['outer_material_type1'] = "Synthetic"
    data['outer_material_type2'] = "Mesh"
    data['variation_theme'] = 'SizeName-ColorName'
    data['product_description'] = desc
    data['manufacturer'] = brand
    data['generic_keywords'] = name
    data['main_image_url'] = imgs[0]
    data['other_image_url1'] = imgs[1]
    data['other_image_url2'] = imgs[2]
    data['other_image_url3'] = imgs[3]
    data['bullet_point1'] = bullets[0]
    data['bullet_point2'] = bullets[1]
    data['bullet_point3'] = bullets[2]
    
    return list(data.values())
def get_urls_dict():
    with open('Amazon_URLS.csv') as infile:
        reader = csv.DictReader(infile)
        dict = {row['URL']:row['Script Category'] for row in reader} 
    return dict
def get_code(url):
    category = get_urls_dict().get(url)
    codes = {
                'Electronics' : 'ELECTRNCS',
                'Sports Equipment': 'SPRTSEQIP',
                'Health and Beauty': 'HLTHBTY',
                "Women's Fashion Accessories" : 'WMNFSHACCSS',
                'Toys and Games': 'TOYS',
                "Men's Fashion Shoes": 'MNFSHSHOE',
                "Other Sports Shoes": 'OTHSPRTSSHOE',
                "Women's Sports Shoes": 'WMNSPORTSHOE',
                "Men's Running Shoes": 'MNSRUNSHOE',
                "Amazon Global-Toys": 'GLBTOYS',
                "Women's Running Shoes": 'WMNRUNSHOE',
                "Women's Fashion Shoes": 'WMNFSHSHOE',
                "Computer & Accessories": 'CMPTRACCS',
                "Office Supplies" : "OFFSUPPLIES",
                "Clothing Accessories" : "CLTHACCSS",
                "TigerDirect" : "TDRCT"
                }

    return codes.get(category)
def main():
    l = [1]
    it = iter(l)
    print(next(it))
    print(next(it,'l;'))
        
        
    
if __name__ == '__main__':
    main()
