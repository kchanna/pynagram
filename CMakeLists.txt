cmake_minimum_required(VERSION 3.1)
project(generateWords)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES main.cpp dictionary.cpp dictionary.h)
add_executable(generateWords ${SOURCE_FILES})