#ifndef GENERATOR_H
#define GENERATOR_H

#include <string>

class Generator {
public:
    static std::string generate_image(const std::string& prompt);
};

#endif