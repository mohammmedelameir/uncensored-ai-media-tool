#ifndef SECURITY_H
#define SECURITY_H

#include <string>
#include <vector>

class Security {
public:
    static bool validate_prompt(const std::string& prompt);
};

#endif