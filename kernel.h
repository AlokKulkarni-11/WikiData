#pragma once

extern "C" __global__
void mergeXMLKernel(
    const char* pageLinks,
    const char* categories,
    const char* xmlContent,
    char* outputBuffer,
    int totalFiles,
    int pageCount,
    int categoryCount,
    int xmlSize,
    int slotSize,
    int outputSlotSize
);
