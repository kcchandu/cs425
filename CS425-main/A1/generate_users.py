with open('users.txt', 'a') as f:
    for i in range(1, 1001):
        f.write(f"testuser{i}:password{i}\n")
print("Appended 1000 users to users.txt")
