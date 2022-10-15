all: drawer.cpp
	mkdir -p build
	g++ -o build/drawer drawer.cpp
test:
	make all
	g++ -o build/tests tests.cpp
	build/tests
clean:
	$(RM) build