#include "security.h"
#include <algorithm>
#include <cctype>
#include <regex>

bool Security::validate_prompt(const std::string& prompt) {
    // Check for empty prompts
    if (prompt.empty()) {
        return false;
    }
    
    // Check for excessively long prompts (potential injection)
    if (prompt.length() > 500) {
        return false;
    }
    
    // Block common injection patterns
    std::regex injection_pattern(R"([;|&`$(){}[\]\\])");
    if (std::regex_search(prompt, injection_pattern)) {
        return false;
    }
    
    // Basic content filtering (optional - can be disabled)
    std::string lower_prompt = prompt;
    std::transform(lower_prompt.begin(), lower_prompt.end(), lower_prompt.begin(), ::tolower);
    
    std::vector<std::string> blocked_terms = {
        "illegal", "harm", "violence", "exploit"
    };
    
    for (const auto& term : blocked_terms) {
        if (lower_prompt.find(term) != std::string::npos) {
            return false;
        }
    }
    
    return true;
}