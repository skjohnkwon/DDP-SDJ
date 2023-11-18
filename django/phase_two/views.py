from datetime import datetime, timedelta
from django.db import connection
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Item, Comment
from phase_three.models import Favorite
from .serializers import ItemSerializer, CommentSerializer
from random import uniform
from userauth.models import User
import random
from random import choice, randint, sample
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from itertools import combinations
from threading import Lock


class style():

    RESET = '\033[0m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'

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
    
def drop_tables():
    print("\n\033[1m" + style.BRIGHT_RED + "DROPPING TABLES..." + style.RESET + "\033[0m")
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"DROP TABLE IF EXISTS phase_two_item CASCADE")
            cursor.execute(f"DROP TABLE IF EXISTS phase_two_comment CASCADE")
            cursor.execute(f"DROP TABLE IF EXISTS phase_three_favorite CASCADE")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        connection.close()

def create_tables():
    print("\033[1m" + style.BRIGHT_GREEN + "CREATING TABLES..." + style.RESET + "\033[0m")    
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
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS phase_three_favorite (
                    id serial PRIMARY KEY,
                    user_id integer REFERENCES userauth_user(id) ON DELETE CASCADE,
                    fav_user_id integer REFERENCES userauth_user(id) ON DELETE CASCADE,
                    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
                )
            """)
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        connection.close()

def get_random_date(start, end):
    time_between_dates = end - start
    random_seconds = random.randint(0, int(time_between_dates.total_seconds()))
    return start + timezone.timedelta(seconds=random_seconds)

def create_item(user, title, description, price, categories, date):

    return Item.objects.create(
        user=user, 
        title=title, 
        description=description,
        price=price, 
        categories=categories,
        created_at=date
    )

def create_comment(user, item, rating, comment_text, date):

    Comment.objects.create(
        user=user, 
        item=item, 
        rating=rating, 
        comment=comment_text,
        created_at=date
    )

def create_favorites_task(user_a, user_b, common_users):

    random_date = get_random_date(datetime(2023, 5, 1, tzinfo=timezone.utc), datetime(2023, 5, 8, tzinfo=timezone.utc))

    # Assuming Favorite is a model that records user favorites
    # Create favorite records in the database
    for common_user in common_users:
        Favorite.objects.create(user=user_a, fav_user=common_user, created_at=random_date)
        Favorite.objects.create(user=user_b, fav_user=common_user, created_at=random_date)
    # Return some indication of completion, if needed

def create_items_for_user(user):
    categories = ['Electronics', 'Books', 'Clothing', 'Toys', 'Home & Garden']
    for _ in range(randint(1, 3)):
        selected_categories = sample(categories, 2)
        item = create_item(
            user, 
            "Item " + str(randint(1, 1000)),
            "Description for item",
            randint(10, 100),
            selected_categories,
            get_random_date(datetime(2023, 5, 1, tzinfo=timezone.utc), datetime(2023, 5, 8, tzinfo=timezone.utc))
        )
        #print(f"Item created: {item.title} by {style.CYAN}{user.username}{style.RESET}")

def create_excellent_comments(pair):

    user1, user2 = pair
    # Code for creating comments for user1's items
    for item in Item.objects.filter(user=user1):
        create_comment(user2, item, 'excellent', 'Excellent product!', get_random_date(item.created_at, datetime(2023, 5, 8, tzinfo=timezone.utc)))
        #print(f"Excellent comment from {style.CYAN}{user2.username}{style.RESET} to {style.CYAN}{user1.username}{style.RESET}'s item: {item.title}")

    # Code for creating comments for user2's items
    for item in Item.objects.filter(user=user2):
        create_comment(user1, item, 'excellent', 'Outstanding quality!', get_random_date(item.created_at, datetime(2023, 5, 8, tzinfo=timezone.utc)))
        #print(f"Excellent comment from {style.CYAN}{user1.username}{style.RESET} to {style.CYAN}{user2.username}{style.RESET}'s item: {item.title}")

def create_item_and_comments(user, users_list):

    categories = ['Electronics', 'Books', 'Clothing', 'Toys', 'Home & Garden']
    # Fetch or create an item for the user
    user_items = Item.objects.filter(user=user)
    if user_items.exists():
        item = user_items.first()
    else:
        item = create_item(
            user, 
            "Item " + str(randint(1, 1000)),
            "Description for item",
            randint(10, 100),
            sample(categories, 2),
            get_random_date(datetime(2023, 5, 1, tzinfo=timezone.utc), datetime(2023, 5, 8, tzinfo=timezone.utc))
        )
        #print(f"New Item created for {style.CYAN}{user.username}{style.RESET}: {item.title}")

    # Add comments to the item
    for _ in range(5):
        commenting_user = choice(users_list)
        create_comment(
            commenting_user, 
            item, 
            'excellent', 
            'Excellent product!', 
            get_random_date(datetime(2023, 5, 1, tzinfo=timezone.utc), datetime(2023, 5, 8, tzinfo=timezone.utc))
        )
        #print(f"Excellent comment added by {style.CYAN}{commenting_user.username}{style.RESET} to {style.BRIGHT_CYAN}{user.username}{style.RESET}'s item: {item.title} ({item.id})")

def delete_and_add_poor_comments(user):
    # Delete all comments made by the user
    Comment.objects.filter(user=user).delete()
    #print(f"All comments deleted for {style.CYAN}{user.username}{style.RESET}")

    # Add three 'poor' comments to random items
    for _ in range(3):
        random_item = choice(Item.objects.all())  # Select a random item
        create_comment(
            user, 
            random_item, 
            'poor', 
            'Poor quality!', 
            get_random_date(datetime(2023, 5, 1, tzinfo=timezone.utc), datetime(2023, 5, 8, tzinfo=timezone.utc))
        )
        #print(f"Poor comment added by {style.CYAN}{user.username}{style.RESET} to item: {random_item.title} ({random_item.id})")

def gen_fake_data():

    print("\033[1m" + style.BRIGHT_CYAN + "GENGERATING DATA..." + style.RESET + "\033[0m\n")

    usernames = [f"user{n:04d}" for n in range(21)]
    users = User.objects.filter(username__in=usernames)
    categories = ['Electronics', 'Books', 'Clothing', 'Toys', 'Home & Garden']

    if users.count() < len(usernames):
        print(style.RED + "Not all users exist in the database. Please ensure the users are created before running this function." + style.RESET)
        return

    users_list = list(users)

    # Create items using multithreading
    with ThreadPoolExecutor(max_workers=10) as executor:
        list(tqdm(executor.map(create_items_for_user, users_list), total=len(users_list), desc=style.BRIGHT_MAGENTA + "Creating items" + style.RESET, ncols=100))

    users_list = list(users)

    # Select 10 random users
    selected_users = sample(users_list, 10)

    # Create items and add comments using multithreading
    with ThreadPoolExecutor(max_workers=10) as executor:
        tasks = [(user, users_list) for user in selected_users]  # Prepare tuples of arguments
        list(tqdm(executor.map(lambda args: create_item_and_comments(*args), tasks), total=len(selected_users), desc=style.BRIGHT_RED + "Creating items and adding poor comments" + style.RESET, ncols=100))

    users_list = list(users)

    assigned_favorites = {user: set() for user in users_list}
    unique_user_pairs = list(combinations(users_list, 2))
    tasks = []

    for user_a, user_b in unique_user_pairs:

        excluded_users = assigned_favorites[user_a].union(assigned_favorites[user_b])
        available_users = [user for user in users_list if user not in excluded_users and user not in (user_a, user_b)]

        if len(available_users) >= 5:
            selected_common_users = sample(available_users, 5)
        else:

            selected_common_users = available_users

        assigned_favorites[user_a].update(selected_common_users)
        assigned_favorites[user_b].update(selected_common_users)

        tasks.append((user_a, user_b, selected_common_users))

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(tqdm(executor.map(lambda p: create_favorites_task(p[0], p[1], p[2]), tasks), total=len(tasks), desc=style.BRIGHT_GREEN + "Creating favorites" + style.RESET, ncols=100))

    users_list = list(users) 

    random.shuffle(users_list)
    used_users = set()
    max_pairs = 5

    # Select user pairs while respecting the used_users and max_pairs constraints
    user_pairs = []
    for i in range(0, len(users_list) - 1, 2):
        if users_list[i] not in used_users and users_list[i + 1] not in used_users:
            user_pairs.append((users_list[i], users_list[i + 1]))
            used_users.update([users_list[i], users_list[i + 1]])
            if len(user_pairs) >= max_pairs:
                break

    # Create excellent comments using multithreading
    with ThreadPoolExecutor(max_workers=10) as executor:
        list(tqdm(executor.map(create_excellent_comments, user_pairs), total=len(user_pairs), desc=style.BRIGHT_BLUE + "Creating excellent comments" + style.RESET, ncols=100))

    users_list = list(users)

    # Pick 5 random users
    available_users = [user for user in users_list if user not in used_users]
    selected_users = sample(available_users, 5)

    # Delete comments and add new comments using multithreading
    with ThreadPoolExecutor(max_workers=5) as executor:
        list(tqdm(executor.map(delete_and_add_poor_comments, selected_users), total=len(selected_users), desc=style.BRIGHT_YELLOW + "Deleting and adding comments" + style.RESET, ncols=100))

    print(style.GREEN + "\nFake data generated successfully\n" + style.RESET)
    
@api_view(['POST'])
def init_db(request):

    drop_tables()

    create_tables()

    gen_fake_data()

    return Response({"message": "Database initialized successfully"}, status=status.HTTP_201_CREATED)