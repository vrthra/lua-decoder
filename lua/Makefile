LUAC=./lua-5.1.5/src/luac
LUADEC=/home/rahul.gopinath/Research/Decoder_Lua/luadec/luadec
%.luac: %.lua
	$(LUAC) -o $*.luac -s $*.lua
	$(LUAC) -l $*.luac

list-%:
	$(LUAC) -l -l $*.luac
	hexdump -C $*.luac

%.hex: %.luac
	python3 to_hex.py $*.luac > $*.hex
	cat $*.hex

%.bin: %.hex
	python3 to_bin.py $*.hex $*.bin
	$(LUAC) -l -l $*.bin
	#lua $*.bin

uncopile:
	$(luadec)
