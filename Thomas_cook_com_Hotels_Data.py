#requests module will allow you to send HTTP/1.1 requests using Python. With it, you can add content like headers, form data, multipart files, and parameters via simple Python libraries. It also allows you to access the response data of Python in the same way
import requests
#csv module implements classes to read and write tabular data in CSV format
import csv
import json
import math
import time

http_proxy = "Your Proxy:Port Number"
https_proxy = "Your Proxy:Port Number"
proxies = {'http': http_proxy, 'https': https_proxy}

#User defined function for extracting a portion of string from a given string.
def get_str(resp_str,frm_str,to_str):
    start_index = resp_str.find(frm_str)+ len(frm_str)
    end_index = resp_str.find(to_str, start_index)
    resp_dict = resp_str[start_index:(end_index)]
    return resp_dict

#Assigning the searching criteria(values) for which we want to scrap Hotels information from the ThomasCook.com website.
input_dict = {
    'city': 'London',
    'country': 'United Kingdom',
    'checkIn': "21-2-2019",
    'checkOut': "28-2-2019",
    'rooms': 1,
    'adults': 2,
    'noOfNights': 7
}

#Converting the searching criteria values according to website Query String values.
CheckinDate=str(format(input_dict['checkIn'])).split("-")
StrPickupyear=CheckinDate[2]
StrPickupmnth=CheckinDate[1]
StrPickupday=CheckinDate[0]
strStartDate=StrPickupday+"/"+StrPickupmnth+"/"+StrPickupyear
# print(strStartDate)

ReturnDate=str(format(input_dict['checkOut'])).split("-")
Strreturnyear=ReturnDate[2]
Strreturnmnth=ReturnDate[1]
Strreturnday=ReturnDate[0]
strreturnDate=Strreturnday+"/"+Strreturnmnth+"/"+Strreturnyear
# print(strreturnDate)
stradult =str(format(input_dict['adults']))
noOfNights =str(format(input_dict['noOfNights']))
city =str(format(input_dict['city']))

##Hitting Destination Code page to get dynamic destination code value. So that we can search hotels for any destiation.
Dest_Code_Url = "https://www.thomascook.com/api/apim-expedia/smartfill?locationKeyword=" + city + "&productType=HOTEL&types=403&locale=en_GB"
#print(Dest_Code_Url)
Dest_Code_headers = {
    'Accept': 'application/vnd.exp-smartfill.v1+json',
    'Accept-Language': 'en-US,en;q=0.9',
    'Host': 'www.thomascook.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Connection': 'keep-alive',
    'Partner-Transaction-ID': 'ThomasCook',
    'key': '3fa0646b-067c-4e37-a2e4-12dd43848959',
    'Referer': 'https://www.thomascook.com/hotels/'
}

Dest_Code_resp = requests.get(Dest_Code_Url,proxies=proxies,headers=Dest_Code_headers,timeout=20)
Dest_Code_resp = Dest_Code_resp.text
# print("size {}".format(len(Dest_Code_resp)))

with open("Dest_Code_resp.html",'w', encoding ='utf-8') as file:
    file.write(Dest_Code_resp)

with open("Dest_Code_resp.html") as destcode:#'r', encoding ='utf-8') as destcode:
    data = json.loads(destcode.read())

# print(len(data))#2
## print(type(data))#<class 'dict'>

#Getting regionId and city values
for location in data['Locations']:
    regionId =location['Id']
    strcity =location['Keyword']
    break

temp_city=strcity
langid="2057"

