# Import here
from .models import *
from django.db.models import Avg, Sum, Count, Q
from django.utils import timezone
from datetime import timedelta


def young_employees(job: str):
    employees = Employee.objects.filter(
        age__lt=30,
        job=job
    )
    return employees

# SQL
# SELECT *
# FROM employee
# WHERE age < 30 AND job = 'Data Analyst';

def cheap_products():
    avg_price = Product.objects.aggregate(avg=Avg('price'))['avg']
    product_names = (
        Product.objects
        .filter(price__lt=avg_price)
        .order_by('price')
        .values_list('name', flat=True)
    )
    return product_names

# SQL
# SELECT name
# FROM (
#   SELECT p.*, AVG(price) OVER () AS global_avg
#   FROM product p
# ) x
# WHERE x.price < x.global_avg
# ORDER BY x.price ASC;

def products_sold_by_companies():
    company_sold = (
        Company.objects
        .annotate(total_sold=Sum('product__sold'))
        .values_list('name', 'total_sold')
    )
    return company_sold

# SQL
# SELECT c.name, SUM(p.sold) AS total_sold
# FROM company c
# LEFT JOIN product p ON p.company_id = c.id
# GROUP BY c.id, c.name;

def sum_of_income(start_date: str, end_date: str):
    revenue = (
        Order.objects
        .filter(time__gte=start_date, time__lte=end_date)
        .aggregate(total=Sum('price'))
    )['total'] or 0
    return revenue

# SQL
# SELECT SUM(price) AS total
# FROM "order"
# WHERE time BETWEEN TIMESTAMP '2025-08-01 00:00:00+04' AND TIMESTAMP '2025-08-31 23:59:59+04';

def good_customers():
    one_month_ago = timezone.now() - timedelta(days=30)
    gold_heavy_buyers = (
        Customer.objects
        .all()
        .annotate(
            recent_orders=Count('order', filter=Q(order__time__gte=one_month_ago))
        )
        .filter(recent_orders__gt=10)
        .values_list('name', 'phone')
    )
    return gold_heavy_buyers

# SQL
# SELECT c.name, c.phone
# FROM customer c
# JOIN (
#   SELECT customer_id, COUNT(*) AS recent_orders
#   FROM "order"
#   WHERE time >= NOW() - INTERVAL '30 days'
#   GROUP BY customer_id
# ) o ON o.customer_id = c.id
# WHERE c.level = 'gold' AND o.recent_orders > 10;

def nonprofitable_companies():
    companies_4_lt_100 = (
        Company.objects
        .annotate(
            low_sellers=Count('product', filter=Q(product__sold__lt=100))
        )
        .filter(low_sellers__gte=4)
        .values_list('name', flat=True)
    )
    return companies_4_lt_100

# SQL
# SELECT c.name
# FROM company c
# LEFT JOIN product p ON p.company_id = c.id
# GROUP BY c.id, c.name
# HAVING SUM(CASE WHEN p.sold < 100 THEN 1 ELSE 0 END) >= 4;