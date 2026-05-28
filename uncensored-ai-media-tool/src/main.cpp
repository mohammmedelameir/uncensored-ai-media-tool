#include <iostream>
#include "generator.h"
#include "security.h"

int main() {
    std::cout << "Uncensored AI Media Tool v1.0" << std::endl;
    
    std::string prompt;
    std::cout << "Enter image prompt: ";
    std::getline(std::cin, prompt);
    
    if (!Security::validate_prompt(prompt)) {
        std::cerr << "Error: Invalid or malicious prompt detected." << std::endl;
        return 1;
    }
    
    std::string image_path = Generator::generate_image(prompt);
    if (!image_path.empty()) {
        std::cout << "Image saved to: " << image_path << std::endl;
    } else {
        std::cerr << "Generation failed." << std::endl;
        return 1;
    }
    
    return 0;
}