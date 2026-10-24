#include "mfcc.h"
#include <math.h>
#include <stdio.h>

int main(void) {
  float samples[512], actual[10], expected[10] = {-434.245117188f, 31.724918365f, 71.949157715f, 22.652713776f, 29.826322556f, 12.290983200f, -12.415746689f, -89.598945618f, -29.791992188f, 36.174621582f};
  for (int i = 0; i < 512; ++i) samples[i] = sinf((float)i * 0.071f) * 0.2f + (float)(i % 17) * 0.001f;
  vaanicore_mfcc_frame(samples, 512, actual);
  float max_error = 0.0f;
  for (int i = 0; i < 10; ++i) { float error = fabsf(actual[i] - expected[i]); if (error > max_error) max_error = error; }
  printf("max_abs_error=%g\n", max_error);
  return max_error < 0.05f ? 0 : 1;
}
