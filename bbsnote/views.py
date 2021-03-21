from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Board, Comment
from django.utils import timezone
from .forms import BoardForm
from django.core.paginator import Paginator


def index(request):
    # page라는 이름으로 넘어오는게 없으면 1로 초기화
    page = request.GET.get('page', 1)
    board_list = Board.objects.order_by('-create_date')
 # 역순으로 데이터 가져옴
    # paging
    paginator = Paginator(board_list, 5)
    page_obj = paginator.get_page(page)

    context = {'board_list': page_obj}
    return render(request, 'bbsnote/board_list.html', context)


def detail(request, board_id):
    board = Board.objects.get(id=board_id)
    context = {'board': board}
    return render(request, 'bbsnote/board_detail.html', context)


def comment_create(request, board_id):
    board = Board.objects.get(id=board_id)  # 게시판정보가져옴
   # comment= Comment(board=board,content=request.POST.get('content'),create_date=timezone.now())
   # comment.save()
    board.comment_set.create(content=request.POST.get(
        'content'), create_date=timezone.now())
   # 장고에서 제공 foreign 키로 연결되어있어서 가능
    return redirect('bbsnote:detail', board_id=board.id)
    # 데이터 저장후 redirect


def board_create(request):  # post방식과 get방식 분기 처리
    if request.method == 'POST':  # POST방식일때
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.create_date = timezone.now()
            board.save()
            return redirect('bbsnote:index')
    else:  # POST 아닌경우 BoardForm 그대로
        form = BoardForm()
    return render(request, 'bbsnote/board_form.html', {'form': form})
