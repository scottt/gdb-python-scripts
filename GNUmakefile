CFLAGS := -Os -g -Wall
CXXFLAGS := $(CFLAGS)

PROGRAMS := $(basename $(wildcard *.c *.cc *.S))

%: %.S
	$(CC) -nostdlib $(CFLAGS) $(LDFLAGS) $< -o $@

all: $(PROGRAMS)

lib%.so: %.c
	$(CC) $(CFLAGS) -fPIC -shared $< $(LDFLAGS) -o $@
clean:
	rm -f $(PROGRAMS) core.*