#Hitting 1st List Pages url for capturing next List Page url and Hotels information.
First_List_page_Url="https://ww5.thomascook.com/Hotel-Search-Data?responsive=true&rfrr=SW-HO-CIT-" + strcity + "&regionId=" + regionId + "&startDate=" + strStartDate + "&endDate=" + strreturnDate + "&adults=" + stradult + "&paandi=true&timezoneOffset=19800000&langid=" + langid + "&hsrIdentifier=HSR&?1545171588184"
# print(First_List_page_Url)
First_List_page_headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US',
    'Host': 'ww5.thomascook.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Connection': 'Keep-Alive',
    'Referer': 'https://ww5.thomascook.com/Hotel-Search?rfrr=SW-HO-CIT-London,England,UnitedKingdom&regionId=2114&startDate=24/1/2019&endDate=31/1/2019&adults=2&paandi=true'
}
First_List_page_post=""
First_List_page_resp = requests.post(First_List_page_Url,First_List_page_post,proxies=proxies,headers=First_List_page_headers,timeout=30)
First_List_page_resp = First_List_page_resp.text

Tot_avail_Hotels_Cnt = int(get_str(First_List_page_resp, '"totalCount":', ',"'))
# print(Tot_avail_Hotels_Cnt)

#Calculating Total List Pages count.
Tot_ListPg=float(Tot_avail_Hotels_Cnt/50)
if isinstance(Tot_ListPg, float)==True:
    Tot_List_Pages = math.trunc(Tot_ListPg) + 1
    # print(Tot_List_Pages)

with open("First_List_page.html",'w', encoding ='utf-8') as file:
    file.write(First_List_page_resp)

with open("First_List_page.html",'r', encoding ='utf-8') as f:
    text = f.read()

listpage_result_dict_cut = get_str(text, 'searchResults":', ',"loyalty":{')#searchResults":

with open("Listpage_SearchResult.html",'w', encoding ='utf-8') as file:
    file.write(listpage_result_dict_cut)

with open("Listpage_SearchResult.html") as f_SearchResult:
    data = json.loads(f_SearchResult.read())

##print(len(data))#55
##print(type(data))#<class 'dict'>
##print(len(data['retailHotelModels']))
##print(data['retailHotelModels'][0]['retailHotelInfoModel'].get('searchDestination'))
##print(data['hotelCount'])#50

#Capturing a Hotels information from 1st ListPages from JSON response.
count_4_header=0
for retailHotelModels in data['retailHotelModels']:
    hotelId=retailHotelModels['retailHotelInfoModel'].get('hotelId')
    normalizedHotelName=retailHotelModels['retailHotelInfoModel'].get('normalizedHotelName')
    hotelDescription=retailHotelModels['retailHotelInfoModel'].get('hotelDescription')
    structureType=retailHotelModels['retailHotelInfoModel'].get('structureType')
    latLong=retailHotelModels['retailHotelInfoModel'].get('latLong')
    bedrooms=retailHotelModels['retailHotelInfoModel'].get('bedrooms')
    isBookable=retailHotelModels['retailHotelInfoModel'].get('isBookable')
    POOL=retailHotelModels['retailHotelInfoModel'].get('POOL')
    PRIVATE_POOL=retailHotelModels['retailHotelInfoModel'].get('PRIVATE_POOL')
    isFreeBreakfast=retailHotelModels['retailHotelInfoModel'].get('isFreeBreakfast')
    roomTypeCode=retailHotelModels['retailHotelInfoModel'].get('roomTypeCode')
    hotelBrandName=retailHotelModels['retailHotelInfoModel'].get('hotelBrandName')
    try:
        hotelStarRating = retailHotelModels['hotelStarRating']
        # print(hotelStarRating)
    except KeyError as error:
        hotelStarRating="0.0"
        # print(hotelStarRating)

    isFreeCancel=retailHotelModels['isFreeCancel']
    isPayLater=retailHotelModels['isPayLater']
    infositeUrl=retailHotelModels['infositeUrl']
    price=retailHotelModels['retailHotelPricingModel'].get('price')
    pricingStartDate=retailHotelModels['retailHotelPricingModel'].get('pricingStartDate')
    pricingEndDate=retailHotelModels['retailHotelPricingModel'].get('pricingEndDate')
    pricingNumberOfNightStay=retailHotelModels['retailHotelPricingModel'].get('pricingNumberOfNightStay')
    guestRating=retailHotelModels['ugcModel'].get('guestRating')
    if guestRating=="" or guestRating==" " or guestRating==None:
        guestRating="0.0"
    totalReviews = retailHotelModels['ugcModel'].get('totalReviews')

    #Writing all Hotel's information into csv file.
    with open("ThomasCook_Hotel_data.csv", "a", newline='') as file:
        # Defines column names into a csv file.
        field_names = ['hotelId', 'HotelName', 'hotelDescription', 'HotelType', 'latLong','bedrooms','isBookable','POOL','PRIVATE_POOL','isFreeBreakfast','roomTypeCode','hotelBrandName','hotelStarRating','isFreeCancel','isPayLater','HotelUrl','price','StartDate','EndDate','NightStay','guestRating','totalReviews']
        writer = csv.DictWriter(file, fieldnames=field_names)
        # Condition for writing header only once.
        if count_4_header == 0:
            writer.writeheader()
        count_4_header+=1
        # Writing all information in a row.
        writer.writerow(
            {
                'hotelId': hotelId,
                'HotelName': normalizedHotelName,
                'hotelDescription': hotelDescription,
                'HotelType': structureType,
                'latLong': latLong,
                'bedrooms': bedrooms,
                'isBookable': isBookable,
                'POOL': POOL,
                'PRIVATE_POOL': PRIVATE_POOL,
                'isFreeBreakfast': isFreeBreakfast,
                'roomTypeCode': roomTypeCode,
                'hotelBrandName': hotelBrandName,
                'hotelStarRating': hotelStarRating,
                'isFreeCancel': isFreeCancel,
                'isPayLater': isPayLater,
                'HotelUrl': infositeUrl,
                'price': price,
                'StartDate': pricingStartDate,
                'EndDate': pricingEndDate,
                'NightStay': pricingNumberOfNightStay,
                'guestRating': guestRating,
                'totalReviews': totalReviews

            }
        )

