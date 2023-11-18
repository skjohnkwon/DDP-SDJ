from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from phase_two.models import Item, Comment
from django.db.models import Count
from userauth.models import User
from django.db.models import Count, Q
from .serializer import FavoriteSerializer
from .models import Favorite
from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

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

@api_view(['GET'])
def send_list_of_users_excluding_admin_and_current_user(request):
    users = User.objects.all()
    user_list = []

    for user in users:
        if user.username != 'admin' and user.username != request.user.username:
            entry = [user.username, user.id]
            user_list.append(entry)

    user_list.sort()

    return Response({"users": user_list}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favorite(request):
    print(request.data)

    if not request.user.is_authenticated:
        return Response({"message": "You are not authorized to create a comment"}, status=status.HTTP_401_UNAUTHORIZED)
    
    if request.method == 'POST':
        serializer = FavoriteSerializer(data=request.data)
        
        if serializer.is_valid():
            valid_data = serializer.validated_data
            print(valid_data)

            # Check for duplicate favorites
            user = request.user
            fav_user_id = valid_data.get('fav_user').id

            # Query to check if this favorite already exists
            if Favorite.objects.filter(user=user, fav_user_id=fav_user_id).exists():
                return Response({"message": "This favorite already exists"}, status=status.HTTP_409_CONFLICT)

            serializer.save()
            return Response({"message": "Added favorite user successfully"}, status=status.HTTP_201_CREATED)
        
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def q10(request):
    print(style.RED + "\nQ10" + style.RESET)
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT u1.username, u2.username
            FROM userauth_user AS u1
            JOIN phase_two_item AS i1 ON u1.id = i1.user_id
            JOIN phase_two_comment AS c1 ON i1.id = c1.item_id AND c1.rating = 'excellent'
            JOIN userauth_user AS u2 ON c1.user_id = u2.id
            WHERE u1.id < u2.id
            AND NOT EXISTS (
                SELECT 1
                FROM phase_two_item AS i2
                LEFT JOIN phase_two_comment AS c2 ON i2.id = c2.item_id AND c2.user_id = u1.id
                WHERE i2.user_id = u2.id AND (c2.rating != 'excellent' OR c2.rating IS NULL)
            )
            AND NOT EXISTS (
                SELECT 1
                FROM phase_two_item AS i3
                LEFT JOIN phase_two_comment AS c3 ON i3.id = c3.item_id AND c3.user_id = u2.id
                WHERE i3.user_id = u1.id AND (c3.rating != 'excellent' OR c3.rating IS NULL)
            );
        """)
        user_pairs = cursor.fetchall()

    for pair in user_pairs:
        print(style.BRIGHT_GREEN + f"User1: {pair[0]}" + style.RESET)
        print(style.BRIGHT_CYAN + f"User2: {pair[1]}" + style.RESET + "\n")

    return Response({"answer": user_pairs}, status=status.HTTP_200_OK)

@api_view(['GET'])
def q9(request):
    print(style.RED + "\nQ9" + style.RESET)
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT u.username
            FROM userauth_user u
            LEFT JOIN phase_two_item i ON u.id = i.user_id
            LEFT JOIN phase_two_comment c ON i.id = c.item_id
            WHERE u.username != 'admin'
            GROUP BY u.id
            HAVING COUNT(c.id) FILTER (WHERE c.rating = 'poor') = 0
        """)
        users_without_poor_reviews = cursor.fetchall()

    answer_array = [user[0] for user in users_without_poor_reviews]

    for username in answer_array:
        print(f"\nUser: {style.CYAN}{username}{style.RESET}")
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, title
                FROM phase_two_item
                WHERE user_id = (SELECT id FROM userauth_user WHERE username = %s)
            """, [username])
            items = cursor.fetchall()

            for item_id, item_title in items:
                print(f"  Item ID: {item_id}, Title: {style.BRIGHT_CYAN}{item_title}{style.RESET}")

                cursor.execute("""
                    SELECT comment
                    FROM phase_two_comment
                    WHERE item_id = %s
                """, [item_id])
                comments = cursor.fetchall()

                for comment in comments:
                    comment_text = comment[0]
                    comment_str = comment_text if comment_text else 'None'
                    print(f"    Comment: {comment_str}")

    return Response({"answer": answer_array}, status=status.HTTP_200_OK)

@api_view(['GET'])
def q8(request):
    print(style.RED + "\nQ8" + style.RESET)
    
    # Query to find users who have only posted 'poor' reviews
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT u.username
            FROM userauth_user u
            JOIN phase_two_comment c ON u.id = c.user_id
            GROUP BY u.id
            HAVING COUNT(c.id) > 0
            AND COUNT(c.id) FILTER (WHERE c.rating != 'poor') = 0
        """)
        users_all_poor_reviews = cursor.fetchall()

    answer_array = [user[0] for user in users_all_poor_reviews]

    # Print all users from answer_array and their comments
    for username in answer_array:
        print(f"\nUser: {style.CYAN}{username}{style.RESET}")
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT i.title, c.comment
                FROM phase_two_comment c
                INNER JOIN phase_two_item i ON c.item_id = i.id
                WHERE c.user_id = (SELECT id FROM userauth_user WHERE username = %s)
            """, [username])
            comments = cursor.fetchall()

            for comment in comments:
                item_title, comment_text = comment
                comment_str = comment_text if comment_text else 'None'
                print(f"  Item: {style.BRIGHT_CYAN}{item_title}{style.RESET}, Comment: {comment_str}")

    return Response({"answer": answer_array}, status=status.HTTP_200_OK)

@api_view(['GET'])
def q7(request): 
    print(style.RED + "\nQ7" + style.RESET)

    # Query to find users who never posted a 'poor' review
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT u.username
            FROM userauth_user u
            WHERE u.username != 'admin'
            AND NOT EXISTS (
                SELECT 1
                FROM phase_two_comment c
                WHERE c.user_id = u.id AND c.rating = 'poor'
            )
        """)
        rows = cursor.fetchall()

    answer_array = [row[0] for row in rows]

    for username in answer_array:
        print(f"\nUser: {style.CYAN}{username}{style.RESET}")
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT i.title, c.comment
                FROM phase_two_comment c
                INNER JOIN phase_two_item i ON c.item_id = i.id
                WHERE c.user_id = (SELECT id FROM userauth_user WHERE username = %s)
            """, [username])
            comments = cursor.fetchall()

            for comment in comments:
                item_title, comment_text = comment
                comment_str = comment_text if comment_text else 'None'
                print(f"  Item: {style.BRIGHT_CYAN}{item_title}{style.RESET}, Comment: {comment_str}")

    return Response({"answer": answer_array})

@api_view(['GET'])
def q6(request): 
    print(style.RED + "\nQ6" + style.RESET)

    # Query to find users who never posted an 'excellent' item
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT u.username
            FROM userauth_user u
            WHERE u.username != 'admin'
            AND NOT EXISTS (
                SELECT 1
                FROM phase_two_item i
                INNER JOIN phase_two_comment c ON i.id = c.item_id
                WHERE i.user_id = u.id AND c.rating = 'excellent'
                GROUP BY i.id
                HAVING COUNT(*) >= 3
            )
        """)
        users_without_excellent = cursor.fetchall()

    # Query to find users who have posted at least one 'excellent' item
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT u.username
            FROM userauth_user u
            JOIN phase_two_item i ON u.id = i.user_id
            JOIN phase_two_comment c ON i.id = c.item_id
            WHERE u.username != 'admin' AND c.rating = 'excellent'
            GROUP BY i.id, u.username
            HAVING COUNT(c.rating) >= 3
        """)
        users_with_excellent = cursor.fetchall()

    # Print and process users without excellent items
    answer_array_without = [user[0] for user in users_without_excellent]
    for username in answer_array_without:
        print(f"{style.RED}\nUser Without Excellent Items:{style.RESET} {style.CYAN}{username}{style.RESET}")
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, title
                FROM phase_two_item
                WHERE user_id = (SELECT id FROM userauth_user WHERE username = %s)
            """, [username])
            items = cursor.fetchall()

            for item_id, item_title in items:
                print(f"  Item ID: {item_id}, Title: {style.BRIGHT_CYAN}{item_title}{style.RESET}")

                cursor.execute("""
                    SELECT comment
                    FROM phase_two_comment
                    WHERE item_id = %s
                """, [item_id])
                comments = cursor.fetchall()

                for comment in comments:
                    comment_text = comment[0]
                    comment_str = comment_text if comment_text else 'None'
                    print(f"    Comment: {comment_str}")

    # Print and process users with excellent items
    for username in [user[0] for user in users_with_excellent]:
        print(f"{style.BRIGHT_GREEN}\nUser With Excellent Items:{style.RESET} {style.CYAN}{username}{style.RESET}")
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, title
                FROM phase_two_item
                WHERE user_id = (SELECT id FROM userauth_user WHERE username = %s)
            """, [username])
            items = cursor.fetchall()

            for item_id, item_title in items:
                print(f"  Item ID: {item_id}, Title: {style.BRIGHT_CYAN}{item_title}{style.RESET}")

                cursor.execute("""
                    SELECT comment
                    FROM phase_two_comment
                    WHERE item_id = %s
                """, [item_id])
                comments = cursor.fetchall()

                for comment in comments:
                    comment_text = comment[0]
                    comment_str = comment_text if comment_text else 'None'
                    print(f"    Comment: {comment_str}")

    return Response({"answer": answer_array_without}, status=status.HTTP_200_OK)

@api_view(['GET'])
def q5(request):
    userX = request.query_params.get('userX')
    userY = request.query_params.get('userY')

    # Debugging: Print userX and userY
    print(f"{style.RED}userX: {style.RESET}{style.CYAN}{userX}{style.RESET}, {style.RED}userY: {style.RESET}{style.CYAN}{userY}{style.RESET}")

    # Define the SQL query to find mutual favorite users
    sql_query = f"""
        SELECT DISTINCT u.username
        FROM userauth_user u
        INNER JOIN (
            SELECT fav_user_id
            FROM phase_three_favorite
            WHERE user_id = {userX}
            INTERSECT
            SELECT fav_user_id
            FROM phase_three_favorite
            WHERE user_id = {userY}
        ) AS mutual_favorites ON u.id = mutual_favorites.fav_user_id
    """

    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        mutual_favorite_usernames = [row[0] for row in cursor.fetchall()]

        # For each user in mutual_favorite_usernames, print all of their favorites
        for username in mutual_favorite_usernames:
            
            cursor.execute("""
                SELECT fav_user.username
                FROM phase_three_favorite
                INNER JOIN userauth_user fav_user ON phase_three_favorite.fav_user_id = fav_user.id
                WHERE phase_three_favorite.user_id = (
                    SELECT id FROM userauth_user WHERE username = %s
                )
            """, [username])
            favorites = [fav_row[0] for fav_row in cursor.fetchall()]

            print(f"{style.BRIGHT_CYAN}User: {username}{style.RESET}")
            print(f"  {style.YELLOW}Favorite: {favorites}{style.RESET}")

    return Response({"answer": mutual_favorite_usernames}, status=status.HTTP_200_OK)

@api_view(['GET'])
def q4(request):
    print(style.RED + "\nQ4" + style.RESET)

    with connection.cursor() as cursor:
        # Find the maximum number of posts by any user on the specified date
        cursor.execute("""
            SELECT MAX(post_count) FROM (
                SELECT COUNT(*) as post_count
                FROM phase_two_item
                WHERE DATE(created_at) = '2023-05-01'  -- Cast the timestamp to date
                GROUP BY user_id
            ) AS subquery
        """)
        max_post_count = cursor.fetchone()[0]

        if max_post_count is not None:
            # Find all users who have made that number of posts on the specified date
            cursor.execute("""
                SELECT u.username, COUNT(*) as post_count
                FROM userauth_user u
                JOIN phase_two_item i ON u.id = i.user_id
                WHERE DATE(i.created_at) = '2023-05-01'  -- Cast the timestamp to date
                GROUP BY u.username
                HAVING COUNT(*) = %s
                ORDER BY post_count DESC, u.username
            """, [max_post_count])
            top_posters = cursor.fetchall()
        else:
            top_posters = []

    for x in top_posters:
        print(f"User: {style.CYAN}{x[0]}{style.RESET}, Number of Posts: {style.BRIGHT_GREEN}{x[1]}{style.RESET}")

    return Response({"answer": top_posters}, status=status.HTTP_200_OK)

@api_view(['GET'])
def q3(request):

    requested_user_id = request.query_params.get('user')
    
    if not requested_user_id:
        return Response({"error": "User parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    print(style.RED + "\nQ3" + style.RESET)
    print(f"Requested User ID: {style.CYAN}{requested_user_id}{style.RESET}")

    with connection.cursor() as cursor:

        cursor.execute("""
            SELECT id FROM userauth_user WHERE id = %s
        """, [requested_user_id])
        if not cursor.fetchone():
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        cursor.execute("""
            SELECT id, title
            FROM phase_two_item
            WHERE user_id = %s
        """, [requested_user_id])
        items = cursor.fetchall()

        valid_items = []

        for item_id, item_title in items:
            cursor.execute("""
                SELECT comment, rating
                FROM phase_two_comment
                WHERE item_id = %s
            """, [item_id])
            comments = cursor.fetchall()

            if not comments:
                continue

            if all(rating.lower() in ['excellent', 'good'] for comment, rating in comments):
                valid_items.append({
                    'item_id': item_id,
                    'title': item_title,
                    'comments': comments
                })

    for item in valid_items:
        print(f"  Item ID: {item['item_id']}, Title: {style.BRIGHT_CYAN}{item['title']}{style.RESET}")
        for comment, rating in item['comments']:
            print(f"    Comment: {comment} (Rating: {rating})")

    #print out all user's items and comments
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, title
            FROM phase_two_item
            WHERE user_id = %s
        """, [requested_user_id])
        items = cursor.fetchall()

        for item_id, item_title in items:
            print(f"  Item ID: {item_id}, Title: {style.BRIGHT_CYAN}{item_title}{style.RESET}")

            cursor.execute("""
                SELECT comment, rating
                FROM phase_two_comment
                WHERE item_id = %s
            """, [item_id])
            comments = cursor.fetchall()

            for comment, rating in comments:
                print(f"    Comment: {comment} (Rating: {rating})")

    return Response({"answer": valid_items}, status=status.HTTP_200_OK)

