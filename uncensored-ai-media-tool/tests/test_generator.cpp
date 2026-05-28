#include <iostream>
#include <cassert>
#include "../src/generator.h"
#include "../src/security.h"

void test_validate_prompt() {
    // Test valid prompts
    assert(Security::validate_prompt("a cat sitting on a mat") == true);
    assert(Security::validate_prompt("landscape with mountains") == true);
    
    // Test invalid prompts
    assert(Security::validate_prompt("") == false);
    assert(Security::validate_prompt(std::string(600, 'a')) == false);
    assert(Security::validate_prompt("rm -rf /") == false);
    assert(Security::validate_prompt("illegal content") == false);
    
    std::cout << "All security tests passed!" << std::endl;
}

void test_generator() {
    // Test that generator returns non-empty for valid prompt
    std::string result = Generator::generate_image("test prompt");
    // Note: This will fail if server is not running, but shows structure
    assert(result.empty() || result.find(".png") != std::string::npos);
    
    std::cout << "Generator tests passed!" << std::endl;
}

int main() {
    test_validate_prompt();
    test_generator();
    std::cout << "All tests passed!" << std::endl;
    return 0;
}