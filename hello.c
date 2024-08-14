#include <omp.h>
 
#include <stdio.h>
#include <stdlib.h>
 
int main(int argc, char* argv[])
{
 
    // Beginning of parallel region
    #pragma omp parallel
    {
 
        printf("Hello World... from thread");
    }
    // Ending of parallel region
}