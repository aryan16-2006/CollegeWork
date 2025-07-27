arr = []


n = int(input("How many numbers? "))

for i in range(n):
    num = int(input(f"Enter number: "))
    arr.append(num)
for i in range(n):
    for j in range(n - 1):
        if arr[j] > arr[j + 1]:
            arr[j], arr[j + 1] = arr[j + 1], arr[j]

print("Sorted array:", arr)
