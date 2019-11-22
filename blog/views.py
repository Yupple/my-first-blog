from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post, Comment
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CommentForm
from django.shortcuts import redirect, render
from django.http import HttpResponse
import itertools



def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)



def hello_get_query(request):

    addresses = {264:'「大皿（264円）」',308:'「大皿（308円）」',330:' 「大皿or麺類（330円）」',99:'「小鉢orスイーツ（99円）」',154:'「小鉢orスイーツ（154円）」',143:'「クリームケーキ（143円）」',110:'「小鉢（121円）」',176:'「サバの味噌煮（176円）」',121:'「小鉢orスイーツ（121円）」',253:'「野菜南蛮あんかけ（253円）」',88:'「小鉢（88円）」',55:'「納豆（55円）」',66:'「エッグマカロニサラダ(66円)」',71:'「豆腐（71円）」',484:'「白味噌ラーメン（484円）」',616:'「サーモンいくら丼M（616円）」',594:'「サーモンいくら丼S（594円）」',418:'「麺類（418円）」',313:'「醤油ラーメン（313円）」',231:'「麺類（231円）」',275:'「麺類orスイーツ（275円）」',245:'「カレーライスM（245円）」',317:'「カラーライスL（317円）」',167:'「カレーライスS（167円）」',400:'「カツカレーM（400円）」',473:'「カツカレーL(473円)」',244:'「カツカレーS（244円）」',396:'「ハヤシライスM（396円）」',341:'「ハヤシライスS(341円)」',134:'「ライスL（134円）」',106:'「ライスM(106円)」',93:'「ライスS（93円）」',72:'「ライスSS（72円）」',57:'「ライスプチ（57円）」',33:'「味噌汁（33円）」'}
    a = list()
    a1 = list()
    a2 = list()
    m = 0
    item =0
    if request.POST.get('wan') is  None or request.POST.get('tu') is None :
        answer = '数字を入れてください'
        conbi = list()
    else:
        m = int(request.POST.get('wan'))
        item = int(request.POST.get('tu'))
       
        
    if item == 1:
        for d  in itertools.combinations_with_replacement(addresses,item):
            if sum(d) == m:
                
                e = addresses[d[0]]
                
                a1.append(e)
            
                
        if len(a1) > 0:
            answer = '合計'+ str(m) +'円の組みはこちら'
            conbi = a1

        else:
            for d  in itertools.combinations_with_replacement(addresses,item):
                if sum(d) == m - 1:
                    
                    e = addresses[d[0]]
                
                    a2.append(e)
                

            if len(a2) > 0:
                answer = str(m)+'円の組み合わせはありません。合計'+str(m - 1) +'円の全ての組みはこちら'
                conbi = a2
            

            else:
                for n in range(2,300):
                    for d  in itertools.combinations_with_replacement(addresses,item):
                        if sum(d) == m - n:
                            
                            e = addresses[d[0]]
                        
                            a.append(e)
                            
                    
                    if len(a) > 0:
                    
                        answer = str(m) +'円から'+str(m - n+1)+'円までの組み合わせはありません。合計'+ str(m - n) +'円の全ての組みはこちら'
                        conbi = a
                        break

                else:
                    answer = '金額を変えてください。'
                    conbi = list()

    elif item == 2:
        for d  in itertools.combinations_with_replacement(addresses,item):
            if sum(d) == m:
                
                e = addresses[d[0]]+ 'と' + addresses[d[1]]
                
                a1.append(e)
            
                
        if len(a1) > 0:
            answer = '合計'+str(m)+'円の組みはこちら'
            conbi = a1

        else:
            for d  in itertools.combinations_with_replacement(addresses,item):
                if sum(d) == m - 1:
                    
                    e = addresses[d[0]]+ 'と' + addresses[d[1]]
                
                    a2.append(e)
                

            if len(a2) > 0:
                answer = str(m)+'円の組み合わせはありません。合計'+str(m - 1) +'円の全ての組みはこちら'
                conbi = a2
        

            else:
                for n in range(2,300):
                    for d  in itertools.combinations_with_replacement(addresses,item):
                        if sum(d) == m - n:
                            
                            e = addresses[d[0]]+ 'と' + addresses[d[1]]
                        
                            a.append(e)
                            
                    
                    if len(a) > 0:
                    
                        answer = str(m)+'円から'+str(m - n+1)+'円までの組み合わせはありません。合計'+str(m - n)+ '円の全ての組みはこちら'
                        conbi = a
                        break

                else:
                    answer ='金額を変えてください。'
                    conbi = list()

    elif item == 3:
        for d  in itertools.combinations_with_replacement(addresses,item):
            if sum(d) == m:
                
                e = addresses[d[0]]+ 'と' + addresses[d[1]]+ 'と' + addresses[d[2]]
                
                a1.append(e)
            
                
        if len(a1) > 0:
            answer = '合計'+str(m)+'円の組みはこちら'
            conbi = a1

        else:
            for d  in itertools.combinations_with_replacement(addresses,item):
                if sum(d) == m - 1:
                    
                    e = addresses[d[0]]+ 'と' + addresses[d[1]]+ 'と' + addresses[d[2]]
                
                    a2.append(e)
                

            if len(a2) > 0:
                answer = str(m)+'円の組み合わせはありません。合計'+str(m - 1)+'円の全ての組みはこちら'
                conbi= a2
            

            else:
                for n in range(2,300):
                    for d  in itertools.combinations_with_replacement(addresses,item):
                        if sum(d) == m - n:
                            
                            e = addresses[d[0]]+ 'と' + addresses[d[1]]+ 'と' + addresses[d[2]]
                        
                            a.append(e)
                            
                    
                    if len(a) > 0:
                    
                        answer = str(m)+'円から'+str(m - n+1)+'円までの組み合わせはありません。合計'+str(m - n)+'円の全ての組みはこちら'
                        conbi=a
                        break

                else:
                    answer='金額を変えてください。'
                    conbi = list()


    elif item == 4:
        for d  in itertools.combinations_with_replacement(addresses,item):
            if sum(d) == m:
                
                e = addresses[d[0]]+ 'と' + addresses[d[1]]+ 'と' + addresses[d[2]]+ 'と' + addresses[d[3]]
                
                a1.append(e)
            
                
        if len(a1) > 0:
            answer ='合計'+str(m)+'円の組みはこちら'
            conbi = a1

        else:
            for d  in itertools.combinations_with_replacement(addresses,item):
                if sum(d) == m - 1:
                    
                    e = addresses[d[0]]+ 'と' + addresses[d[1]]+ 'と' + addresses[d[2]]+ 'と' + addresses[d[3]]
                
                    a2.append(e)
                

            if len(a2) > 0:
                answer = str(m)+'円の組み合わせはありません。合計'+ str(m - 1)+'円の全ての組みはこちら'
                conbi =a2
            

            else:
                for n in range(2,300):
                    for d  in itertools.combinations_with_replacement(addresses,item):
                        if sum(d) == m - n:
                            
                            e = addresses[d[0]]+ 'と' + addresses[d[1]]+ 'と' + addresses[d[2]]+ 'と' + addresses[d[3]]
                        
                            a.append(e)
                            
                    
                    if len(a) > 0:
                    
                        answer = str(m)+'円から'+str(m - n+1)+'円までの組み合わせはありません。合計'+str(m - n)+'円の全ての組みはこちら'
                        conbi=a
                        break

                else:
                    answer='金額を変えてください。'
                    conbi = list()


    elif item == 5:
        for d  in itertools.combinations_with_replacement(addresses,item):
            if sum(d) == m:
                
                e = addresses[d[0]]+ 'と' + addresses[d[1]]+ 'と' + addresses[d[2]]+ 'と' + addresses[d[3]]+ 'と' + addresses[d[4]]
                
                a1.append(e)
            
                
        if len(a1) > 0:
            answer = '合計'+str(m)+ '円の組みはこちら'
            conbi=a1

        else:
            for d  in itertools.combinations_with_replacement(addresses,item):
                if sum(d) == m - 1:
                    
                    e = addresses[d[0]]+ 'と' + addresses[d[1]]+ 'と' + addresses[d[2]]+ 'と' + addresses[d[3]]+ 'と' + addresses[d[4]]
                
                    a2.append(e)
                

            if len(a2) > 0:
                answer=str(m)+'円の組み合わせはありません。合計'+str(m - 1) +'円の全ての組みはこちら'
                answer=a2
            

            else:
                for n in range(2,300):
                    for d  in itertools.combinations_with_replacement(addresses,item):
                        if sum(d) == m - n:
                            
                            e = addresses[d[0]]+ 'と' + addresses[d[1]]+ 'と' + addresses[d[2]]+ 'と' + addresses[d[3]]+ 'と' + addresses[d[4]]
                        
                            a.append(e)
                            
                    
                    if len(a) > 0:
                    
                        answer = str(m)+'円から'+str(m - n+1)+'円までの組み合わせはありません。合計'+str(m - n)+'円の全ての組みはこちら'
                        conbi=a
                        break

                else:
                    answer='mの数値を変えてください。'
                    conbi = list()


    elif item == 6:
        for d  in itertools.combinations_with_replacement(addresses,item):
            if sum(d) == m:
                
                e = addresses[d[0]]+ 'と' + addresses[d[1]]+ 'と' + addresses[d[2]]+ 'と' + addresses[d[3]]+ 'と' + addresses[d[4]]+ 'と' + addresses[d[5]]
                
                a1.append(e)
            
                
        if len(a1) > 0:
            answer ='合計'+str(m) +'円の組みはこちら'
            conbi=a1

        else:
            for d  in itertools.combinations_with_replacement(addresses,item):
                if sum(d) == m - 1:
                    
                    e = addresses[d[0]]+ 'と' + addresses[d[1]]+ 'と' + addresses[d[2]]+ 'と' + addresses[d[3]]+ 'と' + addresses[d[4]]+ 'と' + addresses[d[5]]
                
                    a2.append(e)
                

            if len(a2) > 0:
                answer=str(m)+'円の組み合わせはありません。合計'+str(m - 1)+'円の全ての組みはこちら'
                conbi=a2
            

            else:
                for n in range(2,300):
                    for d  in itertools.combinations_with_replacement(addresses,item):
                        if sum(d) == m - n:
                            
                            e = addresses[d[0]]+ 'と' + addresses[d[1]]+ 'と' + addresses[d[2]]+ 'と' + addresses[d[3]]+ 'と' + addresses[d[4]]+ 'と' + addresses[d[5]]
                        
                            a.append(e)
                            
                    
                    if len(a) > 0:
                    
                        answer= str(m)+ '円から'+str(m - n+1)+'円までの組み合わせはありません。合計'+str(m - n)+ '円の全ての組みはこちら'
                        conbi=a
                        break

                else:
                    answer ='金額を変えてください。'
                    conbi = list()


    elif item == 7:
        for d  in itertools.combinations_with_replacement(addresses,item):
            if sum(d) == m:
                
                e = addresses[d[0]]+ 'と' + addresses[d[1]]+ 'と' + addresses[d[2]]+ 'と' + addresses[d[3]]+ 'と' + addresses[d[4]]+ 'と' + addresses[d[5]]+ 'と' + addresses[d[6]]
                
                a1.append(e)
            
                
        if len(a1) > 0:
            answer ='合計'+ str(m)+ '円の組みはこちら'
            conbi=a1

        else:
            for d  in itertools.combinations_with_replacement(addresses,item):
                if sum(d) == m - 1:
                    
                    e = addresses[d[0]]+ 'と' + addresses[d[1]]+ 'と' + addresses[d[2]]+ 'と' + addresses[d[3]]+ 'と' + addresses[d[4]]+ 'と' + addresses[d[5]]+ 'と' + addresses[d[6]]
                
                    a2.append(e)
                

            if len(a2) > 0:
                answer=str(m)+'円の組み合わせはありません。合計'+str(m - 1)+ '円の全ての組みはこちら'
                conbi=a2
            

            else:
                for n in range(2,300):
                    for d  in itertools.combinations_with_replacement(addresses,item):
                        if sum(d) == m - n:
                            
                            e = addresses[d[0]]+ 'と' + addresses[d[1]]+ 'と' + addresses[d[2]]+ 'と' + addresses[d[3]]+ 'と' + addresses[d[4]]+ 'と' + addresses[d[5]]+ 'と' + addresses[d[6]]
                        
                            a.append(e)
                            
                    
                    if len(a) > 0:
                    
                        answer=str(m)+ '円から'+str(m - n+1)+'円までの組み合わせはありません。合計'+str(m - n)+ '円の全ての組みはこちら'
                        conbi=a
                        break

                else:
                    answer='金額を変えてください。'
                    conbi = list()

    elif item == 8:
        for d  in itertools.combinations_with_replacement(addresses,item):
            if sum(d) == m:
                
                e = addresses[d[0]]+ 'と' + addresses[d[1]]+ 'と' + addresses[d[2]]+ 'と' + addresses[d[3]]+ 'と' + addresses[d[4]]+ 'と' + addresses[d[5]]+ 'と' + addresses[d[6]]+ 'と' + addresses[d[7]]
                
                a1.append(e)
            
                
        if len(a1) > 0:
            answer ='合計'+str(m)+'円の組みはこちら'
            conbi=a1

        else:
            for d  in itertools.combinations_with_replacement(addresses,item):
                if sum(d) == m - 1:
                    
                    e = addresses[d[0]]+ 'と' + addresses[d[1]]+ 'と' + addresses[d[2]]+ 'と' + addresses[d[3]]+ 'と' + addresses[d[4]]+ 'と' + addresses[d[5]]+ 'と' + addresses[d[6]]+ 'と' + addresses[d[7]]
                
                    a2.append(e)
                

            if len(a2) > 0:
                answer=str(m)+'円の組み合わせはありません。合計'+str(m - 1)+'円の全ての組みはこちら'
                conbi=a2
            

            else:
                for n in range(2,300):
                    for d  in itertools.combinations_with_replacement(addresses,item):
                        if sum(d) == m - n:
                            
                            e = addresses[d[0]]+ 'と' + addresses[d[1]]+ 'と' + addresses[d[2]]+ 'と' + addresses[d[3]]+ 'と' + addresses[d[4]]+ 'と' + addresses[d[5]]+ 'と' + addresses[d[6]]+ 'と' + addresses[d[7]]
                        
                            a.append(e)
                            
                    
                    if len(a) > 0:
                    
                        answer= str(m)+ '円から'+str(m - n+1)+'円までの組み合わせはありません。合計'+str(m - n)+'円の全ての組みはこちら'
                        conbi=a
                        break

                else:
                    answer='金額を変えてください。'
                    conbi = list()

    elif item == 9:
        for d  in itertools.combinations_with_replacement(addresses,item):
            if sum(d) == m:
                
                e = addresses[d[0]]+ 'と' + addresses[d[1]]+ 'と' + addresses[d[2]]+ 'と' + addresses[d[3]]+ 'と' + addresses[d[4]]+ 'と' + addresses[d[5]]+ 'と' + addresses[d[6]]+ 'と' + addresses[d[7]]+ 'と' + addresses[d[8]]
                
                a1.append(e)
            
                
        if len(a1) > 0:
            answer='合計'+str(m)+'円の組みはこちら'
            conbi=a1

        else:
            for d  in itertools.combinations_with_replacement(addresses,item):
                if sum(d) == m - 1:
                    
                    e = addresses[d[0]]+ 'と' + addresses[d[1]]+ 'と' + addresses[d[2]]+ 'と' + addresses[d[3]]+ 'と' + addresses[d[4]]+ 'と' + addresses[d[5]]+ 'と' + addresses[d[6]]+ 'と' + addresses[d[7]]+ 'と' + addresses[d[8]]
                
                    a2.append(e)
                

            if len(a2) > 0:
                answer=str(m)+'円の組み合わせはありません。合計'+str(m - 1)+'円の全ての組みはこちら'
                conbi=a2
            

            else:
                for n in range(2,300):
                    for d  in itertools.combinations_with_replacement(addresses,item):
                        if sum(d) == m - n:
                            
                            e = addresses[d[0]]+ 'と' + addresses[d[1]]+ 'と' + addresses[d[2]]+ 'と' + addresses[d[3]]+ 'と' + addresses[d[4]]+ 'と' + addresses[d[5]]+ 'と' + addresses[d[6]]+ 'と' + addresses[d[7]]+ 'と' + addresses[d[8]]
                        
                            a.append(e)
                            
                    
                    if len(a) > 0:
                    
                        answer=str(m)+ '円から'+str(m - n+1)+'円までの組み合わせはありません。合計'+str(m - n)+ '円の全ての組みはこちら'
                        conbi=a
                        break

                else:
                    answer='金額を変えてください。'
                    conbi=list()

    elif item == 10:
        for d  in itertools.combinations_with_replacement(addresses,item):
            if sum(d) == m:
                
                e = addresses[d[0]]+ 'と' + addresses[d[1]]+ 'と' + addresses[d[2]]+ 'と' + addresses[d[3]]+ 'と' + addresses[d[4]]+ 'と' + addresses[d[5]]+ 'と' + addresses[d[6]]+ 'と' + addresses[d[7]]+ 'と' + addresses[d[8]]+ 'と' + addresses[d[9]]
                
                a1.append(e)
            
                
        if len(a1) > 0:
            answer='合計'+str(m)+'円の組みはこちら'
            conbi=a1

        else:
            for d  in itertools.combinations_with_replacement(addresses,item):
                if sum(d) == m - 1:
                    
                    e = addresses[d[0]]+ 'と' + addresses[d[1]]+ 'と' + addresses[d[2]]+ 'と' + addresses[d[3]]+ 'と' + addresses[d[4]]+ 'と' + addresses[d[5]]+ 'と' + addresses[d[6]]+ 'と' + addresses[d[7]]+ 'と' + addresses[d[8]]+ 'と' + addresses[d[9]]
                
                    a2.append(e)
                

            if len(a2) > 0:
                answer=str(m)+'円の組み合わせはありません。合計'+str(m - 1)+'円の全ての組みはこちら'
                conbi=a2
            
            else:
                for n in range(2,300):
                    for d  in itertools.combinations_with_replacement(addresses,item):
                        if sum(d) == m - n:
                            
                            e = addresses[d[0]]+ 'と' + addresses[d[1]]+ 'と' + addresses[d[2]]+ 'と' + addresses[d[3]]+ 'と' + addresses[d[4]]+ 'と' + addresses[d[5]]+ 'と' + addresses[d[6]]+ 'と' + addresses[d[7]]+ 'と' + addresses[d[8]]+ 'と' + addresses[d[9]]
                        
                            a.append(e)
                            
                    
                    if len(a) > 0:
                    
                        answer=str(m)+ '円から'+str(m - n+1)+'円までの組み合わせはありません。合計'+str(m - n)+'円の全ての組みはこちら'
                        conbi=a
                        break

                else:
                    answer='金額を変えてください。'
                    conbi=list()
    elif item == 0 or m == 0:
        answer ='数字を入れてください'
        conbi=list()
    else:
        answer='品数を変更してください。'
        conbi = list()



    d = {
        'yon': answer,
        'go': conbi
        

    }
    return render(request, 'blog/get_query.html', d)


