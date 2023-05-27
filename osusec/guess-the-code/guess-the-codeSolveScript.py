from pwn import *

#Start connections
a = remote("chal.ctf-league.osusec.org", "1382")
b = remote("chal.ctf-league.osusec.org", "1382")

#Go through inputs, send fake guess ("1"), and receive value
a.recvline()
a.recvline()
a.recv()
a.sendline(b"1")
c = a.recvline()

#Ignore the first 45 characters, and only take the number that is returned
payload = c.decode("utf-8")[44:]

#Go through b, send the value found above from a, send, skip through prompts, and take option 3
b.recvline()
b.recvline()
b.recv()
b.sendline(payload.encode("utf-8"))

for _ in range(6):
    b.recvline()

b.sendline(b"3")

#Get the flag output, print, and close connections
c = b.recvline()

print(c.decode("utf-8"))

a.close()
b.close()

