import re
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse

from django.shortcuts import render, redirect

from restaurant.models import Restaurant


def view_restaurant(request, page=None):
    # 키워드 입력받음
    if request.method == "POST" or page == 2:
        keyword = request.POST['search_word']

        # 키워드를 cp949 형태로 인코딩
        cp949_keyword = keyword.encode('cp949')
        encoding_keyword = str(cp949_keyword)[2:-1].replace('\\x', '%')

        url = f'https://www.menupan.com/search/restaurant/restaurant_result.asp?sc=basicdata&kw={encoding_keyword}&page={page}'
        # image_url = f'https://www.menupan.com{image_src}'
        # link_url = f'https://www.menupan.com{link_href}'
        response = requests.get(url)
        html = BeautifulSoup(response.text)

        shop = html.select_one('ul.listStyle3')
        shop_list = shop.select('li')
        shop_list

        # 빈 딕셔너리 생성
        result_list = []

        for shop in shop_list:
            src = shop.select_one('img')['src']
            link = shop.select_one('a')['href']
            title = shop.select_one('dl a').get_text()
            category, menu = shop.select_one('dd').get_text().split(' |')
            text = shop.select_one('dd.sum').get_text().split(' | ')
            address = text[0]
            tel = text[1]

            # address, tel, none_sel = shop.select_one('dd.sum').get_text().split(' | ')

            shop_dict = {
                'title': title,
                'src': src,
                'link': link,
                'category': category,
                'menu': menu,
                'address': address,
                'tel': tel,
            }

            result_list.append(shop_dict)

        context = {
            'result_list': result_list,
            'search_word': request.POST['search_word'],
        }

        return render(request, 'index.html', context)
    else:
        return render(request, 'index.html')


def bookmark(request):
    # user = models.ManyToManyField(User)
    title = request.POST['title']
    category = request.POST['category']
    menu = request.POST['menu']
    address = request.POST['address']
    tel = request.POST['tel']
    image = request.POST['image']
    link = request.POST['link']

    restaurant = \
        Restaurant.objects.get_or_create(title=title, category=category, menu=menu, address=address, tel=tel,
                                         image=image, link=link)[0]
    restaurant.user.add(request.user)

    return HttpResponse('<script>window.onload = function(){alert("즐겨찾기에 추가되었습니다."); history.back();}</script>')


def bookmark_list(request):
    if request.user.is_authenticated:

        result_list = Restaurant.objects.filter(user=request.user)
        context = {
            'result_list': result_list
        }
        return render(request, 'restaurant/bookmark_list.html', context)
    else:
        return redirect('login')

def delete_bookmark(request, pk):
    restaurant = Restaurant.objects.get(pk=pk)
    restaurant.delete()

    return redirect('restaurant:bookmark_list')
