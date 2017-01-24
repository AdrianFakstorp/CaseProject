import json

rankings = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
twenty_value = [6.50, 4.75, 4.25, 3.60, 2.75, 2.20, 1.20, 1.00, 0.85, 0.75, 0.65, 0.5]
fifty_value = [10.50, 9.00, 6.00, 5.25, 4.00, 3.00, 2.75, 2.50, 2.25, 2.00, 1.75, 1.00]
sixty_value = [20.00, 10.00, 5.00, 4.50, 4.00, 3.75, 3.25, 2.75, 2.25, 2.00, 1.50, 1.00]
hundred_value = [45.00, 15.00, 11.00, 6.00, 4.75, 4.25, 3.75 , 3.25, 2.50, 2.00, 1.50, 1.00]
list_of_prize_brackets = [ {'name':'Fifty Value','data':fifty_value} ,{'name':'Sixty Value','data':sixty_value},{'name':'Hundred Value','data':hundred_value},{'name':'Twenty Value','data':twenty_value}]



def prize_zipping():
    final_prize_brackets = {}
    for brackets in list_of_prize_brackets:
        temp_dict_name = brackets['name']
        temp_dict = []
        temp_dict_final = []
        prize_ranking = {}
        total_value = {}
        total_value['Total Value'] = float(sum(brackets['data']))
        temp_dict_final.append(total_value)
        for price in brackets['data']:
            temp_dict_3 = {}
            temp_dict_2 = {}
            list_index = brackets['data'].index(price)
            #print list_index
            ranking_spot = rankings[list_index]
            value_spot = brackets['data'][list_index]
            temp_dict_2["Rank"] = ranking_spot
            temp_dict_2["Value"] = float(value_spot)
            temp_dict.append(temp_dict_2)
        prize_ranking["Prize Ranking"] = temp_dict
        temp_dict_final.append(prize_ranking)
        final_prize_brackets[temp_dict_name] = temp_dict_final
    return final_prize_brackets

asdf = {}
asdf["Prizes"] = prize_zipping()
print asdf

def price_ranking_json():
    json_name = "jsonCase Storage/price_ranking.json"
    with open(json_name, 'w') as outfile:
        json.dump(asdf, outfile)

price_ranking_json()
