import pytube

#url = input()
yt = pytube.YouTube('https://www.youtube.com/watch?v=GwCUbhE0TY0')
stream = yt.streams.filter(progressive='true').all()
print(stream)

s =1 
for v in videos:
	print(s + ". "+ v)

print("Choose one: ")
choose = int(input())
vid= videos[choose -1]

# yt.streams.first().download(".")

vid.download(".")