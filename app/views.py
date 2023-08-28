import datetime

from django.shortcuts import render, redirect
from .models import Order
from .notification import send_telegram_message

def order_list(request):
    user = request.user
    orders = Order.objects.filter(employee=user)

    if request.method == 'POST':
        order_id_to_delete = request.POST.get('order_id')
        order_to_delete = Order.objects.get(pk=order_id_to_delete)
        order_to_delete.delete()
        return redirect('order_list')
    if request.method == 'POST':
        order_id_to_delete = request.POST.get('order_id')
        order_to_delete = Order.objects.get(pk=order_id_to_delete)

        task_id = order_to_delete.task_id
        order_pk = order_to_delete.pk
        order_name = order_to_delete.name
        employee_info = f"{user.first_name} {user.employee.position}"
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        telegram_message = (
            f"Задача №{order_pk}-{task_id} під назвою {order_name} "
            f"була опрацьована {employee_info} у {current_datetime}"
        )
        send_telegram_message(telegram_message)

        order_to_delete.delete()
        return redirect('order_list')

    context = {'orders': orders}
    return render(request, 'order_list.html', context)
