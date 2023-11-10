from datetime import datetime, timedelta
from django.db import connection
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Item, Comment
from .serializers import ItemSerializer, CommentSerializer
from random import uniform
from userauth.models import User
import random

def get_random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randrange(delta.days)
    random_date = start_date + timedelta(days=random_days)
    return random_date

def count_items_today(user):
    print(f"User ID: {user.id}")

    now = timezone.now()
    start_of_day = datetime(now.year, now.month, now.day)
    end_of_day = start_of_day + timedelta(days=1)
    return Item.objects.filter(user_id=user.id, created_at__range=(start_of_day, end_of_day)).count()

def count_comments_today(user):
    print(f"User ID: {user.id}")

    now = timezone.now()
    start_of_day = datetime(now.year, now.month, now.day)
    end_of_day = start_of_day + timedelta(days=1)
    return Comment.objects.filter(user_id=user.id, created_at__range=(start_of_day, end_of_day)).count()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_item(request):
    print(request.data)
    # print(request.user)
    user = request.user
    if not user.is_authenticated:
        return Response({"message": "You are not authorized to create an item"}, status=status.HTTP_401_UNAUTHORIZED)
    
    item_count_today = count_items_today(user)
    print("item count today ", item_count_today, user.username)
    if item_count_today >= 3:
        return Response({"message": "You can only create up to 3 items per day."}, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    if request.method == 'POST':
        serializer = ItemSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Item created successfully"}, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def search(request):

    print(request.GET)
    
    entry = request.GET.get('entry', None).strip().upper()
    print(entry)
    
    if entry:
        items = Item.objects.filter(categories__icontains=entry)
        print(items)
    else:
        items = Item.objects.all()

    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request):
    
    print(request.data)

    if not request.user.is_authenticated:
        return Response({"message": "You are not authorized to create a comment"}, status=status.HTTP_401_UNAUTHORIZED)
    
    comment_count_today = count_comments_today(request.user)
    print("comment count today ", comment_count_today, request.user.username)
    if comment_count_today >= 3:
        return Response({"message": "You can only create up to 3 comments per day."}, status=status.HTTP_409_CONFLICT)
    
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        
        if serializer.is_valid():

            valid_data = serializer.validated_data
            
            # print(valid_data)
            # print("commentor", request.user.id) #perosn who is commenting
            # print("comentee", Item.objects.get(id = valid_data['item'].id).user_id) #the comment receiver
            if(request.user.id == Item.objects.get(id = valid_data['item'].id).user_id):
                print("same user")
                return Response({"message": "You can't comment on your own item"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            
            serializer.save()
            return Response({"message": "Comment created successfully"}, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "Comment created successfully"}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def create_item_test(request):
    if request.method == 'POST':
        serializer = ItemSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Item created successfully"}, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def drop_table():
    print("drop table")
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"DROP TABLE IF EXISTS phase_two_item CASCADE")
            cursor.execute(f"DROP TABLE IF EXISTS phase_two_comment CASCADE")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        connection.close()

def create_tables():
    print("create table")
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS phase_two_item (
                    id serial PRIMARY KEY,
                    user_id integer REFERENCES userauth_user(id) ON DELETE CASCADE,
                    title varchar(255),
                    description text,
                    price decimal(10,2),
                    categories text[],
                    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS phase_two_comment (
                    id serial PRIMARY KEY,
                    user_id integer REFERENCES userauth_user(id) ON DELETE CASCADE,
                    item_id integer REFERENCES phase_two_item(id) ON DELETE CASCADE,
                    rating varchar(255) DEFAULT '',
                    comment varchar(255) DEFAULT '',
                    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
                )
            """)
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        connection.close()

def gen_fake_data():

    start_date = datetime(2023, 5, 1)
    end_date = datetime(2023, 5, 8)

    categories = ['Electronics', 'Books', 'Clothing', 'Toys', 'Home & Garden']
    
    # Fetch actual User model instances assuming User model has a username field
    usernames = [f"user000{n}" for n in range(4)]
    users = User.objects.filter(username__in=usernames)
    
    # Check if we have fetched all the users
    if users.count() != len(usernames):
        print("Not all users exist in the database. Please ensure the users are created before running this function.")
        return

    for category in categories:
        for user in users:

            random_date_for_item = get_random_date(start_date, end_date)

            item = {
                'title': f'{category} Product',
                'description': f'A brief explanation of features for {category} product.',
                'price': round(uniform(10.0, 100.0), 2),
                'categories': [category],
                'user': user.id,
                'created_at': random_date_for_item,
            }

            print("item", item)

            serializer = ItemSerializer(data=item)
            if serializer.is_valid():
                serializer.save()
            else:
                print(serializer.errors) 
                
    
    ratings = ["poor", "fair", "good", "excellent"]
    
    fraction_of_items = 0.25

    for user in users:
        # Get all items and determine the fraction to comment on
        items = list(Item.objects.all())
        items_to_comment_on = random.sample(items, int(len(items) * fraction_of_items))

        for item in items_to_comment_on:

            random_date_for_item = get_random_date(start_date, end_date)

            comment = {
                'rating': random.choice(ratings),
                'comment': 'This is a test comment.',
                'item': item.id,
                'user': user.id,
                'created_at': random_date_for_item,
            }

            print("comment", comment)

            serializer = CommentSerializer(data=comment)
            if serializer.is_valid():
                # Here, we are saving the comment.
                serializer.save()
            else:
                print(serializer.errors)
    
@api_view(['POST'])
def init_db(request):

    print(request)

    drop_table()
    create_tables()

    gen_fake_data()

    return Response({"message": "Database initialized successfully"}, status=status.HTTP_201_CREATED)