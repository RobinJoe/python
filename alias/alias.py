bashrc = open("/home/bmoss/.bashrc", "r")
print "\n"
count = 1
for line in bashrc:
	if line[:5] == "alias":
		loc = line.find("=")
		print line[6:loc],
		print " "*(16-loc),
		if count % 5 == 0: print
		count += 1
bashrc.close()

bashrc = open("/home/bmoss/.bashrc", "r")
print "\n\n"
count = 1
for line in bashrc:
	if line[:8] == "function":
		loc = line.find("{")
		print line[9:loc],
		print " "*(25-loc),
		if count % 5 == 0: print
		count += 1		
bashrc.close()
print "\n"
