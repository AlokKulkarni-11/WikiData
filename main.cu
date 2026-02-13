#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>
#include <filesystem>
#include <cstring>
#include <cuda_runtime.h>
#include "kernel.h"

// ---------------- CUDA error checking macro ----------------
#define CUDA_CHECK(call)                                                   \
do {                                                                       \
    cudaError_t err = call;                                                \
    if (err != cudaSuccess) {                                              \
        std::cerr << "CUDA Error: " << cudaGetErrorString(err)             \
                  << " at " << __FILE__ << ":" << __LINE__ << std::endl;  \
        exit(EXIT_FAILURE);                                                \
    }                                                                      \
} while (0)

// ---------------- Helper: Read full file into string ----------------
std::string readFileToString(const std::string& filePath)
{
    std::ifstream file(filePath);
    if (!file.is_open()) {
        throw std::runtime_error("Cannot open file: " + filePath);
    }

    std::stringstream buffer;
    buffer << file.rdbuf();
    return buffer.str();
}

// ---------------- Helper: Parse simple id + value file ----------------
// Expected format per line:  ID  VALUE
std::vector<std::string> parseSimpleIdValueFile(const std::string& filePath)
{
    std::ifstream file(filePath);
    if (!file.is_open()) {
        throw std::runtime_error("Cannot open file: " + filePath);
    }

    std::vector<std::string> values;
    std::string line;

    while (std::getline(file, line)) {
        std::istringstream ls(line);
        std::string id, value;

        if (ls >> id >> value) {
            values.push_back(value);
        }
    }

    return values;
}

void processData(
    const std::string& xmlFile,
    const std::string& pageSqlFile,
    const std::string& categorySqlFile,
    const std::string& outputFolder,
    int totalFiles)
{
    // Create output folder
    std::filesystem::create_directories(outputFolder);

    // Read XML template
    std::string xmlContent = readFileToString(xmlFile);
    int xmlSize = static_cast<int>(xmlContent.size()) + 1;

    // Parse page titles and categories
    std::vector<std::string> pageLinks = parseSimpleIdValueFile(pageSqlFile);
    std::vector<std::string> categories = parseSimpleIdValueFile(categorySqlFile);

    int pageCount = static_cast<int>(pageLinks.size());
    int categoryCount = static_cast<int>(categories.size());

    if (pageCount == 0) {
        throw std::runtime_error("No pages parsed from: " + pageSqlFile);
    }
    if (categoryCount == 0) {
        throw std::runtime_error("No categories parsed from: " + categorySqlFile);
    }

    // Fixed slot size for each page/category string
    const int SLOT_SIZE = 128;

    // Output slot size per generated XML file
    const int OUTPUT_SLOT_SIZE = 4096;

    // Convert vectors → flat char arrays
    std::vector<char> h_pages(pageCount * SLOT_SIZE, 0);
    std::vector<char> h_categories(categoryCount * SLOT_SIZE, 0);

    for (int i = 0; i < pageCount; i++) {
        std::strncpy(&h_pages[i * SLOT_SIZE], pageLinks[i].c_str(), SLOT_SIZE - 1);
    }

    for (int i = 0; i < categoryCount; i++) {
        std::strncpy(&h_categories[i * SLOT_SIZE], categories[i].c_str(), SLOT_SIZE - 1);
    }

    // ---------------- Allocate GPU memory ----------------
    char* d_pages = nullptr;
    char* d_categories = nullptr;
    char* d_xml = nullptr;
    char* d_output = nullptr;

    CUDA_CHECK(cudaMalloc(&d_pages, h_pages.size()));
    CUDA_CHECK(cudaMalloc(&d_categories, h_categories.size()));
    CUDA_CHECK(cudaMalloc(&d_xml, xmlSize));
    CUDA_CHECK(cudaMalloc(&d_output, totalFiles * OUTPUT_SLOT_SIZE));

    // Copy inputs
    CUDA_CHECK(cudaMemcpy(d_pages, h_pages.data(), h_pages.size(), cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemcpy(d_categories, h_categories.data(), h_categories.size(), cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemcpy(d_xml, xmlContent.c_str(), xmlSize, cudaMemcpyHostToDevice));

    // Clear output
    CUDA_CHECK(cudaMemset(d_output, 0, totalFiles * OUTPUT_SLOT_SIZE));

    // ---------------- Launch kernel ----------------
    int blockSize = 256;
    int numBlocks = (totalFiles + blockSize - 1) / blockSize;

    mergeXMLKernel << <numBlocks, blockSize >> > (
        d_pages,
        d_categories,
        d_xml,
        d_output,
        totalFiles,
        pageCount,
        categoryCount,
        xmlSize,
        SLOT_SIZE,
        OUTPUT_SLOT_SIZE
        );

    CUDA_CHECK(cudaGetLastError());
    CUDA_CHECK(cudaDeviceSynchronize());

    // ---------------- Copy output back ----------------
    std::vector<char> merged(totalFiles * OUTPUT_SLOT_SIZE);
    CUDA_CHECK(cudaMemcpy(merged.data(), d_output, merged.size(), cudaMemcpyDeviceToHost));

    // ---------------- Write files ----------------
    for (int i = 0; i < totalFiles; i++) {
        std::string fileName = outputFolder + "/page_" + std::to_string(i) + ".xml";

        std::ofstream out(fileName, std::ios::binary);
        if (!out.is_open()) {
            std::cerr << "Failed to write: " << fileName << std::endl;
            continue;
        }

        char* start = merged.data() + i * OUTPUT_SLOT_SIZE;

        // Ensure null termination
        start[OUTPUT_SLOT_SIZE - 1] = '\0';

        out << start;
        out.close();
    }

    // ---------------- Cleanup ----------------
    CUDA_CHECK(cudaFree(d_pages));
    CUDA_CHECK(cudaFree(d_categories));
    CUDA_CHECK(cudaFree(d_xml));
    CUDA_CHECK(cudaFree(d_output));

    std::cout << "Done! Generated " << totalFiles << " XML files in: " << outputFolder << "\n";
}

int main()
{
    try {
        std::string xmlFilePath = "data/data.xml";
        std::string pageSqlFilePath = "data/enwiki-latest-page.sql";
        std::string categorySqlFilePath = "data/enwiki-latest-categorylinks.sql";

        std::string outputFolder = "output";

        int totalFiles = 10000;

        processData(
            xmlFilePath,
            pageSqlFilePath,
            categorySqlFilePath,
            outputFolder,
            totalFiles
        );

        return 0;
    }
    catch (const std::exception& e) {
        std::cerr << "Fatal error: " << e.what() << std::endl;
        return 1;
    }
}
