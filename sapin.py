import math, random, sys;

text = "";

argv = sys.argv;
text += "%s\n" % argv;

hs = 6;
nbp = 10;
lc = 5;
hc = 6;

if len(argv) > 1 and argv[1].isdigit():
	hs = int(argv[1]);
if len(argv) > 2 and argv[2].isdigit():
	nbp = int(argv[2]);
if len(argv) > 3 and argv[3].isdigit():
	lc = int(argv[3]);
if len(argv) > 4 and argv[4].isdigit():
	hc = int(argv[4]);

nbt = hs**2;
if nbt < nbp:
	nbp = nbt;

if lc%2 is 0:
	# if lc+1 > 2*hs-1:
		# lc = hs;
	if lc+1 <= 2*hs-1:
		lc += 1;
	else:
		lc -= 1;

appels = [];
iter = 0;
while len(appels) < nbp:
	x = random.randint(0, hs-1);
	y = random.randint(0, 2*(x+1)-2);
	xy = (x, y);
	if xy not in appels:
		appels.append(xy);
	iter += 1;
text += "%d / %d iterations ~~ %f%%\n%s\n\n" % (iter, nbp, iter/nbp, appels);

for i in range(0, hs):
	for j in range(0, hs-i-1):
		text += " ";
	for j in range(0, 2*(i+1)-1):
		ij = (i, j);
		if ij in appels:
			text += "O";
		else:
			text += "*";
		# text += "(%d,%d)" % (i, j);
	# text += "(%d)" % (i);
	text += "\n";

pad = hs - int(math.floor(lc/2)) -1;
for i in range(0, hc):
	for j in range(0, lc+pad):
		text += " " if j < pad else "|";
	text += "\n";

with open('sapin.txt', 'a+') as fp:
	fp.write("%s%s\n" % (text, "-"*40));
	fp.close();

if sys.version_info[:2] > (2, 7):
	text = text[:-1];

print(text);
