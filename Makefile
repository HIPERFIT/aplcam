TAIL_CFLAGS=${CFLAGS} -I ${TAIL_ROOT}/include
TAIL_PRELUDE=${TAIL_ROOT}/lib/prelude.apl
APLS=$(shell echo *.apl)
TAILS=$(APLS:%.apl=%.tail)
APLT?=$(TAIL_ROOT)/aplt

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
	$(APLT) -p_types -s_tail -c -o $@ ${TAIL_PRELUDE} include/pre.apl $< include/post.apl

clean:
	rm -rf work filters.fut filters.py *.tail *~ include/*~

demo: filters.py
	./aplcam.py --scale-to 600x400
