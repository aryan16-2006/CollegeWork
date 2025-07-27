arr = []


n = int(input("How many numbers? "))

for i in range(n):
    num = int(input(f"Enter number: "))
    arr.append(num)


for i in range(1, n):
    key = arr[i]
    j = i - 1
    while j >= 0 and arr[j] > key:
        arr[j + 1] = arr[j]
        j -= 1
    arr[j + 1] = key

print("Sorted array:", arr)
