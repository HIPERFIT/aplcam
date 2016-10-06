TAIL_CFLAGS=${CFLAGS} -I ${TAIL_ROOT}/include
TAIL_PRELUDE=${TAIL_ROOT}/lib/prelude.apl
APLS=work/$(shell echo *.apl)
TAILS=$(shell echo *.apl|sed -r 's!([^ ]+)\.apl!work/\1\.tail!g')

ifndef TAIL_ROOT
$(error TAIL_ROOT is not set)
endif

.PHONY: all

all: filters.py

run: all
	./aplcam.py

filters.py: filters.fut
	futhark-pyopencl --library filters.fut

filters.fut: $(TAILS)
	echo $(TAILS)
	tail2futhark --float-as-single --library $(TAILS) -o $@

%.tail: %.apl
	aplt  -p_types -s_tail -c -o $@ ${TAIL_PRELUDE} $<

%.apl: %.tail

work/%.apl: %.apl
	@echo Generating $@ from $*.apl.
	@mkdir -p work
	@rm -f $@
	@echo "image ← ReadCSVInt 'image.txt'" >> $@
	@echo "dims ← ReadCSVInt 'dims.txt'" >> $@
	@echo "dims ← 2 ↑ dims" >> $@
	@echo "degree ← ReadCSVDouble 'degree.txt'" >> $@
	@echo "degree ← degree[1]" >> $@
	@cat $*.apl >> $@
	@echo "⎕ ← image" >> $@
	@echo "0" >> $@

clean:
	rm -rf work filters.fut filters.py