@api_view(['GET'])
def q2(request):
    category_x = request.query_params.get('categoryX').upper()
    category_y = request.query_params.get('categoryY').upper()

    if not category_x or not category_y:
        return Response({"error": "Both categoryX and categoryY parameters are required."}, status=status.HTTP_400_BAD_REQUEST)

    print(style.RED + "\nQ3" + style.RESET)
    print(f"Requested Categories: {style.CYAN}{category_x}{style.RESET} and {style.CYAN}{category_y}{style.RESET}")

    with connection.cursor() as cursor:
        
        cursor.execute("""
            SELECT u.username
            FROM userauth_user u
            INNER JOIN phase_two_item i1 ON u.id = i1.user_id
            INNER JOIN phase_two_item i2 ON u.id = i2.user_id
            WHERE %s = ANY(i1.categories) AND %s = ANY(i2.categories)
            AND DATE(i1.created_at) = DATE(i2.created_at)
            GROUP BY u.id, u.username, DATE(i1.created_at)
            HAVING COUNT(DISTINCT i1.id) >= 1 AND COUNT(DISTINCT i2.id) >= 1
        """, [f'{category_x}', f'{category_y}'])
        users_with_matching_items = cursor.fetchall()

    # Process the results
    user_list = [user[0] for user in users_with_matching_items]
    for username in user_list:
        print(f"{style.BRIGHT_GREEN}\nUser With Matching Items:{style.RESET} {style.CYAN}{username}{style.RESET}")

    return Response({"answer": user_list}, status=status.HTTP_200_OK)

@api_view(['GET'])
def q1(request):
    print(style.RED + "\nQ1" + style.RESET)

    with connection.cursor() as cursor:
        
        # SQL query to find the most expensive item in each category
        cursor.execute("""
            SELECT unnested_category, MAX(price) AS max_price
            FROM (
                SELECT UNNEST(phase_two_item.categories) AS unnested_category, price
                FROM phase_two_item
            ) AS subquery
            GROUP BY unnested_category
        """)
        most_expensive_items = cursor.fetchall()

    # Process the results
    result = [{'category': item[0], 'max_price': item[1]} for item in most_expensive_items]

    for item in result:
        print(f"Category: {style.CYAN}{item['category']}{style.RESET}, Max Price: {style.BRIGHT_GREEN}{item['max_price']}{style.RESET}")

    return Response({"answer": result}, status=status.HTTP_200_OK)