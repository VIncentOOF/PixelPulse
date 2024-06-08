import math

password = input("Enter your password: ")

# Calculate the range of characters
unique_chars = len(set(password))
password_length = len(password)

entropy = math.log2(unique_chars ** password_length)
strong_threshold = 64
moderate_threshold = 48

# Determine password strength based on entropy value
if entropy >= strong_threshold:
    print("Password strength: Strong, Entropy bits: ", entropy)
elif entropy >= moderate_threshold:
    print("Password strength: Moderate, Entropy bits: ", entropy)
else:
    print("Password strength: Weak, Entropy bits: ", entropy)

guesses_per_second = 1e9
seconds = 2 ** entropy / guesses_per_second

# Convert seconds to days, hours, and seconds
days = seconds // (24 * 3600)
seconds %= (24 * 3600)
hours = seconds // 3600
seconds %= 3600
minutes = seconds // 60
seconds %= 60

print("Estimated time to crack: {} days, {} hours, {} minutes, {} seconds".format(int(days), int(hours), int(minutes), int(seconds)))
