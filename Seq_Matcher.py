from difflib import SequenceMatcher
text1 = "My Name is Yann"
text2 = "Hi, My Name is Yanno"
sequenceScore = SequenceMatcher(None, text1, text2).ratio()
print(f"Both are {sequenceScore * 100} % similar")