from django.shortcuts import render, get_object_or_404
from django.http import Http404
from datetime import date,datetime
from .models import record
from .forms import formdata
import calendar
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

@login_required
def home(request):
    try:
        qst=record.objects.filter(user=request.user).filter(date=date.today()).values('cost')
        sumt=0
        for a in qst:
            sumt+=(a['cost'])

        x=date.today()
        x=str(x)
        x=x[0:8]+"01"
        qsm=record.objects.filter(user=request.user).filter(date__range=[x,date.today()]).values('cost')
        summ=0
        for a in qsm:
            summ+=(a['cost'])

        context={'totalt':sumt,'totalm':summ}

        for i in range(1,13):
            x="2019-"
            if i<10:
                x+="0"+str(i)
            else:
                x+=str(i)
            x+="-"

            y=str((calendar.monthrange(2019,i))[1])
            qsm=record.objects.filter(user=request.user).filter(date__range=[x+"01",x+y]).values('cost')
            summ=0
            for a in qsm:
                summ+=(a['cost'])
            
            context["m"+str(i)]=summ

    except:
        raise Http404
    return render(request,"home.html",context)

@login_required
def addnew(request):
    form=formdata(request.POST)
    context={'form':None}
    if form.is_valid():
        data=form.cleaned_data
        print(data)
        obj=record()
        obj.info=data['info']
        obj.cost=data['cost']
        obj.user=request.user
        obj.date=str(date.today())
        obj.save()
    return render(request,"addnew.html",context)

@login_required
def monthview(request,mi):
    y=int((calendar.monthrange(2019,int(mi)))[1])+1
    context={}
    objl=[]

    for dt in range(1,y):
        t={}
        sum=0
        x="2019-"+mi
        x+="-"
        if dt<10:
            x+="0"+str(dt)
        else:
            x+=str(dt)

        try:
            qs=record.objects.filter(user=request.user).filter(date=x).values('cost')

            for a in qs:
                sum+=a['cost']
            t['date']=datetime.strptime(x, '%Y-%m-%d').date()
            t['sum']=sum
            t['d']=x
            objl.append(t)

        except:
            raise Http404
    context['objlist']=objl

    return render(request,"bymonth.html",context)

@login_required
def dateview(request,d):
    try:
        qs=record.objects.filter(user=request.user).filter(date=d)

    except:
        raise Http404
    context={'objlist':qs}
    return render(request,"bydate.html",context)

@login_required
def todayview(request):
    try:
        qs=record.objects.filter(user=request.user).filter(date=date.today())
    except:
        raise Http404
    context={'objlist':qs}
    return render(request,"bydate.html",context)

@login_required
def thismonthview(request):
    mi=str(date.today())
    mi=mi[5:7]
    x=monthview(request,mi)
    return x