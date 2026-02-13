#include <cuda_runtime.h>
#include "kernel.h"

// Copy a null-terminated string into out buffer safely
__device__ int copyString(char* out, int outPos, int maxOut, const char* src)
{
    while (*src && outPos < maxOut - 1) {
        out[outPos++] = *src++;
    }
    out[outPos] = '\0';
    return outPos;
}

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
    int outputSlotSize)
{
    int idx = blockIdx.x * blockDim.x + threadIdx.x;

    // Prevent out-of-bounds threads
    if (idx >= totalFiles) return;

    // Choose page + category index safely
    int pageIndex = idx % pageCount;
    int catIndex = idx % categoryCount;

    const char* page = pageLinks + pageIndex * slotSize;
    const char* category = categories + catIndex * slotSize;

    char* out = outputBuffer + idx * outputSlotSize;

    // Start writing XML
    int pos = 0;

    pos = copyString(out, pos, outputSlotSize, "<page>\n");

    pos = copyString(out, pos, outputSlotSize, "  <content>");
    pos = copyString(out, pos, outputSlotSize, xmlContent);
    pos = copyString(out, pos, outputSlotSize, "</content>\n");

    pos = copyString(out, pos, outputSlotSize, "  <link>");
    pos = copyString(out, pos, outputSlotSize, page);
    pos = copyString(out, pos, outputSlotSize, "</link>\n");

    pos = copyString(out, pos, outputSlotSize, "  <category>");
    pos = copyString(out, pos, outputSlotSize, category);
    pos = copyString(out, pos, outputSlotSize, "</category>\n");

    pos = copyString(out, pos, outputSlotSize, "</page>\n");

    // Ensure null termination
    out[outputSlotSize - 1] = '\0';
}
