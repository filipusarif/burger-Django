def is_cashier(request):
    return{'is_cashier':request.user.groups.filter(name='kasir').exists()}
def is_owner(request):
    return{'is_owner':request.user.groups.filter(name='owner').exists()}
def is_chef(request):
    return{'is_chef':request.user.groups.filter(name='chef').exists()}