cmake_minimum_required(VERSION 3.10)
project(uncensored-ai-media-tool)

set(CMAKE_CXX_STANDARD 17)

find_package(OpenCV REQUIRED)
find_package(CURL REQUIRED)
find_package(nlohmann_json REQUIRED)

add_executable(uncensored_ai_media_tool
    src/main.cpp
    src/generator.cpp
    src/security.cpp
)

target_link_libraries(uncensored_ai_media_tool
    ${OpenCV_LIBS}
    ${CURL_LIBRARIES}
    nlohmann_json::nlohmann_json
)

add_test(
    NAME test_generator
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/tests/test_generator.cpp
)

enable_testing()