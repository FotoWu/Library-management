from django.shortcuts import render, redirect, reverse, render_to_response
from django.http import HttpResponse
from library.models import User, Book, Card, Borrow

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        post = request.POST
        user = User.objects.filter(username=post['username'], password=post['password']).first()
        if user is not None:
            return render(request, 'home.html', {'username': username})
        else:
            return render(request, 'login.html', {
                'username': username,
                'password': password,
                'login_err': '用户名或密码错误!'
            })

def home(request):
    return render_to_response('home.html')

def add_book(request):
    if request.method == 'GET':
        return render_to_response('add_book.html')
    else:
        isempty = False
        if request.POST:
            post = request.POST
            post_attr_list = ['title', 'category', 'press', 'year', 'author', 'price', 'total', 'stock']
            old_book = Book.objects.filter(title=post['title']).first()
            for post_attr in post_attr_list:
                if post[post_attr] == '':
                    isempty = True
                    continue
            if isempty is False and old_book is None:
                new_book = Book(
                    title=post['title'],
                    category=post['category'],
                    press=post['press'],
                    year=post['year'],
                    author=post['author'],
                    price=post['price'],
                    total=post['total'],
                    stock=post['stock'],
                )
                new_book.save()
                add_msg = '添加成功!'
                return render(request, 'add_book.html', {'success_msg': add_msg})
            elif old_book is not None:
                add_msg = '该书已存在!'
                return render(request, 'add_book.html', {'fail_msg': add_msg})
            else:
                add_msg = '请输入图书信息!'
                return render(request, 'add_book.html', {'enter_none': add_msg})

def search(request):
    # error_msg = ''
    issearch = True
    if request.method == 'GET':
        query = request.GET.get('query')
        if query != '':
            books = list(Book.objects.filter(title__icontains=query))
            books.extend(list(Book.objects.filter(category__icontains=query)))
            books.extend(list(Book.objects.filter(press__icontains=query)))
            # books.extend(list(Book.objects.filter(year__range=query)))
            books.extend(list(Book.objects.filter(author__icontains=query)))
            # books.extend(list(Book.objects.filter(price__in=query)))
            books = list(set(books))
            if books != []:
                return render(request, 'borrow_return.html', {'books': books,
                                                              'issearch': issearch})
            else:
                error_msg = 'Query Not Found!'
                books = Book.objects.all()
                return render(request, 'borrow_return.html', {'error_msg': error_msg,
                                                              'books': books,
                                                              'issearch': issearch})
        else:
            error_msg = '请输入关键词！!'
            books = Book.objects.all()
            return render(request, 'borrow_return.html', {'error_msg': error_msg,
                                                          'books': books,
                                                          'issearch': issearch})

def borrow_return(request):
    books = Book.objects.all()
    if request.method == "GET":
        cid = request.GET.get('cid')
        if cid is None:
            return render(request, 'borrow_return.html', {'books': books})
        else:
            try:
                card = Card.objects.get(id=cid)
                book_list = Book.objects.filter(borrow__cid=cid)
                return render(request, 'borrow_return.html', {'book_list': book_list,
                                                              'books': books,
                                                              'cid': cid,
                                                              'name': card.name})
            except:
                card = None
                book_list = None
                error_card_msg = '该借书证不存在，请重新输入！'
                return render(request, 'borrow_return.html', {'book_list': book_list,
                                                              'books': books,
                                                              'cid': cid,
                                                              'error_card_msg': error_card_msg})

def borrow_book(request):
    if request.method == 'POST':
        post = request.POST
        bid = post.get('bid')
        cid = post.get('cid')
        bor = post.get('borrow_date')
        ret = post.get('return_date')
        books = Book.objects.all()
        book = Book.objects.get(id=bid)
        card = Card.objects.get(id=cid)
        book_list = Book.objects.filter(borrow__cid=cid)
        if book in book_list:
            error_msg = '该书还未归还，无法借阅！'
            return render(request, 'borrow_return.html', {'book_list': book_list,
                                                          'books': books,
                                                          'cid': cid,
                                                          'name': card.name,
                                                          'error_msg': error_msg
                                                          })
        else:
            if book.stock > 0:
                book.stock -= 1
                book.save()
                new_borrow = Borrow(
                    bid_id=book.id,
                    cid_id=card.id,
                    borrow_date=bor,
                    return_date=ret,
                    manager_id=User.objects.get().id
                )
                new_borrow.save()
                return render(request, 'borrow_return.html', {'book_list': book_list,
                                                              'books': books,
                                                              'cid': cid,
                                                              'name': card.name})
            elif book.stock <= 0:
                borrow = Borrow.objects.filter(bid=bid).first()
                error_msg = '该书库存为零，无法借阅！'
                if borrow is not None:
                    return render(request, 'borrow_return.html',
                                    {'book_list': book_list,
                                     'books': books,
                                     'cid': cid,
                                     'name': card.name,
                                     'return_date': borrow.return_date,
                                     'error_msg': error_msg})
                else:
                    return render(request, 'borrow_return.html',
                                  {'book_list': book_list,
                                   'books': books,
                                   'cid': cid,
                                   'name': card.name,
                                   'return_date': '无法找到该书最近归还时间!',
                                   'error_msg': error_msg})


def return_book(request):
    bid = request.GET.get('bid')
    cid = request.GET.get('cid')
    books = Book.objects.all()
    Borrow.objects.get(bid=bid, cid=cid).delete()
    book = Book.objects.get(id=bid)
    book.stock += 1
    book.save()
    card = Card.objects.get(id=cid)
    book_list = Book.objects.filter(borrow__cid=cid)
    return render(request, 'borrow_return.html', {'book_list': book_list,
                                                  'books': books,
                                                  'cid': cid,
                                                  'name': card.name})

def manage_card(request):
    cards = Card.objects.all()
    if request.method =='GET':
        return render(request, 'manage_card.html', {'cards': cards})
    else:
        isempty = False
        if request.POST:
            post = request.POST
            post_attr_list = ['name', 'dept', 'type']
            old_card = Card.objects.filter(name=post['name'], dept=post['dept'], type=post['type']).first()
            for post_attr in post_attr_list:
                if post[post_attr] == '':
                    isempty = True
                    continue
            if isempty is False and old_card is None:
                new_card = Card(
                    name=post['name'],
                    dept=post['dept'],
                    type=post['type'],
                )
                new_card.save()
                success_msg = '添加成功'
                return render(request, 'manage_card.html', {'cards': cards,
                                                            'success_msg': success_msg})
            elif old_card is not None:
                error_msg = '该借书证已存在'
                return render(request, 'manage_card.html', {'cards': cards,
                                                            'error_msg': error_msg})
            else:
                error_msg = '请输入借书证信息'
                return render(request, 'manage_card.html', {'cards': cards,
                                                            'error_msg': error_msg})

def delete_card(request):
    cid = request.GET.get('cid')
    Card.objects.filter(id=cid).delete()
    return redirect('manage_card')