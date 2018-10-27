#include <iostream>
#include "lib1.h"
#include <lib2.h>

void hello1(){
	std::cout << "Hello World! (from lib1)\n";
	hello();
}