#Hitting 2nd and next List Pages urls
strcity=strcity.replace(" ",'+')
cnt=1
for List_page in range(2,(Tot_List_Pages+1)):

    Next_List_page_Url = "https://ww5.thomascook.com/Hotel-Search-Data?responsive=true"
    Next_List_page_headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Host': 'ww5.thomascook.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Connection': 'Keep-Alive',
        'content-type':'application/x-www-form-urlencoded; charset=UTF-8',
        'x-requested-with':'XMLHttpRequest'
    }

    #Making Post data dynamic for hitting 2nd or next List Pages.
    Next_List_page_post="destination=" + strcity + "&startDate=" + strStartDate + "&endDate=" + strreturnDate + "&adults=" + stradult + "&regionId=" + regionId + "&sort=recommended&page=" + str(List_page) + "&langid=" + langid + "&hsrIdentifier=HSR&timezoneOffset=19800000"
    # print(Next_List_page_post)
    Next_List_page_resp = requests.post(Next_List_page_Url,Next_List_page_post,proxies=proxies,headers=Next_List_page_headers,timeout=30)
    time.sleep(5)
    Next_List_page_resp = Next_List_page_resp.text

    with open("Next_List_page_resp" + str(List_page) + ".html",'w', encoding ='utf-8') as file:
        file.write(Next_List_page_resp)

    with open("Next_List_page_resp" + str(List_page) + ".html",'r', encoding ='utf-8') as ff:
        text_val = ff.read()

    Nextlistpage_result_dict_cut = get_str(text_val, 'searchResults":', ',"loyalty":{')

    with open("NextListpage_SearchResult" + str(List_page) + ".html",'w', encoding ='utf-8') as file:
        file.write(Nextlistpage_result_dict_cut)

    with open("NextListpage_SearchResult" + str(List_page) + ".html") as f_SearchResult:
        data = json.loads(f_SearchResult.read())

        # print(len(data))#55
        # print(type(data))#<class 'dict'>
        # print(len(data['retailHotelModels']))
        # print(data['retailHotelModels'][0]['retailHotelInfoModel'].get('searchDestination'))
        # print(data['hotelCount'])#50

    for retailHotelModels in data['retailHotelModels']:
        hotelId = retailHotelModels['retailHotelInfoModel'].get('hotelId')
        normalizedHotelName = retailHotelModels['retailHotelInfoModel'].get('normalizedHotelName')
        hotelDescription = retailHotelModels['retailHotelInfoModel'].get('hotelDescription')
        structureType = retailHotelModels['retailHotelInfoModel'].get('structureType')
        latLong = retailHotelModels['retailHotelInfoModel'].get('latLong')
        bedrooms = retailHotelModels['retailHotelInfoModel'].get('bedrooms')
        isBookable = retailHotelModels['retailHotelInfoModel'].get('isBookable')
        POOL = retailHotelModels['retailHotelInfoModel'].get('POOL')
        PRIVATE_POOL = retailHotelModels['retailHotelInfoModel'].get('PRIVATE_POOL')
        isFreeBreakfast = retailHotelModels['retailHotelInfoModel'].get('isFreeBreakfast')
        roomTypeCode = retailHotelModels['retailHotelInfoModel'].get('roomTypeCode')
        hotelBrandName = retailHotelModels['retailHotelInfoModel'].get('hotelBrandName')
        try:
            hotelStarRating = retailHotelModels['hotelStarRating']
            # print(hotelStarRating)
        except KeyError as error:
            hotelStarRating = "0.0"
            # print(hotelStarRating)

        isFreeCancel = retailHotelModels['isFreeCancel']
        isPayLater = retailHotelModels['isPayLater']
        infositeUrl = retailHotelModels['infositeUrl']
        price = retailHotelModels['retailHotelPricingModel'].get('price')
        pricingStartDate = retailHotelModels['retailHotelPricingModel'].get('pricingStartDate')
        pricingEndDate = retailHotelModels['retailHotelPricingModel'].get('pricingEndDate')
        pricingNumberOfNightStay = retailHotelModels['retailHotelPricingModel'].get('pricingNumberOfNightStay')
        guestRating = retailHotelModels['ugcModel'].get('guestRating')
        if guestRating == "" or guestRating == " " or guestRating == None:
            guestRating = "0.0"
        totalReviews = retailHotelModels['ugcModel'].get('totalReviews')

        # Writing all Hotel's information into csv file.
        with open("ThomasCook_Hotel_data.csv", "a", newline='') as file:
            # Defines column names into a csv file.
            field_names = ['hotelId', 'HotelName', 'hotelDescription', 'HotelType', 'latLong', 'bedrooms', 'isBookable',
                           'POOL', 'PRIVATE_POOL', 'isFreeBreakfast', 'roomTypeCode', 'hotelBrandName',
                           'hotelStarRating', 'isFreeCancel', 'isPayLater', 'HotelUrl', 'price', 'StartDate', 'EndDate',
                           'NightStay', 'guestRating', 'totalReviews']
            writer = csv.DictWriter(file, fieldnames=field_names)
            # Writing all information in a row.
            writer.writerow(
                {
                    'hotelId': hotelId,
                    'HotelName': normalizedHotelName,
                    'hotelDescription': hotelDescription,
                    'HotelType': structureType,
                    'latLong': latLong,
                    'bedrooms': bedrooms,
                    'isBookable': isBookable,
                    'POOL': POOL,
                    'PRIVATE_POOL': PRIVATE_POOL,
                    'isFreeBreakfast': isFreeBreakfast,
                    'roomTypeCode': roomTypeCode,
                    'hotelBrandName': hotelBrandName,
                    'hotelStarRating': hotelStarRating,
                    'isFreeCancel': isFreeCancel,
                    'isPayLater': isPayLater,
                    'HotelUrl': infositeUrl,
                    'price': price,
                    'StartDate': pricingStartDate,
                    'EndDate': pricingEndDate,
                    'NightStay': pricingNumberOfNightStay,
                    'guestRating': guestRating,
                    'totalReviews': totalReviews

                }
            )











