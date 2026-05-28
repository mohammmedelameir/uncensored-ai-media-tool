#include "generator.h"
#include <curl/curl.h>
#include <nlohmann/json.hpp>
#include <fstream>
#include <iostream>

using json = nlohmann::json;

static size_t WriteCallback(void* contents, size_t size, size_t nmemb, void* userp) {
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}

std::string Generator::generate_image(const std::string& prompt) {
    CURL* curl;
    CURLcode res;
    std::string readBuffer;
    
    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();
    
    if(curl) {
        json data;
        data["prompt"] = prompt;
        data["model"] = "flux-uncensored-v1";
        data["steps"] = 20;
        
        std::string jsonStr = data.dump();
        
        curl_easy_setopt(curl, CURLOPT_URL, "http://localhost:8080/generate");
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, jsonStr.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
        
        struct curl_slist* headers = NULL;
        headers = curl_slist_append(headers, "Content-Type: application/json");
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        
        res = curl_easy_perform(curl);
        
        if(res != CURLE_OK) {
            std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
            curl_easy_cleanup(curl);
            curl_global_cleanup();
            return "";
        }
        
        curl_easy_cleanup(curl);
        curl_global_cleanup();
        
        json response = json::parse(readBuffer);
        std::string base64_image = response["image"];
        
        // Save image (simplified - in real app decode base64 to binary)
        std::string filename = "output_" + std::to_string(time(nullptr)) + ".png";
        std::ofstream out(filename);
        out << base64_image;
        out.close();
        
        return filename;
    }
    
    return "";
}